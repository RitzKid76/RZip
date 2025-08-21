from collections import deque


class Decompressor:

    @staticmethod
    def binary_to_int(input: str) -> int:
        return int(input, 2)

    @staticmethod
    def binary_to_char(input: str) -> str:
        return chr(Decompressor.binary_to_int(input))

    @staticmethod
    def read_n_bits(input: deque, n: int) -> str:
        return "".join(input.popleft() for _ in range(n))

    @staticmethod
    def extract_compressed_int(input: deque) -> int:
        size_binary = Decompressor.read_n_bits(input, 3)
        nibble_count = Decompressor.binary_to_int(size_binary) + 1

        size = nibble_count * 4
        value_binary = Decompressor.read_n_bits(input, size)

        return Decompressor.binary_to_int(value_binary)

    @staticmethod
    def huffman_table(bits: deque) -> dict[str, str]:
        output = {}

        while True:
            char_binary = Decompressor.read_n_bits(bits, 7)
            if char_binary == "0" * 7:
                break

            char = Decompressor.binary_to_char(char_binary)

            length = Decompressor.extract_compressed_int(bits)
            code = Decompressor.read_n_bits(bits, length)

            output[code] = char

        return output

    @staticmethod
    def bytes_to_bits(bytes: bytes) -> str:
        return "".join(format(byte, "08b") for byte in bytes)

    @staticmethod
    def deserialize(bits: deque, table: dict[str, str]) -> str:
        output = ""

        buffer = ""
        while bits:
            buffer += bits.popleft()

            if buffer not in table:
                continue

            output += table[buffer]
            buffer = ""

        return output

    @staticmethod
    def decompress(input: bytes) -> str:
        bits = deque(Decompressor.bytes_to_bits(input))

        table = Decompressor.huffman_table(bits)

        return Decompressor.deserialize(bits, table)
