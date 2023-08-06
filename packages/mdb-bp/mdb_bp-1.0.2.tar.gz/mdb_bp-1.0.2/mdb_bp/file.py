import math
import os
import string

from mdb_bp.protocol_buffers.odbc_pb2 import StoreFileRequest


class BasicStoreFile:
    def __init__(self, auth, file_name: string, file_path: string, file_extension: string, package_size: int = 2500):
        self.auth = auth

        self.file_name = file_name
        self.file_path = file_path
        self.file_extension = file_extension
        self.package_size = package_size

        self.file_reader = open(file_path, "rb")

        self.file_size = os.path.getsize(file_path)

        self.index = 0
        self.total_bits = math.ceil(self.file_size / self.package_size)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.total_bits:
            # Read the next set of bytes
            file_bit_bytes = self.file_reader.read(
                self.package_size if self.index < self.total_bits - 1
                else self.file_size % self.package_size
            )

            # Create the request
            req = StoreFileRequest(
                auth=self.auth,

                file_name=self.file_name,
                file_extension=self.file_extension,
                file_size=self.file_size,

                file_bit_id=self.index,
                file_bit_size=self.package_size,
                file_bit_bytes=file_bit_bytes,
            )

            # Increment position
            self.index += 1

            # return the request
            return req

        # If there is no next, stop the iterator
        raise StopIteration

    def generator(self):
        for resp in self:
            yield resp
