import os
import sys
import numpy as np
from concurrent.futures import ThreadPoolExecutor

from gradient_divide import divide

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../util')))
from static import invert_image  # type: ignore
from char_template import CharTemplate, PositionalCharTemplate  # type: ignore
from slicer import Slicer  # type: ignore
from palette_template import PaletteTemplate  # type: ignore

class GradientWriter:
    def __init__(self,
                 templates: list[PaletteTemplate],
                 max_workers: int,
                 antialiasing: bool):
        self.templates = templates
        self.max_workers = max_workers
        self.gradient_imgs: list[np.ndarray] = []
        self.char_rank: dict[str, int] = dict()
        self.antialiasing = antialiasing

        self.writer = None  # Only useful for fixed-width case

    def assign_gradient_imgs(self, img_gray: np.ndarray, thresholds_gamma: float):
        self.gradient_imgs = divide(img_gray, len(self.templates), thresholds_gamma)

    def match(self) -> tuple[np.ndarray, list[PositionalCharTemplate]]:
        p_ct_lists: list[list[PositionalCharTemplate]] = []
        h, w = 0, 0
        for i in range(len(self.templates)):
            template = self.templates[i]
            writer = template.create_writer(self.max_workers, self.antialiasing)
            img = self.gradient_imgs[i]
            img = invert_image(img)
            slicer = Slicer()
            padded_char_bound = self._make_padded_char_bound(self.templates[i].char_bound,
                                                             (
                                                                 template.pad_top,
                                                                 template.pad_bottom,
                                                                 template.pad_left,
                                                                 template.pad_right
                                                             ))
            cells = slicer.slice(img, padded_char_bound)
            matched_img, p_cts = writer.match_cells(cells)
            self.writer = writer
            h, w = matched_img.shape[:2]
            p_ct_lists.append(p_cts)

        stacks = self.stack(p_ct_lists)
        return self.stack_to_img(stacks, w, h), stacks

    @staticmethod
    def _make_padded_char_bound(char_bound: tuple[int, int],
                                pad: tuple[int, int, int, int]) -> tuple[int, int]:
        return char_bound[0] + pad[2] + pad[3], char_bound[1] + pad[0] + pad[1]

    def stack_to_img(self, p_cts: list[PositionalCharTemplate], w: int, h: int) \
            -> np.ndarray:
        stacks = p_cts
        result_img = np.zeros((h, w, 3), dtype=np.uint8)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            list(executor.map(lambda cell: self._paste_to_img(cell, result_img, self.antialiasing), stacks))

        result_img = invert_image(result_img)
        # large_char_bound = self.get_large_char_bound()
        # result_img = result_img[0:math.floor(h / large_char_bound[1]) * large_char_bound[1],
        #              0:math.floor(w / large_char_bound[0]) * large_char_bound[0]]
        return result_img

    def get_large_char_bound(self) -> tuple[int, int]:
        if self.writer is not None:
            return self.writer.char_templates[0].char_bound
        return -1, -1

    @staticmethod
    def _paste_to_img(p_ct: PositionalCharTemplate, result_img: np.ndarray, antialiasing: bool):
        if antialiasing:
            template = p_ct.char_template.img
        else:
            template = p_ct.char_template.img_binary
        top_left = p_ct.top_left
        # bottom_right_y = top_left[1] + template.shape[0]
        # bottom_right_x = top_left[0] + template.shape[1]

        # bottom_right_y = top_left[1] + template.shape[0]
        # bottom_right_x = top_left[0] + template.shape[1]

        # template: (H, W) or (H, W, 3)
        cell_h, cell_w = template.shape[:2]

        # ensure template has 3 channels
        if template.ndim == 2:  # grayscale
            template_to_paste = np.stack([template] * 3, axis=-1)
        elif template.ndim == 3 and template.shape[2] == 3:  # already RGB
            template_to_paste = template
        else:
            raise ValueError(f"Unsupported template shape: {template.shape}")

        # paste into result_img
        result_img[top_left[1]:top_left[1] + cell_h, top_left[0]:top_left[0] + cell_w] = template_to_paste

    def stack(self, p_ct_lists: list[list[PositionalCharTemplate]]) -> list[PositionalCharTemplate]:
        self._assign_template_rank()
        table: dict[tuple[int, int], CharTemplate] = dict()
        for p_ct_list in reversed(p_ct_lists):
        # for p_ct_list in p_ct_lists:
            for p_ct in p_ct_list:
                char_template = p_ct.char_template
                top_left = p_ct.top_left
                self._add_to_table(table, top_left, char_template)

        result = []
        for top_left, char_template in table.items():
            p_ct = PositionalCharTemplate(char_template, top_left)
            result.append(p_ct)
        return result

    def _add_to_table(self, table: dict[tuple[int, int], CharTemplate],
                      top_left: tuple[int, int],
                      char_template: CharTemplate):
        if top_left in table:
            # Prioritize the character in the lower rank (0 is the highest rank)
            if self._compare_template_char(char_template.char, table[top_left].char):
                table[top_left] = char_template
        else:
            table[top_left] = char_template

    def _compare_template_char(self, tc1: str, tc2: str) -> bool:
        """
        Compare two template chars.

        :param tc1: template char 1
        :param tc2: template char 2
        :return: Return True if tc1 has lower rank in templates.
        Otherwise, False.
        """
        return self.char_rank[tc1] > self.char_rank[tc2]

    def _assign_template_rank(self):
        count = 0
        for template in self.templates:
            for char in template.chars:
                self.char_rank[char] = count
                count += 1
        # Force space to have the guaranteed highest rank
        self.char_rank[" "] = -1
