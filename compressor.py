import math
from .huffman_node import HuffmanNode


class Compressor:

    @staticmethod
    def char_frequencies(input: str) -> list[HuffmanNode]:
        counts = {}

        for char in input:
            if char not in counts:
                counts[char] = 0

            counts[char] += 1

        return [HuffmanNode.from_char(char, frequency) for (char, frequency) in counts.items()]

    @staticmethod
    def huffman_tree(nodes: list[HuffmanNode]) -> HuffmanNode:
        while len(nodes) > 1:
            nodes = sorted(nodes, key=lambda node: node.frequency)

            left = nodes.pop(0)
            right = nodes.pop(0)

            new = HuffmanNode.from_children(left, right)
            nodes.append(new)

        return nodes[0]

    @staticmethod
    def huffman_table(tree: HuffmanNode, prefix: str = "", table: dict[str, str] = {}) -> dict[str, str]:
        if tree.char is not None:
            table[tree.char] = prefix
            return table

        if tree.left is not None:
            Compressor.huffman_table(tree.left, prefix + "0", table)

        if tree.right is not None:
            Compressor.huffman_table(tree.right, prefix + "1", table)

        return table

    @staticmethod
    def bits_to_bytes(bits: str) -> bytes:
        output = bytearray()

        for i in range(0, len(bits), 8):
            chunk = bits[i: i+8]
            chunk = chunk.ljust(8, "0")

            output.append(int(chunk, 2))

        return bytes(output)

    @staticmethod
    def byte_to_binary(input: int) -> str:
        return format(input, "08b")

    @staticmethod
    def int_to_binary(input: int) -> str:
        if input == 0:
            return "0" * 7

        bit_count = input.bit_length()
        nibble_count = math.ceil(bit_count / 4)

        padded_bit_count = nibble_count * 4

        size = nibble_count - 1
        value = format(input, f"0{padded_bit_count}b")

        return f"{format(size, '03b')}{value}"

    @staticmethod
    def char_to_binary(input: str) -> str:
        return "".join(format(ord(input), "07b"))

    @staticmethod
    def serialize_table(table: dict[str, str]) -> str:
        serialized = ""

        for char, code in table.items():
            serialized += Compressor.char_to_binary(char)

            serialized += Compressor.int_to_binary(len(code))
            serialized += code

        return serialized

    @staticmethod
    def serialize(input: str, table: dict[str, str]) -> bytes:
        bits = ""

        bits += Compressor.serialize_table(table)
        bits += "0" * 7

        for char in input:
            bits += table[char]

        return Compressor.bits_to_bytes(bits)

    @staticmethod
    def compress(input: str) -> bytes:
        if any(ord(char) >= 128 for char in input):
            raise ValueError("input is not rzip compressible")

        nodes = Compressor.char_frequencies(input)
        tree = Compressor.huffman_tree(nodes)
        table = Compressor.huffman_table(tree)

        return Compressor.serialize(input, table)
