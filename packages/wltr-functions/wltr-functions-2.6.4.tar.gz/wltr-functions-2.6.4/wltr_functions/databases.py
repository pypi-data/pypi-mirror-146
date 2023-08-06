import pymongo
import psycopg2
import cx_Oracle
import urllib.parse


class Databases(object):
    class Oracle:
        def __init__(self, oracle_user, oracle_pwd, oracle_dsn):
            self.oracle_user = oracle_user
            self.oracle_pwd = oracle_pwd
            self.oracle_dsn = oracle_dsn

        def conn_oracle(self):
            try:
                cnxn = cx_Oracle.connect(user=self.oracle_user,
                                         password=self.oracle_pwd,
                                         dsn=self.oracle_dsn)

                return cnxn

            except ValueError as e:
                return print(e)

    class Redshift:
        def __init__(self, rs_db, rs_host, rs_port,
                     rs_user, rs_pwd):
            self.rs_db = rs_db
            self.rs_host = rs_host
            self.rs_port = int(rs_port)
            self.rs_user = rs_user
            self.rs_pwd = rs_pwd

        def conn_redshift(self):
            try:
                cnxn = psycopg2.connect(dbname=self.rs_db,
                                        host=self.rs_host,
                                        port=self.rs_port,
                                        user=self.rs_user,
                                        password=self.rs_pwd)

                return cnxn

            except ValueError as e:
                return print(e)

    class DocumentDB:
        def __init__(self, ddb_host, ddb_port, ddb_user,
                     ddb_pwd, ddb_public_key):
            self.ddb_host = ddb_host
            self.ddb_port = int(ddb_port)
            self.ddb_user = urllib.parse.quote_plus(ddb_user)
            self.ddb_pwd = urllib.parse.quote_plus(ddb_pwd)

            self.ddb_public_key = ddb_public_key

        def conn_ddb(self):
            try:
                engine = pymongo.MongoClient

                cnxn = engine('mongodb://%s:%s@%s:%s'
                              % (self.ddb_user, self.ddb_pwd,
                                 self.ddb_host, self.ddb_port),
                              tls=True,
                              tlsCAFile=self.ddb_public_key
                              )
                return cnxn

            except ValueError as e:
                return print(e)


class SparkDatabases(object):
    class Oracle:
        def __init__(self, spark_instance, host, port, service, user, pwd, arg):
            self.spark_instance = spark_instance
            self.host = host
            self.port = port
            self.service = service
            self.user = user
            self.pwd = pwd
            self.arg = arg

        def conn_oracle(self):
            try:
                data = (self.spark_instance.read \
                        .format("jdbc") \
                        .option("url",
                                "jdbc:oracle:thin:@(DESCRIPTION="
                                "(ADDRESS=(PROTOCOL=TCP)"
                                "(HOST=" + self.host + ")" \
                                                       "(PORT=" + self.port + "))" \
                                                                              "(CONNECT_DATA=(SERVER=DEDICATED)" \
                                                                              "(SERVICE_NAME=" + self.service + ")))") \
                        .option("driver", "oracle.jdbc.driver.OracleDriver") \
                        .option("user", self.user) \
                        .option("password", self.pwd) \
                        .option("numPartitions", 4) \
                        .option("dbtable", self.arg)) \
                    .load()

                return data

            except ValueError as e:
                return print(e)
