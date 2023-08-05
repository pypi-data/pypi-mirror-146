import uuid
from datetime import datetime
import struct

from mdb_bp.bitmap import Bitmap
from mdb_bp.protocol_buffers import odbc_pb2
from mdb_bp.utils import build_table


class ResultSet:
    def __init__(self, column_names, rows=[]):
        self.column_names = column_names
        self.rows = rows

    def build_next_result_set(self, schema, rs):
        rows = [None] * len(rs)

        assert len(rs) > 0, "rows is empty"

        for i in range(len(rs)):
            row = {}  # [None] * len(columns)

            columns = rs[i].columns
            null_bitmap = Bitmap(rs[i].null_column_bitmap)
            for j in range(len(columns)):
                col = columns[j]

                # If the column is not NULL add it to the dictionary
                if null_bitmap.get(j) == 0:
                    try:
                        row[schema.column_name[j]] = convert_column_to_value(col, schema.column_type[j])
                    except Exception as err:
                        err = "Err: {}".format(err)
                        print(err)
                        raise ValueError(err)

            rows[i] = row

        self.rows = rows


class Rows:
    def __init__(self, stream_recv, schema, rs, done):
        self.stream_recv = stream_recv

        self.schema = schema

        self.set = rs
        self.next_set = None

        self.pos = 0
        self.done = done

    def __str__(self):
        #  Build the header
        table_rows = []
        for col in self.schema.column_name:
            table_rows.append([col])

        # Build the rows
        itr = iter(self)
        for row_dict in itr:
            for i in range(len(self.schema.column_name)):
                col = self.schema.column_name[i]

                try:
                    table_rows[i].append("{}".format(row_dict[col]))
                except:
                    table_rows[i].append("NULL")

            # table_rows.append(row)

        return build_table(table_rows)

    def columns(self):
        return self.set.column_names

    def __iter__(self):
        return self

    def __next__(self):
        if not self.set:
            a = []
        # Check for next
        if self.pos < len(self.set.rows):
            resp = self.set.rows[self.pos]
            self.pos += 1
            return resp

        # Check for next set
        if self.has_next_result_set():
            # Build the next set
            self.set.build_next_result_set(
                self.next_set.resp_schema,
                self.next_set.result_set
            )
            # Reset the position
            self.pos = 0

            # Set next_set to None
            self.next_set = None

            # Call next again
            return self.__next__()

        # If there is no next, stop the iterator
        raise StopIteration

    def has_next_result_set(self):
        if self.next_set is not None:
            return True

    def close(self):
        self.stream_recv.close()


def build_column_list(schema):
    if schema.table_name == "":
        column_names = schema.column_name
    else:
        column_names = ["{}.".format(schema.table_name)] * len(schema.column_name)
        for i in range(len(schema.column_name)):
            column_names[i] += schema.column_name[i]
    return column_names


def build_result_set(schema, set):
    column_names = build_column_list(schema)
    rs = ResultSet(column_names)

    rs.build_next_result_set(schema, set)
    return rs


def convert_column_to_value(col, col_type):
    if col_type == odbc_pb2.BYTEARRAY:
        return col
    elif col_type == odbc_pb2.STRING:
        return col.decode('utf-8')
    elif col_type == odbc_pb2.INT8 or col_type == odbc_pb2.INT16 or \
            col_type == odbc_pb2.INT32 or col_type == odbc_pb2.INT64:
        return int.from_bytes(col, byteorder='little', signed=True)
    elif col_type == odbc_pb2.UINT8 or col_type == odbc_pb2.UINT16 or \
            col_type == odbc_pb2.UINT32 or col_type == odbc_pb2.UINT64:
        return int.from_bytes(col, byteorder='little', signed=False)
    elif col_type == odbc_pb2.FLOAT32 or col_type == odbc_pb2.FLOAT64:
        return float.fromhex(hex(int.from_bytes(col, byteorder='little', signed=False)))
    elif col_type == odbc_pb2.BOOL:
        return bool(col[0] == 1)
    elif col_type == odbc_pb2.TIMESTAMP:
        return datetime.utcfromtimestamp(int.from_bytes(col[0:8], byteorder='little', signed=False) // 1000000000)
    elif col_type == odbc_pb2.DATETIME:
        return datetime.fromtimestamp(int.from_bytes(col[0:8], byteorder='little', signed=False))
    elif col_type == odbc_pb2.DATE:
        return datetime.fromisocalendar(
            int.from_bytes(col[0:2], byteorder='little', signed=False),
            int.from_bytes(col[2:3], byteorder='little', signed=False),
            int.from_bytes(col[3:4], byteorder='little', signed=False),
        )
    elif col_type == odbc_pb2.TIME:
        return datetime.time(
            int.from_bytes(col[0:1], byteorder='little', signed=False),
            int.from_bytes(col[1:2], byteorder='little', signed=False),
            int.from_bytes(col[2:3], byteorder='little', signed=False),
        )
    elif col_type == odbc_pb2.UUID:
        return uuid.UUID(bytes=col).__str__()
    raise Exception('')
