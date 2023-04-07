import bitstring


class TransformBits:

    BYTE = 'byte'

    BIT = 'bit'

    @staticmethod
    def separate(msg, sys=BIT):
        print(sys)
        # TO DO: в зависимости от sys переводить биты в байты, или оставить так
        return ' '.join([msg[i:i + 8] for i in range(0, len(msg), 8)])

    @staticmethod
    def bytes_to_bits(msg):
        return bitstring.BitArray(msg).bin

    @staticmethod
    def str_to_bits(msg):
        return ''.join([format(ord(ch), '08b') for ch in msg])

    @staticmethod
    def transform(msg, sys=BIT) -> str:
        if type(msg) is bytes:
            return TransformBits\
                .separate(TransformBits.bytes_to_bits(msg), sys)
        elif type(msg) is str:
            return TransformBits\
                .separate(TransformBits.str_to_bits(msg),sys)
        return ''

    @staticmethod
    def to_bin(msg):
        return bin(msg)[2:]

    @staticmethod
    def add_bits(msg, bits_count):
        if type(msg) is int:
            msg = TransformBits.to_bin(msg)
        return ('0' * (bits_count - len(msg))) + msg
