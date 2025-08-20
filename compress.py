import math
from huffman_node import HuffmanNode


def char_frequencies(input: str) -> list[HuffmanNode]:
    counts = {}

    for char in input:
        if char not in counts:
            counts[char] = 0

        counts[char] += 1

    return [HuffmanNode.from_char(char, frequency) for (char, frequency) in counts.items()]


def huffman_tree(nodes: list[HuffmanNode]) -> HuffmanNode:
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda node: node.frequency)

        left = nodes.pop(0)
        right = nodes.pop(0)

        new = HuffmanNode.from_children(left, right)
        nodes.append(new)

    return nodes[0]


def huffman_table(tree: HuffmanNode, prefix: str = "", table: dict[str, str] = {}) -> dict[str, str]:
    if tree.char is not None:
        table[tree.char] = prefix
        return table

    if tree.left is not None:
        huffman_table(tree.left, prefix + "0", table)

    if tree.right is not None:
        huffman_table(tree.right, prefix + "1", table)

    return table


def bits_to_bytes(bits: str) -> bytes:
    output = bytearray()

    for i in range(0, len(bits), 8):
        chunk = bits[i: i+8]
        chunk = chunk.ljust(8, "0")

        output.append(int(chunk, 2))

    return bytes(output)


def byte_to_binary(input: int) -> str:
    return format(input, "08b")


def int_to_binary(input: int) -> str:
    if input == 0:
        return "0" * 7

    bit_count = input.bit_length()
    nibble_count = math.ceil(bit_count / 4)

    padded_bit_count = nibble_count * 4

    size = nibble_count - 1
    value = format(input, f"0{padded_bit_count}b")

    return f"{format(size, '03b')}{value}"


def char_to_binary(input: str) -> str:
    return "".join(format(ord(input), "07b"))


def serialize_table(table: dict[str, str]) -> str:
    serialized = ""

    for char, code in table.items():
        serialized += char_to_binary(char)

        serialized += int_to_binary(len(code))
        serialized += code

    return serialized


def serialize(input: str, table: dict[str, str]) -> bytes:
    bits = ""

    bits += serialize_table(table)
    bits += "0" * 7

    for char in input:
        bits += table[char]

    return bits_to_bytes(bits)


def clean_to_ascii(input: str) -> str:
    return "".join(char for char in input if ord(char) < 128)


def compress(input: str, output: str):
    with open(input) as f:
        contents: str = clean_to_ascii(f.read())

    nodes = char_frequencies(contents)
    tree = huffman_tree(nodes)
    table = huffman_table(tree)

    serialized = serialize(contents, table)
    with open(output, "wb") as f:
        f.write(serialized)


if __name__ == "__main__":
    compress("input.txt", "compressed")
