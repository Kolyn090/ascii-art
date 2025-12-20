import os.path

from writer import PositionalCharTemplate, CharTemplate
from color_util import PositionalColor

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
        self.output_folder = 'f_output'
        self.chars_file = 'chars.txt'
        self.color_file = 'color.txt'

    def save(self):
        if not os.path.exists(self.save_path):
            print("ASCII Writer: Invalid save path, abort.")
        output_path = self.get_output_path()
        os.makedirs(output_path, exist_ok=True)
        chars_path = os.path.join(output_path, self.chars_file)
        self._save_chars(chars_path)

        color_path = os.path.join(output_path, self.color_file)
        self._save_color(color_path)

    def get_output_path(self):
        return os.path.join(self.save_path, self.output_folder)

    def _save_chars(self, chars_path: str):
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
            y = p_c.position[1]
            if y not in table:
                table[y] = []
            table[y].append(p_c)
        result = []
        for _, p_cs in table.items():
            row = []
            for p_c in p_cs:
                row.append(f"{{{p_c.color}{p_c.position}}}")
            result.append(row)
        return result

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
