# Stuff
#
import math
import os.path
import string

import grpc;

import mdb_bp.utils
from mdb_bp import row
from mdb_bp.const import ERR_CONNECTION_CLOSED, ERR_QUERY_ACTIVE, ERR_CNFG_SUPPORT, ERR_CONCURRENT_TRANSACTION
from mdb_bp.file import BasicStoreFile
from mdb_bp.protocol_buffers import odbc_pb2
from mdb_bp.protocol_buffers.odbc_pb2 import StoreFileResponse, ExportFileResponse, StoreFileRequest, ExportFileRequest
from mdb_bp.protocol_buffers.odbc_pb2_grpc import MDBServiceStub
from mdb_bp.row import build_result_set
from mdb_bp.statement import stmt
from mdb_bp.result import Result
from mdb_bp.transaction import TX, TXOptions


class Connection:
    def __init__(
            self,
            cfg,
    ):
        self.cfg = cfg
        # self.status = status

        self._channel = grpc.insecure_channel(self.cfg.address())
        self._stub = MDBServiceStub(self._channel)

        self.closed = False

        # Query
        self.active_query = False
        self._query_stream = None  # odbc_pb2_grpc.MDBServiceStub
        self._tx = None

        # Configure the connection
        self.auth = odbc_pb2.authPacket()

        init_req = odbc_pb2.InitializationRequest(
            username=self.cfg.username,
            password=self.cfg.password,
            db_name=self.cfg.database_name,
            auth=self.auth
        )

        self.auth = self._stub.InitializeConnection(init_req)

    def __enter__(self):
        return self

    def prepare(self, query):
        # Create and return a statement
        return stmt(self, query)

    # TODO @Paul: Finalize function
    def begin(self, isolation_level=1, read_only=False):
        # Make sure the db connection is still live
        if self.is_closed():
            raise Exception(ERR_CONNECTION_CLOSED)

        # Make sure this is the only tx?
        if self._tx is not None:
            raise Exception(ERR_CONCURRENT_TRANSACTION)

        # Build the request
        req = odbc_pb2.XactRequest(
            auth=self.auth,
            isolation_level=isolation_level,
            read_only=read_only
        )

        resp = self._stub.Begin(req)

        self._tx = TX(
            conn=self,
            id=resp.xact_id,
            tx_options=TXOptions(isolation_level, read_only)
        )
        return self._tx

    def exec(self, query: string, args=[]) -> Result:
        # Make sure the db connection is still live
        if self.is_closed():
            raise Exception(ERR_CONNECTION_CLOSED)

        # Prepare the statement
        query = self._validate_and_prepare_statement(query, args)

        # Execute the query
        try:
            affected_rows, insert_id = self._exec_helper(query)
        except Exception as err:
            err = "Err: {}".format(err)
            raise Exception(err)

        # Generate the response
        return Result(affected_rows, insert_id)

    def _exec_helper(self, query) -> (int, int):
        # Build the request object
        req = odbc_pb2.ExecRequest(
            auth=self.auth,
            statement=query
        )

        # Send the request using the connection stub
        resp = self._stub.Exec(req)
        # TODO: Update JWT

        # Generate the response
        return resp.affected_rows, resp.insert_id

    def query(self, query: string, args=[]) -> row.Rows:
        # Make sure the db connection is live
        if self.is_closed():
            raise Exception(ERR_CONNECTION_CLOSED)

        # Make sure there are no active queries
        if self.active_query:
            raise Exception(ERR_QUERY_ACTIVE)

        # Prepare the statement
        query = self._validate_and_prepare_statement(query, args)

        # Build the request
        req = odbc_pb2.QueryRequest(
            auth=self.auth,
            statement=query,
            max_response_length=self.cfg.parameters[
                "max_response_length"] if "max_response_length" in self.cfg.parameters else -1,
            batch_size=self.cfg.parameters["fetch_size"] if "fetch_size" in self.cfg.parameters else 10
        )

        # Execute the query
        try:
            resp_client = self._stub.Query(req)
            # TODO: Update JWT
        except Exception as err:
            err = "Err: {}".format(err)
            print(err)
            raise Exception(err)

        # # Update auth
        # self.auth = resp.auth

        # Store the query stream
        self._query_stream = resp_client

        rows = None
        for stream_resp in self._query_stream:
            if len(stream_resp.result_set) == 0:
                rs = row.ResultSet(row.build_column_list(stream_resp.resp_schema))
            else:
                rs = build_result_set(stream_resp.resp_schema, stream_resp.result_set)

            rows = row.Rows(
                stream_recv=self._query_stream,
                schema=stream_resp.resp_schema,
                rs=rs,
                done=stream_resp.done
            )
            break

        return rows

    def store_file(
            self, file_name: string, file_path: string, file_extension: string, package_size: int = 2500
    ) -> StoreFileResponse:
        writable_stream = self._stub.StoreFile.future(
            BasicStoreFile(
                self.auth,
                file_name, file_path, file_extension, package_size
            ),
        )

        return writable_stream.result()

    def export_file(
            self, file_name: string, output_path: string, file_extension: string, package_size: int = 2500
    ) -> ExportFileResponse:
        export_file_response_stream = self._stub.ExportFile(
            ExportFileRequest(
                auth=self.auth,

                file_name=file_name,
                file_extension=file_extension,

                file_bit_size=package_size
            )
        )

        with open(output_path, "wb") as out_file:
            for resp in export_file_response_stream:
                out_file.write(resp.file_bit_bytes)

    def close_query(self):
        # Send a close query request
        return self._stub.CloseQuery(self.auth)

    def close(self):
        # Close the connection
        if not self.closed:
            self.closed = True

            # Close the gRPC channel
            if self._channel:
                self._channel.close()
            # Close the query stub
            # if self._query_stream:
            #     self._query_stream.close()

    def clear_tx(self):
        self._tx = None

    def is_closed(self):
        return self.closed

    def _validate_and_prepare_statement(self, query: string, args=[]) -> string:
        # Interpolate any parameters
        if len(args) != 0:
            if not self.cfg.parameters['interpolate_params']:
                raise Exception(ERR_CNFG_SUPPORT)

            query = mdb_bp.utils.interpolate_params(query, args)
        return query
