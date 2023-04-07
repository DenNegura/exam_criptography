import struct
from print_bits import TransformBits as tb


class MD4:
    """An implementation of the MD4 hash algorithm."""

    width = 32
    mask = 0xFFFFFFFF

    # Unlike, say, SHA-1, MD4 uses little-endian. Fascinating!
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]

    def __init__(self, msg=None):
        print("ШАГ 1. Добавление недостающих битов.")
        """:param ByteString msg: The message to be hashed."""
        if msg is None:
            msg = b""

        self.msg = msg
        print('Исходное сообщение : ', msg)
        print('Исходное сообщение в битах : ', tb.transform(msg, tb.BIT))
        to_msg = msg
        # Pre-processing: Total length is a multiple of 512 bits.
        ml = len(msg) * 8
        msg += b"\x80"
        msg += b"\x00" * (-(len(msg) + 8) % 64)
        print('Добавляем биты в конец : 1 + 0 в количестве', (len(msg) - len(to_msg)) * 8 - 1)
        msg += struct.pack("<Q", ml)
        print('Добавляем биты длины в конец : ', tb.transform(struct.pack("<Q", ml)))

        print('\nШАГ 2. Инициализация MD-буфера.')
        print('MD-буфер: A = 0x67452301, B = 0xEFCDAB89, C = 0x98BADCFE, D = 0x10325476')
        print('\nШАГ 3. Обработка сообщения блоками по 16 слов.')
        print('F(X, Y, Z) = XY | !XZ')
        print('G(X, Y, Z) = XY | XZ | YZ')
        print('H(X, Y, Z) = X ^ Y ^ Z')
        # Process the message in successive 512-bit chunks.
        chunks = [msg[i: i + 64] for i in range(0, len(msg), 64)]
        print('разбиваем сообщение на части, кратные 512. Всего: ', len(chunks))
        self._process(chunks)

    def __repr__(self):
        if self.msg:
            return f"{self.__class__.__name__}({self.msg:s})"
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return self.hexdigest()

    def __eq__(self, other):
        return self.h == other.h

    def bytes(self):
        """:return: The final hash value as a `bytes` object."""
        return struct.pack("<4L", *self.h)

    def hexbytes(self):
        """:return: The final hash value as hexbytes."""
        return self.hexdigest().encode

    def hexdigest(self):
        """:return: The final hash value as a hexstring."""
        return "".join(f"{value:02x}" for value in self.bytes())

    def _process(self, chunks):
        num_chunk = 1
        for chunk in chunks:
            print(f'Обрабатываем блок {num_chunk} из 16-ти слов по 32 бита:')
            X, h = list(struct.unpack("<16I", chunk)), self.h.copy()
            chink_bin = tb.bytes_to_bits(chunk)
            X_bin = [chink_bin[x * 32: (x + 1) * 32] for x in range(16)]
            for i in range(len(X)):
                print(f'Слово X[{i + 1}]:  ', tb.separate(X_bin[i]))

            # transform print
            tp = lambda x: tb.separate(tb.add_bits(x, 32))
            # later position

            def lp(x, s, round):
                msg = '['
                if s == 3:
                    msg += 'abcd '
                elif s in [5, 7] or k == 9 and round == 2:
                    msg += 'dabc '
                elif s in [11, 9, 11]:
                    msg += 'cdab '
                else:
                    msg += 'bcda '
                msg += str(x) + ' ' + str(s) + ']'
                return msg + (12 - len(msg)) * ' '

            # Round 1.
            print('Раунд 1. Операция: a = (a + F(b, c, d) + X[k]) << s')

            Xi = [3, 7, 11, 19]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = n, Xi[n % 4]
                a, b, c, d, xk = h[i], h[j], h[k], h[l], X[k]
                hn = h[i] + MD4.F(h[j], h[k], h[l]) + X[K]
                h[i] = MD4.lrot(hn & MD4.mask, S)
                a2 = h[i]
                print(f'{n + 1}) {lp(n, S, 1)} :{tp(a2)} = ({tp(a)} + (({tp(b)} & {tp(c)}) '
                      f'| (~{tp(b)} & {tp(d)})) + {tp(xk)}) << {S}')

            # Round 2.
            print('\n\n\nРаунд 2. Операция: a = (a + G(b, c, d) + X[k] + 0x5A827999) << s')
            Xi = [3, 5, 9, 13]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = n % 4 * 4 + n // 4, Xi[n % 4]
                a, b, c, d, xk = h[i], h[j], h[k], h[l], X[k]
                hn = h[i] + MD4.G(h[j], h[k], h[l]) + X[K] + 0x5A827999
                h[i] = MD4.lrot(hn & MD4.mask, S)
                a2 = h[i]
                print(f'{n + 1})\t{tp(a2)} = ({tp(a)} + '
                      f'({tp(b)} & {tp(c)}) | ({tp(b)} & {tp(d)}) | ({tp(c)} & {tp(d)} + 0x5A827999) << {S}')

            # Round 3.
            print('\n\n\nРаунд 3. Операция: a = (a + H(b, c, d) + X[k] + 0x6ED9EBA1) << s')
            Xi = [3, 9, 11, 15]
            Ki = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = Ki[n], Xi[n % 4]
                a, b, c, d, xk = h[i], h[j], h[k], h[l], X[k]
                hn = h[i] + MD4.H(h[j], h[k], h[l]) + X[K] + 0x6ED9EBA1
                h[i] = MD4.lrot(hn & MD4.mask, S)
                a2 = h[i]
                print(f'{n + 1})\t{tp(a2)} = ({tp(a)} + ({tp(b)} ^ {tp(c)} ^ {tp(d)}) + 0x6ED9EBA1) << {S}')

            print('\n\nКонкатенация значений')
            self.h = [((v + n) & MD4.mask) for v, n in zip(self.h, h)]

    @staticmethod
    def F(x, y, z):
        return (x & y) | (~x & z)

    @staticmethod
    def G(x, y, z):
        return (x & y) | (x & z) | (y & z)

    @staticmethod
    def H(x, y, z):
        return x ^ y ^ z

    @staticmethod
    def lrot(value, n):
        lbits, rbits = (value << n) & MD4.mask, value >> (MD4.width - n)
        return lbits | rbits


def main():
    # Import is intentionally delayed.
    import sys

    if len(sys.argv) > 1:
        messages = [msg.encode() for msg in sys.argv[1:]]
        for message in messages:
            print(MD4(message).hexdigest())
    else:
        messages = [b"The quick brown fox jumps over the lazy dog"]
        known_hashes = [
            "1bee69a46ba811185c194762abaeae90",
        ]

        print("Testing the MD4 class.")
        print()

        for message, expected in zip(messages, known_hashes):
            # print("Message: ", message)
            # print("Expected:", expected)
            print("Actual:  ", MD4(message).hexdigest())
            print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
