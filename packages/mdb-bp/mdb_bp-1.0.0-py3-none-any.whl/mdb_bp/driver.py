'''
dsn="admin:password@tcp(0.0.0.0:8080)/master",

'''
from mdb_bp.config import Config
from mdb_bp.connection import Connection
from mdb_bp.connector import connector

'''
connect()

connect takes in a series of parameters that describe a data source and initialize a connection. 



'''


def connect(
        username="",
        password="",
        connection_protocol="tcp",
        server_address="0.0.0.0",
        server_port=8080,
        database_name="master",
        parameters={"interpolateParams": True},
) -> Connection:
    # Build the config
    cfg = Config(
        username, password,
        connection_protocol,
        server_address, server_port,
        database_name,
        parameters,
    )

    # Create a new connection object
    conn = connector(cfg)
    return conn.connect()


def open_connector(
        username="",
        password="",
        connection_protocol="tcp",
        server_address="localhost",
        server_port=8080,
        database_name="master",
        parameters={"interpolateParams": True},
):
    # Build the config
    cfg = Config(
        username, password,
        connection_protocol,
        server_address, server_port,
        database_name,
        parameters,
    )

    conn = connector(cfg)
    return conn
