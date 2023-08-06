from mdb_bp.connection import Connection


class connector:
    def __init__(self, cfg):
        self.cfg = cfg

    def connect(self):
        # Connect to the database with the gRPC client side protocol
        return Connection(
            cfg=self.cfg,
            # grpc_stub=channel
        )
