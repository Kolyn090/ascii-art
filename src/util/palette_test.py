from arg_util import ShadeArgUtil

def test():
    palettes = ShadeArgUtil.get_palette_json("../../resource/palette_files/jx_files/palette_test.json")
    for palette in palettes:
        print(palette)

if __name__ == '__main__':
    test()
