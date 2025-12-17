from writer import Writer
from PIL.ImageFont import FreeTypeFont

class PaletteTemplate:
    def __init__(self,
                 layer: int,
                 chars: list[str],
                 imageFont: FreeTypeFont,
                 char_bound: tuple[int, int],
                 approx_ratio: float,
                 vector_top_k: int,
                 get_most_similar_method: str):
        self.layer = layer
        self.chars = chars
        self.imageFont = imageFont
        self.char_bound = char_bound
        self.approx_ratio = approx_ratio
        self.vector_top_k = vector_top_k
        self.get_most_similar_method = get_most_similar_method

    def create_writer(self) -> Writer:
        result = Writer()
        return result

    def __str__(self):
        chars = "".join(self.chars)
        return (f"Layer: {self.layer}, "
                f"Font: {self.imageFont.getname()}, "
                f"Character Bound: {self.char_bound}, "
                f"Approximate Ratio: {self.approx_ratio}, "
                f"Vector Top K: {self.vector_top_k}, "
                f"Method: {self.get_most_similar_method}, "
                f"Chars: {chars} ")
