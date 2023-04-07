import bitstring


class TransformBits:
    BYTE = 'byte'

    BIT = 'bit'

    def separate(self, msg, sys=BIT):
        bits_list = [msg[i:i + 8] for i in range(0, len(msg), 8)]
        if sys == TransformBits.BYTE:
            bytes_list = [int(x, 2) for x in bits_list]
            return bytes(bytes_list)
        return ' '.join(bits_list)

    def bytes_to_bits(self, msg):
        return bitstring.BitArray(msg).bin

    def str_to_bits(self, msg):
        return ''.join([format(ord(ch), '08b') for ch in msg])

    def transform(self, msg, sys=BIT) -> str:
        if type(msg) is bytes:
            return self.separate(self.bytes_to_bits(msg), sys)
        elif type(msg) is str:
            return self.separate(self.str_to_bits(msg), sys)
        return ''

    def to_bin(self, msg):
        return bin(msg)[2:]

    def add_bits(self, msg, bits_count):
        if type(msg) is int:
            msg = self.to_bin(msg)
        return ('0' * (bits_count - len(msg))) + msg


tb = TransformBits()
byte = tb.transform('10000000', tb.BYTE)
print(hex(int('10000000', 2)))