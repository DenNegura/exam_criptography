import bitstring


class TransformBits:
    HEX = 'hex'

    BIT = 'bit'

    SEPARATOR = ' '

    def __init__(self, sep=SEPARATOR, sys=BIT):
        if sys == TransformBits.HEX:
            self.__default = sys
            self.__separator = sep
        else:
            self.__default = TransformBits.BIT
            self.__separator = sep

    def get_sys_default(self):
        return self.__default

    def separate(self, msg, sep=SEPARATOR, sys=BIT):
        if sep == TransformBits.SEPARATOR:
            sep = self.__separator

        bits_list = [msg[i:i + 8] for i in range(0, len(msg), 8)]
        if sys == TransformBits.HEX \
                or self.__default == TransformBits.HEX:
            bytes_list = [x if len(x) == 2 else '0' + x for x in
                          [hex(int(x, 2))[2:] for x in bits_list]]
            return sep.join(bytes_list)
        return sep.join(bits_list)

    def bytes_to_bits(self, msg):
        return bitstring.BitArray(msg).bin

    def str_to_bits(self, msg):
        return ''.join([format(ord(ch), '08b') for ch in msg])

    def transform(self, msg, sep=' ',  sys=BIT) -> str:
        if type(msg) is bytes:
            return self.separate(msg=self.bytes_to_bits(msg), sep=sep, sys=sys)
        elif type(msg) is str:
            return self.separate(msg=self.str_to_bits(msg), sep=sep, sys=sys)
        return ''

    def to_bin(self, msg, msg_type=BIT):
        if msg_type == TransformBits.HEX:
            return bin(int(msg, 16))[2:]
        return bin(msg)[2:]

    def add_bits(self, msg, bits_count):
        if type(msg) is int:
            msg = self.to_bin(msg)
        return ('0' * (bits_count - len(msg))) + msg
