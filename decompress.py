from collections import deque


def binary_to_int(input: str) -> int:
    return int(input, 2)


def binary_to_string(input: str) -> str:
    return chr(binary_to_int(input))


def read_n_bits(input: deque, n: int) -> str:
    return "".join(input.popleft() for _ in range(n))


def huffman_table(bits: deque) -> dict[str, str]:
    output = {}

    while True:
        char_binary = read_n_bits(bits, 8)
        if char_binary == "00000000":
            break

        char = binary_to_string(char_binary)

        length_binary = read_n_bits(bits, 32)
        length = binary_to_int(length_binary)

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
