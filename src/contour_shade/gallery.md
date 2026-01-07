# Gallery (Contour Shade ASCII Filter)

1️⃣ `cd` to `src/contour_shade`.

---

<p align="center">
    <img src="../../resource/gallery/contour_shade/gpe_colored.png" width="400">
</p>

```commandline
python contour_shade.py ^
--image_path ../../resource/imgs/girl_with_pearl_earring.jpg ^
--resize_factor 4 ^
--color_option original ^
--contrast_factor 2 ^
--thresholds_gamma 5
```

---

<p align="center">
    <img src="../../resource/gallery/contour_shade/gpe_nonfix.png" width="400">
</p>

```commandline
python contour_shade.py ^
--image_path ../../resource/imgs/girl_with_pearl_earring.jpg ^
--resize_factor 4 ^
--color_option original ^
--thresholds_gamma 4 ^
--palette_path ../../resource/palette_files/palette_default_6_arial_fast.json
```
