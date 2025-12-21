import os
import numpy as np

from writer import PositionalCharTemplate, CharTemplate
from color_util import PositionalColor

class FontEssential:
    def __init__(self,
                 font_name: str,
                 font_size: int,
                 char_bound: tuple[int, int]):
        self.font_name = font_name
        self.font_size = font_size
        self.char_bound = char_bound

    def __eq__(self, other):
        return isinstance(other, FontEssential) and \
            (self.font_name, self.font_size, self.char_bound) == \
            (other.font_name, other.font_size, other.char_bound)

    def __hash__(self):
        return hash((self.font_name, self.font_size, self.char_bound))

    def __str__(self):
        return f"{{[Font Name]: {self.font_name}, [Font Size]: {self.font_size}, [Character Bound]: {self.char_bound}}}"

class AsciiWriter:
    def __init__(self,
                 p_cts: list[PositionalCharTemplate],
                 p_cs: list[PositionalColor],
                 width: int, save_path=''):
        self.p_cts = p_cts
        self.p_cs = p_cs
        self.width = width
        self.save_path = save_path
        p_cts.sort(key=lambda x: (x.top_left[1], x.top_left[0]))
        self.output_folder = 'ascii_output'
        self.chars_file = 'chars.txt'
        self.color_file = 'color.txt'
        self.pos_file = 'position.txt'
        self.font_file = 'font.txt'
        self.font_table_split = "<><>"

    def save(self):
        if not os.path.exists(self.save_path):
            print("ASCII Writer: Invalid save path, abort.")
        output_path = os.path.join(self.save_path, self.output_folder)
        os.makedirs(output_path, exist_ok=True)
        chars_path = os.path.join(output_path, self.chars_file)
        self._save_ascii(chars_path)

        color_path = os.path.join(output_path, self.color_file)
        self._save_color(color_path)

        pos_path = os.path.join(output_path, self.pos_file)
        self._save_top_left_position(pos_path)

        font_path = os.path.join(output_path, self.font_file)
        self._save_font(font_path)

    def _save_ascii(self, chars_path: str):
        content = self._get_2d_chars()
        with open(chars_path, "w", encoding="utf-8") as f:
            for row in content:
                f.write("".join(row) + "\n")

    def _get_2d_chars(self) -> list[list[str]]:
        chars = [p_ct.char_template.char for p_ct in self.p_cts]
        return [chars[i:i + self.width] for i in range(0, len(chars), self.width)]

    def _save_color(self, color_path: str):
        content = self._get_2d_color()
        with open(color_path, "w", encoding="utf-8") as f:
            for row in content:
                f.write(",".join(row) + "\n")

    def _get_2d_color(self) -> list[list[str]]:
        table: dict[int: list[PositionalColor]] = dict()
        for p_c in self.p_cs:
            y = p_c.top_left[1]
            if y not in table:
                table[y] = []
            table[y].append(p_c)
        result = []
        for _, p_cs in table.items():
            row = []
            for p_c in p_cs:
                row.append(f"{p_c.color}")
            result.append(row)
        return result

    def _save_top_left_position(self, pos_path):
        content = self._get_2d_top_left_position()
        with open(pos_path, "w", encoding="utf-8") as f:
            for row in content:
                f.write(",".join(row) + "\n")

    def _get_2d_top_left_position(self) -> list[list[str]]:
        table: dict[int: list[PositionalColor]] = dict()
        for p_ct in self.p_cts:
            y = p_ct.top_left[1]
            if y not in table:
                table[y] = []
            table[y].append(p_ct)
        result = []
        for _, p_cts in table.items():
            row = []
            for p_ct in p_cts:
                row.append(f"{np.array(p_ct.top_left)}")
            result.append(row)
        return result

    def _save_font(self, font_path: str):
        font_table, font_2d_indices = self._get_2d_font_table()
        result = []
        # 1. Save the font table in the first line
        line1 = []
        for font_ess, index in font_table.items():
            line1.append(f"{str(font_ess)}: {index}")
        result.append(self.font_table_split.join(line1))

        # 2. Save the indices
        for row in font_2d_indices:
            result.append("".join([str(item) for item in row]))
        with open(font_path, "w", encoding="utf-8") as f:
            for row in result:
                f.write("".join(row) + "\n")

    def _get_2d_font_table(self) -> tuple[dict[FontEssential, int], list[list[int]]]:
        """

        :return: A tuple of items.
        1. A table with key=font info, value=index
        2. A 2d list of indices, each indicate the font that the template is using
        """
        def get_font_essential(positional_ct: PositionalCharTemplate) -> FontEssential:
            return FontEssential(
                font_name=" ".join(positional_ct.char_template.image_font.getname()),
                font_size=int(positional_ct.char_template.image_font.size),
                char_bound=positional_ct.char_template.char_bound
            )

        # First item
        font_table: dict[FontEssential, int] = dict()
        font_index = 0

        # Second item
        font_2d_indices: dict[int, list[int]] = dict()

        for p_ct in self.p_cts:
            font_essential = get_font_essential(p_ct)
            if font_essential not in font_table:
                font_table[font_essential] = font_index
                font_index += 1

            y = p_ct.top_left[1]
            if y not in font_2d_indices:
                font_2d_indices[y] = []
            font_2d_indices[y].append(font_table[font_essential])
        return font_table, list(font_2d_indices.values())

def test():
    p_ct1 = PositionalCharTemplate(
        CharTemplate('a', None, None, None, None),
        (13, 22)
    )
    p_ct2 = PositionalCharTemplate(
        CharTemplate('b', None, None, None, None),
        (0, 22)
    )
    p_ct3 = PositionalCharTemplate(
        CharTemplate('c', None, None, None, None),
        (13, 0)
    )
    p_ct4 = PositionalCharTemplate(
        CharTemplate('d', None, None, None, None),
        (0, 0)
    )
    p_cts = [p_ct1, p_ct2, p_ct3, p_ct4]
    ascii_writer = AsciiWriter(p_cts, [],1)
    for p_ct in ascii_writer.p_cts:
        print(p_ct)
    print(ascii_writer._get_2d_chars())

    ascii_writer = AsciiWriter(p_cts, [],2, './')
    print(ascii_writer._get_2d_chars())
    ascii_writer.save()

if __name__ == '__main__':
    test()
