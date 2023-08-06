import requests
from lightwood.api import dtype
from mindsdb.integrations.base import Integration
from mindsdb.utilities.log import log


class ClickhouseConnectionChecker:
    def __init__(self, **kwargs):
        self.host = kwargs.get("host")
        self.port = kwargs.get("port")
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")

    def check_connection(self):
        try:
            res = requests.post(f"http://{self.host}:{self.port}",
                                data="select 1;",
                                params={'user': self.user, 'password': self.password})
            connected = res.status_code == 200
        except Exception:
            connected = False
        return connected


class Clickhouse(Integration, ClickhouseConnectionChecker):
    def __init__(self, config, name, db_info):
        super().__init__(config, name)
        self.user = db_info.get('user', 'default')
        self.password = db_info.get('password', None)
        self.host = db_info.get('host')
        self.port = db_info.get('port')

    def _to_clickhouse_table(self, dtype_dict, predicted_cols, columns):
        subtype_map = {
            dtype.integer: 'Nullable(Int64)',
            dtype.float: 'Nullable(Float64)',
            dtype.binary: 'Nullable(UInt8)',
            dtype.date: 'Nullable(Date)',
            dtype.datetime: 'Nullable(Datetime)',
            dtype.binary: 'Nullable(String)',
            dtype.categorical: 'Nullable(String)',
            dtype.tags: 'Nullable(String)',
            dtype.image: 'Nullable(String)',
            dtype.video: 'Nullable(String)',
            dtype.audio: 'Nullable(String)',
            dtype.short_text: 'Nullable(String)',
            dtype.rich_text: 'Nullable(String)',
            dtype.quantity: 'Nullable(String)',
            dtype.num_array: 'Nullable(String)',
            dtype.cat_array: 'Nullable(String)',
            dtype.num_tsarray: 'Nullable(String)',
            dtype.cat_tsarray: 'Nullable(String)',
            'default': 'Nullable(String)'
        }

        column_declaration = []
        for name in columns:
            try:
                col_subtype = dtype_dict[name]
                new_type = subtype_map.get(col_subtype, subtype_map.get('default'))
                column_declaration.append(f' `{name}` {new_type} ')
                if name in predicted_cols:
                    column_declaration.append(f' `{name}_original` {new_type} ')
            except Exception as e:
                log.error(f'Error: can not determine clickhouse data type for column {name}: {e}')

        return column_declaration

    def _query(self, query):
        params = {'user': self.user}

        if self.password is not None:
            params['password'] = self.password

        host = self.host
        port = self.port

        response = requests.post(f'http://{host}:{port}', data=query, params=params)

        if response.status_code != 200:
            raise Exception(f'Error: {response.content}\nQuery:{query}')

        return response

    def _get_mysql_user(self):
        return f"{self.config['api']['mysql']['user']}_{self.name}"

    def _escape_table_name(self, name):
        return '`' + name.replace('`', '\\`') + '`'

    def setup(self):
        self._query(f'DROP DATABASE IF EXISTS {self.mindsdb_database}')
        self._query(f'CREATE DATABASE IF NOT EXISTS {self.mindsdb_database}')

        msqyl_conn = self.config['api']['mysql']['host'] + ':' + str(self.config['api']['mysql']['port'])
        msqyl_pass = self.config['api']['mysql']['password']
        msqyl_user = self._get_mysql_user()

        q = f"""
            CREATE TABLE IF NOT EXISTS {self.mindsdb_database}.predictors (
                name String,
                status String,
                accuracy String,
                predict String,
                update_status String,
                mindsdb_version String,
                error String,
                select_data_query String,
                training_options String
                ) ENGINE=MySQL('{msqyl_conn}', 'mindsdb', 'predictors', '{msqyl_user}', '{msqyl_pass}')
        """
        self._query(q)
        q = f"""
            CREATE TABLE IF NOT EXISTS {self.mindsdb_database}.commands (
                command String
            ) ENGINE=MySQL('{msqyl_conn}', 'mindsdb', 'commands', '{msqyl_user}', '{msqyl_pass}')
        """
        self._query(q)

    def register_predictors(self, model_data_arr):
        for model_meta in model_data_arr:
            name = self._escape_table_name(model_meta['name'])

            predict = model_meta['predict']
            if not isinstance(predict, list):
                predict = [predict]

            columns_sql = ','.join(self._to_clickhouse_table(
                model_meta['dtype_dict'],
                predict,
                list(model_meta['dtype_dict'].keys())
            ))
            columns_sql += ',`when_data` Nullable(String)'
            columns_sql += ',`select_data_query` Nullable(String)'
            for col in predict:
                columns_sql += f',`{col}_confidence` Nullable(Float64)'

                if model_meta['dtype_dict'][col] in (dtype.integer, dtype.float):
                    columns_sql += f',`{col}_min` Nullable(Float64)'
                    columns_sql += f',`{col}_max` Nullable(Float64)'
                columns_sql += f',`{col}_explain` Nullable(String)'

            msqyl_conn = self.config['api']['mysql']['host'] + ':' + str(self.config['api']['mysql']['port'])
            msqyl_pass = self.config['api']['mysql']['password']
            msqyl_user = self._get_mysql_user()

            self.unregister_predictor(model_meta['name'])
            q = f"""
                CREATE TABLE {self.mindsdb_database}.{name}
                ({columns_sql}
                ) ENGINE=MySQL('{msqyl_conn}', 'mindsdb', {name}, '{msqyl_user}', '{msqyl_pass}')
            """
            self._query(q)

    def unregister_predictor(self, name):
        q = f"""
            drop table if exists {self.mindsdb_database}.{self._escape_table_name(name)};
        """
        self._query(q)

    def get_tables_list(self):
        q = """
            SELECT database, table
            FROM system.parts
            WHERE active and database NOT IN  ('system', 'mdb_system')
            GROUP BY database, table
            ORDER BY database, table;
        """
        tables_list = self._query(q)
        tables = [f"{table[0]}.{table[1]}" for table in tables_list]
        return tables

    def get_columns(self, query):
        q = f"SELECT * FROM ({query}) LIMIT 1 FORMAT JSON"
        query_result = self._query(q).json()
        columns_info = query_result['meta']
        columns = [column['name'] for column in columns_info]
        return columns
