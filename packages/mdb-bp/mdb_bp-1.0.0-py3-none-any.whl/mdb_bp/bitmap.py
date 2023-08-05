BYTE = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7


class Bitmap:
    def __init__(self, b: bytes):
        self.bytes = b

    def get(self, index: int) -> 0 | 1:
        # grab the bit at the desired index
        assert len(self.bytes) * 8 > index, 'Index out of bounds'
        # raise ValueError('Index ')

        # Grab the value and return
        return self.get_bit_from_byte(int(index / 8), index % 8)

    def get_bit_from_byte(self, byte: BYTE, bit: int) -> 0 | 1:
        assert len(self.bytes) > byte, 'byte is out of bounds'
        assert 0 <= bit < 8, 'bit is out of range [0, 8)'

        if self.bytes[byte] & (1 << int(bit)) == 0:
            return 0
        return 1

    def set(self, index: int, val: 0 | 1):
        # set the bit at the given index
        assert len(self.bytes) * 8 > index, 'Index out of bounds'

        self.set_bit_in_byte(int(index / 8), index % 8, val)

    def set_bit_in_byte(self, byte: BYTE, bit: int, val: 0 | 1):
        assert len(self.bytes) > byte, 'byte is out of bounds'
        assert 0 <= bit < 8, 'bit is out of range [0, 8)'

        mask = 1 << bit
        if val == 0:
            self.bytes[byte] = self.bytes[byte] & (~ mask)
        elif val == 1:
            self.bytes[byte] = self.bytes[byte] | mask
