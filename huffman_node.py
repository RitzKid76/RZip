from __future__ import annotations


class HuffmanNode:

    def __init__(
        self,
        left: HuffmanNode = None,
        right: HuffmanNode = None,
        char: str = None,
        frequency: int = None
    ):
        self.left = left
        self.right = right
        self.char = char
        self.frequency = frequency

    @classmethod
    def from_char(cls, char: str, frequency: int):
        return cls(char=char, frequency=frequency)

    @classmethod
    def from_children(cls, left: "HuffmanNode", right: "HuffmanNode"):
        return cls(left=left, right=right, frequency=left.frequency + right.frequency)

    def get_bit(self, child: HuffmanNode) -> bool:
        if self.left == child:
            return False
        if self.right == child:
            return True

        raise IndexError(f"{child} doesnt exist {self.left, self.right}")

    def __str__(self):
        return f"[{self.char, self.frequency}, {self.left, self.right}]"

    def __repr__(self):
        return self.__str__()
