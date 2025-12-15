import numpy as np

from static import resize_nearest_neighbor, resize_bilinear

class TraceArgUtil:
    @staticmethod
    def get_chars(code: str) -> list[str]:
        match code:
            case 'ascii':
                return TraceArgUtil._get_all_ascii()
            case 'file':
                return TraceArgUtil._get_from_file()
        return []

    @staticmethod
    def _get_all_ascii() -> list[str]:
        return [chr(i) for i in range(128)]

    @staticmethod
    def _get_from_file() -> list[str]:
        file = '../trace/chars_file.txt'
        with open(file, 'r', encoding='utf-8') as f:
            return list(dict.fromkeys(c for c in f.read() if c != '\n'))

    @staticmethod
    def resize(code: str, img: np.ndarray, factor: int) -> np.ndarray:
        match code:
            case 'nearest_neighbor':
                return resize_nearest_neighbor(img, factor)
            case 'bilinear':
                return resize_bilinear(img, factor)
        return resize_nearest_neighbor(img, factor)
