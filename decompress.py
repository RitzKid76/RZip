from collections import deque


def binary_to_int(input: str) -> int:
    return int(input, 2)


def binary_to_char(input: str) -> str:
    return chr(binary_to_int(input))


def read_n_bits(input: deque, n: int) -> str:
    return "".join(input.popleft() for _ in range(n))


def extract_compressed_int(input: deque) -> int:
    size_binary = read_n_bits(input, 3)
    nibble_count = binary_to_int(size_binary) + 1

    size = nibble_count * 4
    value_binary = read_n_bits(input, size)

    return binary_to_int(value_binary)


def huffman_table(bits: deque) -> dict[str, str]:
    output = {}

    while True:
        char_binary = read_n_bits(bits, 7)
        if char_binary == "0" * 7:
            break

        char = binary_to_char(char_binary)

        length = extract_compressed_int(bits)
        code = read_n_bits(bits, length)

        output[code] = char

    return output


def bytes_to_bits(bytes: bytes) -> str:
    return "".join(format(byte, "08b") for byte in bytes)


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


def decompress(input: str, output: str):
    with open(input, "rb") as f:
        bits = deque(bytes_to_bits(f.read()))

    table = huffman_table(bits)

    deserialized = deserialize(bits, table)
    with open(output, "w") as f:
        f.write(deserialized)


if __name__ == "__main__":
    decompress("compressed", "output.txt")
