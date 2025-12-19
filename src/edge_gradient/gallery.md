# Gallery (Edge Gradient ASCII Filter)

1️⃣ `cd` to `src/edge_gradient`.

---

<p align="center">
    <img src="../../resource/gallery/edge_gradient/gpe_colored.png" width="400">
</p>

```commandline
python edge_gradient.py ^
--image_path ../../resource/imgs/girl_with_pearl_earring.jpg ^
--resize_factor 4 ^
--contrast_factor 1 ^
--thresholds_gamma 5 ^
--color_option original
```

---

<p align="center">
    <img src="../../resource/gallery/edge_gradient/gpe_colored_invert.png" width="400">
</p>

```commandline
python edge_gradient.py ^
--image_path ../../resource/imgs/girl_with_pearl_earring.jpg ^
--resize_factor 4 ^
--contrast_factor 1 ^
--thresholds_gamma 5 ^
--color_option original ^
--invert_color
```
