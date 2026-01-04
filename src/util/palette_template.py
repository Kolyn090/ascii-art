import os
import sys
import json
from writer import Writer
from PIL import ImageFont
from PIL.ImageFont import FreeTypeFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../nonfixed_width')))
from flow_writer import FlowWriter  # type: ignore

class PaletteTemplate:
    def __init__(self,
                 layer: int,
                 chars: list[str],
                 image_font: FreeTypeFont,
                 char_bound: tuple[int, int],
                 approx_ratio=1,
                 vector_top_k=1,
                 match_method='fast',
                 pad=(0, 0),
                 override_widths: dict[str, int] | None = None,
                 override_weights: dict[str, float] | None = None,
                 flow_match_method='fast',
                 binary_threshold=90):
        self.layer = layer
        self.chars = chars
        self.image_font = image_font
        self.char_bound = char_bound
        self.approx_ratio = approx_ratio
        self.vector_top_k = vector_top_k
        self.match_method = match_method
        self.override_widths = override_widths
        self.override_weights = override_weights
        self.flow_match_method=flow_match_method
        self.binary_threshold=binary_threshold
        self.pad = pad

    def create_writer(self, max_workers: int, antialiasing: bool) -> Writer:
        return Writer(
            image_font=self.image_font,
            max_workers=max_workers,
            char_bound=self.char_bound,
            approx_ratio=self.approx_ratio,
            match_method=self.match_method,
            vector_top_k=self.vector_top_k,
            chars=self.chars,
            override_widths=self.override_widths,
            override_weights=self.override_weights,
            antialiasing=antialiasing,
            pad=self.pad
        )

    def create_flow_writer(self, max_workers: int, antialiasing: bool) -> FlowWriter:
        return FlowWriter(
            chars=self.chars,
            char_bound=self.char_bound,
            override_widths=self.override_widths,
            image_font=self.image_font,
            pad=self.pad,
            flow_match_method=self.flow_match_method,
            binary_threshold=self.binary_threshold,
            override_weights=self.override_weights,
            antialiasing=antialiasing,
            max_workers=max_workers
        )

    @staticmethod
    def read_from_json(obj: dict):
        def read_must_have(key: str):
            if key in obj:
                return obj[key]
            raise Exception(f"Error: palette file item missing key '{key}'.")

        # Must-have fields
        chars = list(dict.fromkeys(c for c in read_must_have("chars") if c != '\n'))
        font = read_must_have("font")
        font_size = read_must_have("font_size")
        char_bound_width = read_must_have("char_bound_width")
        char_bound_height = read_must_have("char_bound_height")

        # Optional fields
        def read_optional(key: str, default):
            if key in obj:
                return obj[key]
            return default

        layer=read_optional("layer", 0)
        approx_ratio=read_optional("approx_ratio", 1)
        vector_top_k=read_optional("vector_top_k", 5)
        match_method=read_optional("match_method", 'fast')
        pad_width=read_optional("pad_width", 0)
        pad_height=read_optional("pad_height", 0)
        override_widths = None
        override_weights = None
        flow_match_method=read_optional("flow_match_method", 'fast')
        binary_threshold=read_optional("binary_threshold", 90)

        if "override_widths" in obj:
            override_widths = dict()
            for item in obj["override_widths"]:
                override_widths[item["char"]] = item["width"]
        if "override_weights" in obj:
            override_weights = dict()
            for item in obj["override_weights"]:
                override_weights[item["char"]] = item["weight"]

        return PaletteTemplate(
            layer=layer,
            chars=chars,
            image_font=ImageFont.truetype(font, int(font_size)),
            char_bound=(char_bound_width, char_bound_height),
            approx_ratio=approx_ratio,
            vector_top_k=vector_top_k,
            match_method=match_method,
            pad=(pad_width, pad_height),
            override_widths=override_widths,
            override_weights=override_weights,
            flow_match_method=flow_match_method,
            binary_threshold=binary_threshold
        )

    def __str__(self):
        chars = "".join(self.chars)
        return (f"Layer: {self.layer}, "
                f"Font: {self.image_font.getname()}, "
                f"Character Bound: {self.char_bound}, "
                f"Approximate Ratio: {self.approx_ratio}, "
                f"Vector Top K: {self.vector_top_k}, "
                f"Method: {self.match_method}, "
                f"Chars: {chars}, "
                f"Pad: {self.pad}, "
                f"Override Widths: {self.override_widths}, "
                f"Override Weights: {self.override_weights}")

def validate_palettes(palettes: list[PaletteTemplate]):
    # 1. Make sure all characters have the same valid cell height
    expected_char_bound_height = palettes[0].char_bound[1]
    expected_char_bound_height += palettes[0].pad[1] * 2
    for i in range(1, len(palettes)):
        palette = palettes[i]
        char_bound_height = palette.char_bound[1]
        char_bound_height += palette.pad[1] * 2
        if expected_char_bound_height != char_bound_height:
            raise Exception("Invalid Palette: Not all characters have the same valid cell height!")

    # 2. Make sure all values are valid
    def is_greater_than(expected, num):
        return num >= expected

    def is_strictly_greater_than(expected, num):
        return num > expected

    def is_within_range(bottom, top, num):
        return bottom <= num <= top

    comparison_error_msgs = [
        "Number of characters must be strictly greater than 0.",
        "Character bound width must be strictly greater than 0.",
        "Character bound height must be strictly greater than 0.",
        "Approximate ratio must be between 0 and 1.",
        "Vector Top K must be strictly greater than 0.",
        "Binary threshold must be greater than or equal to 0."
    ]

    for palette in palettes:
        comparisons = [
            is_strictly_greater_than(0, len(palette.chars)),
            is_strictly_greater_than(0, palette.char_bound[0]),
            is_strictly_greater_than(0, palette.char_bound[1]),
            is_within_range(0, 1, palette.approx_ratio),
            is_strictly_greater_than(0, palette.vector_top_k),
            is_greater_than(0, palette.binary_threshold)
        ]
        for i in range(len(comparisons)):
            comparison = comparisons[i]
            if not comparison:
                raise Exception(f"Invalid Palette: {comparison_error_msgs[i]}.")

    # Add more rules in the future...

    print("All tests passed for palettes.")

def are_palettes_fixed_width(palettes: list[PaletteTemplate]) -> bool:
    if len(palettes) == 0:
        return True

    # Assume heights are already the same, so don't check for that

    # Trying to find a reference width
    palette0 = palettes[0]
    char_bound_width = palette0.char_bound[0]
    if palette0.override_widths is not None:
        for char, width in palette0.override_widths.items():
            if width > 0:
                char_bound_width = width
                break
    char_bound_width += 2 * palette0.pad[0]  # Use this as the standard width
    for palette in palettes:
        curr_width = palette.char_bound[0] + 2 * palette.pad[0]
        if palette.override_widths is None:
            if curr_width != char_bound_width:
                return False
        else:
            for char, curr_width in palette.override_widths.items():
                if curr_width <= 0:
                    return False
                else:
                    width = curr_width + 2 * palette.pad[0]
                    if width != char_bound_width:
                        return False
    return True

def test():
    palette_path = '../../resource/palette_files/jx_files/palette_test.json'
    with open(palette_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
        name = content["name"]
        templates = content["templates"]
        print(f"Reading palette from {name}.")
        palettes = []
        for template in templates:
            palette = PaletteTemplate.read_from_json(template)
            palettes.append(palette)
            print(palette)

    validate_palettes(palettes)

def test_invalid():
    palette_path = '../../resource/palette_files/jx_files/palette_invalid.json'
    with open(palette_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
        name = content["name"]
        templates = content["templates"]
        print(f"Reading palette from {name}.")
        palettes = []
        for template in templates:
            palette = PaletteTemplate.read_from_json(template)
            palettes.append(palette)

    validate_palettes(palettes)

def test_are_fixed_width():
    from pathlib import Path
    path = "../../resource/palette_files"
    json_files = list(Path(path).rglob("*.json"))
    for palette_path in json_files:
        with open(palette_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
            templates = content["templates"]
            palettes = []
            for template in templates:
                palette = PaletteTemplate.read_from_json(template)
                palettes.append(palette)
            are_fixed = are_palettes_fixed_width(palettes)
            msg = "fixed" if are_fixed else "not fixed"
            print(f"{palette_path} is {msg}.")

if __name__ == '__main__':
    test()
