import os
import io
import math
import logging
import psycopg2
import psycopg2.extras
from s3.client import Client as s3_client
from clickhouse_driver import Client
from pg_s3_ch.sql_queries import SQL_HISTORY, SQL_HISTORY_RANGE, SQL_HISTORY_RANGE_NO_INT, SQL_HISTORY_NO_INT, \
    SQL_CH_TABLES, \
    SQL_PG_TABLES

PG_HISTORY_STEP_DEFAULT = 500000


class PGS3CH:
    """

    """

    def __init__(self, config, s3_config, ch_config, pg_config):
        """

        :param config:
        :param s3_config:
        :param ch_config:
        :param pg_config:
        """

        self.execution_date = os.getenv('execution_date')

        self.config = config
        self.s3_config = s3_config
        self.pg_config = pg_config
        self.ch_config = ch_config

        if 'temp_table_prefix' in ch_config:
            self.temp_table_prefix = ch_config['temp_table_prefix']
        else:
            self.temp_table_prefix = '_temp_'

        self.ch_client = None
        self.connect_to_ch()

        self.entity_name = self.config["name"]
        self.key_field = self.config["key_field"] if "key_field" in self.config else "id"
        self.pg_history_step = self.config[
            "pg_history_step"] if "pg_history_step" in self.config else PG_HISTORY_STEP_DEFAULT
        self.schema_ch_insert_fields = []
        self.schema_pg_select_fields = {}
        self.ch_fields = {}
        self.key_field_is_int = True
        self.ch_exclude_columns = ','.join(["'" + item + "'" for item in self.config['ch_exclude_columns'].split(
            ',')]) if 'ch_exclude_columns' in self.config else "''"

    def get_table_schema_ch(self):
        sql = """select name, type, comment from system.columns where database='{database}' and table='{table}'
                 AND name NOT IN ({exclude_columns})   """.format(database=self.ch_config['database'],
                                                                  table=self.config['name'],
                                                                  exclude_columns=self.ch_exclude_columns)
        logging.info(sql)
        result = self.ch_client.execute(sql)
        type_key_field = [r[1] for r in result if r[0] == self.key_field][0]

        if 'int' not in type_key_field.lower():
            self.key_field_is_int = False

        for row in result:
            if row[2].find('Exclude') == -1:
                self.schema_pg_select_fields[row[0]] = row[1]

            if row[2].find('#OnInsert:') > -1:
                start = row[2].find('#OnInsert:') + 10
                end = row[2].find(':EndOnInsert#')
                self.schema_ch_insert_fields.append(row[2][start:end])
            else:
                self.schema_ch_insert_fields.append(row[0])

        if len(self.schema_pg_select_fields) < 1:
            logging.info('CH schema error: {ch_fields}'.format(ch_fields=self.schema_pg_select_fields))
            exit(1)

        if len(self.schema_ch_insert_fields) < 1:
            logging.info(
                'CH schema error: {table}. Have you already created the table?'.format(table=self.config['name']))
            exit(1)

        logging.info('CH schema for {database}.{table} - OK'.format(database=self.ch_config['database'],
                                                                    table=self.config['name']))

    def sync_tables(self, tables_to_exclude=None):
        """
        :param tables_to_exclude: list of tables shouldn't  being considered
        :return: tuple : (list of tables need to remove, list of tables need to create or recreate)
        """
        logging.info('Get tables from pg')
        cnx = self.connect_to_pg()

        cursor = cnx.cursor()
        tables_to_exclude = ','.join(["'" + item + "'" for item in tables_to_exclude.split(
            ',')]) if tables_to_exclude else "''"

        sql = SQL_PG_TABLES.format(tables_to_exclude=tables_to_exclude)
        cursor.execute(sql)
        tables_pg = [r[0] for r in cursor]
        cursor.close()
        cnx.close()

        logging.info('Get tables from ch')

        sql = SQL_CH_TABLES.format(database=self.ch_config['database'], tables_to_exclude=tables_to_exclude)
        result = self.ch_client.execute(sql)
        tables_ch = [r[0] for r in result]
        return tables_ch, tables_pg

    def save_sync_tables(self, client_description, save_table_name, tables_to_exclude):
        """

        :param client_description:
        :param save_table_name:
        :param tables_to_exclude:
        :return:
        """
        tables_ch, tables_pg = self.sync_tables(tables_to_exclude=tables_to_exclude)
        tables_to_remove = [c for c in tables_ch if c not in tables_pg]

        new_tables = []
        for row in tables_pg:
            rr = {"client_description": client_description,
                  "table_name_ch": row,
                  "table_name_pg": row,
                  "database_pg": self.pg_config["database"],
                  "database_ch": self.ch_config["database"]}

            new_tables.append(rr)

        table_name = f"{save_table_name}"
        if len(tables_pg) > 0:
            columns = list(rr.keys())
            columns = ",".join(columns)

        for rr in new_tables:

            sql_stat = "select 1 from {table_name} where database_pg = '{database_pg}' and table_name_pg = '{table_name_pg}' and database_ch = '{database_ch}'".format(
                table_name=table_name,
                database_pg=self.pg_config["database"],
                table_name_pg=rr["table_name_pg"],
                database_ch=self.ch_config["database"])

            x = self.ch_client.execute(sql_stat)
            if len(x) == 0:
                logging.info(f"Add new table {table_name}")
                self.ch_client.execute(
                    f"INSERT INTO {table_name} ({columns}) VALUES", [rr], types_check=True
                )

        for rr in tables_to_remove:
            drop_stat = "DROP TABLE IF EXISTS  {database_ch}.{table_name_pg}".format(
                database_ch=self.ch_config["database"], table_name_pg=rr)
            # logging.info(drop_stat)
            # self.ch_client.execute(drop_stat)
            # sql_stat_remove = """ALTER TABLE  {table_name}
            #               ON CLUSTER '{{cluster}}'
            #               DELETE WHERE table_name_pg  = '{database_pg}' AND database_pg = '{table_name_pg}' and database_ch = '{database_ch}'""".format(
            #     table_name=table_name,
            #     database_pg=self.pg_config["database"],
            #     table_name_pg=rr,
            #     database_ch=self.ch_config["database"])
            #
            # self.ch_client.execute(sql_stat_remove)

    def connect_to_ch(self):

        settings = {'insert_quorum': 3}

        self.ch_client = Client(
            host=self.ch_config['host'],
            user=self.ch_config['user'],
            password=self.ch_config['password'],
            database=self.ch_config['database'],
            settings=settings
        )

    def connect_to_pg(self):
        cnx = psycopg2.connect(user=self.pg_config['user'],
                               password=self.pg_config['password'],
                               host=self.pg_config['host'],
                               port=self.pg_config['port'],
                               database=self.pg_config['database'],
                               sslmode='disable')

        cnx.set_client_encoding('UTF8')
        return cnx

    def extract_to_s3(self):
        logging.info('Starting extract to s3')
        cnx = self.connect_to_pg()
        cursor = cnx.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql_history_local = SQL_HISTORY

        if self.key_field_is_int:
            sql = SQL_HISTORY_RANGE.format(key_field=self.key_field, name=self.entity_name)
            cursor.execute(sql)
        else:
            logging.info("Change logic of extracting data")
            sql = SQL_HISTORY_RANGE_NO_INT.format(key_field=self.key_field, name=self.entity_name)
            cursor.execute(sql)
            sql_history_local = SQL_HISTORY_NO_INT

        for row in cursor:
            min_id = row['min_id']
            max_id = row['max_id']
        cursor.close()

        logging.info('Min ID: {min_id}'.format(min_id=min_id))
        logging.info('Max ID: {max_id}'.format(max_id=max_id))

        if min_id is None or max_id is None:
            logging.info('Max_id or min_id is None. Process is stopped.')
            exit(0)

        step = self.pg_history_step

        end = math.ceil(max_id / step)
        logging.info('Range from 0 to {end}, multiply by {step}'.format(end=end, step=step))

        for id in range(0, end):
            range_from = min_id + id * step
            range_to = min_id + id * step + step - 1

            sql = sql_history_local.format(
                key_field=self.key_field,
                name=self.entity_name,
                fields='"' + '","'.join(self.schema_pg_select_fields.keys()) + '"', range_from=range_from,
                range_to=range_to)

            logging.info(sql)

            cursor = cnx.cursor()
            cursor.execute(sql)
            fa = io.StringIO()
            cursor.copy_to(fa, '({sql})'.format(sql=sql), sep="\t")

            data = fa.getvalue()
            file_name = '{entity_name}_{range_from}.tsv'.format(entity_name=self.entity_name, range_from=range_from)

            logging.info('Copying to S3: {}'.format(self.s3_config['S3_ENDPOINT_URL']))

            client = s3_client(
                aws_access_key_id=self.s3_config['S3_ACCESS_KEY'],
                aws_secret_access_key=self.s3_config['S3_ACCESS_SECRET'],
                endpoint_url=self.s3_config['S3_ENDPOINT_URL'],
                bucket=self.s3_config['S3_TOPMIND_CLIENT_DATA_BUCKET'],
            )
            path = '{upload_path}/{filename}'.format(upload_path=self.s3_config['UPLOAD_PATH'],
                                                     filename=os.path.basename(file_name))
            client.create_file(path=path, data=data)

        cnx.close()

        logging.info('Full extract finished')

    def get_partion_sorting_key(self):
        sql = """select distinct sorting_key, partition_key
                 from system.tables
                 where name = '{name}'
                      and database = '{database}'""".format(database=self.ch_config['database'],
                                                            name=self.config['name'])

        result = self.ch_client.execute(sql)[0]

        return result

    def create_temporary_table(self):

        order_by, partition_by = self.get_partion_sorting_key()
        temp_table_partition_by = partition_by
        temp_table_order_by = order_by

        sql = """CREATE TABLE {staging_database}.{temp_table_prefix}{table} ON CLUSTER '{{cluster}}' AS {database}.{table} 
                    ENGINE=ReplicatedMergeTree() 
                    PARTITION BY {temp_table_partition_by}
                    ORDER BY {temp_table_order_by}""".format(staging_database=self.ch_config['staging_database'],
                                                             temp_table_prefix=self.temp_table_prefix,
                                                             database=self.ch_config['database'],
                                                             table=self.entity_name,
                                                             temp_table_order_by=temp_table_order_by,
                                                             temp_table_partition_by=temp_table_partition_by)
        logging.info(sql)
        self.ch_client.execute(sql)

    def drop_temporary_table(self):
        sql = """DROP TABLE IF EXISTS {staging_database}.{temp_table_prefix}{table} ON CLUSTER '{{cluster}}'""".format(
            staging_database=self.ch_config['staging_database'],
            temp_table_prefix=self.temp_table_prefix,
            table=self.config['name'])
        self.ch_client.execute(sql)
        logging.info(sql)

    def optimize(self):
        """

        :return: None
        """
        sql = """SELECT partition, count() cnt from system.parts where database='{database}' and table='{table}' and active
                GROUP BY partition 
                having cnt > 1""".format(database=self.ch_config['database'], table=self.config['name'])
        result = self.ch_client.execute(sql)

        for row in result:
            logging.info('Partition {partition} has {parts} parts'.format(partition=row[0], parts=row[1]))
            sql_optimize = """OPTIMIZE TABLE {database}.{table} ON CLUSTER '{{cluster}}' PARTITION {partition} """.format(
                database=self.ch_config['database'], table=self.config['name'], partition=row[0])
            logging.info(sql_optimize)
            self.ch_client.execute(sql_optimize)
            logging.info('OK')

    def s3_to_temp(self):
        """

        :return:
        """

        schema = []
        schema_insert = []

        for k in self.schema_pg_select_fields:
            schema.append(k + ' ' + self.schema_pg_select_fields[k])

        for k in self.schema_ch_insert_fields:
            schema_insert.append(k)

        logging.info('Copying from {s3_endpoint_url}/{bucket} to {database}.{temp_table_prefix}{table}'.format(
            s3_endpoint_url=self.s3_config['S3_ENDPOINT_URL'],
            bucket=self.s3_config['S3_TOPMIND_CLIENT_DATA_BUCKET'],
            database=self.ch_config['database'],
            temp_table_prefix=self.temp_table_prefix,
            table=self.config['name']
        ))

        sql = """
            INSERT INTO {staging_database}.{temp_table_prefix}{table}
            SELECT 
                {schema_insert}, NOW()
            FROM s3("{endpoint_url}/{bucket}/{upload_path}/{entity_name}_*.tsv", 
                    '{S3_ACCESS_KEY}',
                    '{S3_ACCESS_SECRET}',
                    'TSV', 
                    '{schema}'
                    );
            """.format(staging_database=self.ch_config['staging_database'],
                       table=self.config['name'],
                       temp_table_prefix=self.temp_table_prefix,
                       endpoint_url=self.s3_config['S3_ENDPOINT_URL'],
                       bucket=self.s3_config['S3_TOPMIND_CLIENT_DATA_BUCKET'],
                       upload_path=self.s3_config['UPLOAD_PATH'],
                       S3_ACCESS_KEY=self.s3_config['S3_ACCESS_KEY'],
                       S3_ACCESS_SECRET=self.s3_config['S3_ACCESS_SECRET'],
                       entity_name=self.entity_name,
                       schema=', '.join(schema),
                       schema_insert=', '.join(schema_insert)
                       )
        logging.info(sql)

        self.ch_client.execute(sql)

        logging.info('Loading from S3 successful')

    def exchange_temp_to_prod(self):
        """

        :return:
        """

        sql = """EXCHANGE TABLES {staging_database}.{temp_table_prefix}{table} AND {database}.{table} ON CLUSTER '{{cluster}}' """.format(
            staging_database=self.ch_config['staging_database'],
            temp_table_prefix=self.temp_table_prefix,
            database=self.ch_config['database'],
            table=self.config['name'])

        logging.info(sql)
        self.ch_client.execute(sql)
