import os

from mdb_bp.config import Config
from mdb_bp.connector import connector


def test_basic_grpc_connection(self):
    # Build test config
    cfg = Config(
        username=os.getenv("DATABASE_USERNAME"),
        password=os.getenv("DATABASE_PASSWORD"),
        connection_protocol="tcp",
        server_address=os.getenv("DATABASE_ADDRESS"),
        server_port=os.getenv("DATABASE_PORT"),
        database_name=os.getenv("DATABASE_NAME"),
        parameters={"interpolateParams": True},
    )
    print("Connection Address: {}".format(cfg.address()))

    conn = connector(cfg).connect()

    conn.close()
