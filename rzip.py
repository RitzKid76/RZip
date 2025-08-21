from .compressor import Compressor
from .decompressor import Decompressor

class RZip:

    @staticmethod
    def read_file(file: str) -> str:
        with open(file) as f:
            compressed = f.read()

        return Decompressor.decompress(compressed)
    
    @staticmethod
    def write_file(file: str, contents: str) -> None:
        compressed = Compressor.compress(contents)

        with open(file, "wb") as f:
            f.write(compressed)