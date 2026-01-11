# Palette Tutorial

This tutorial describes how to make a palette. To begin with, check out the
[default palette I made](./resource/palette_files/palette_default_consolab_fast.json) first.

```json
{
  "name": "palette_default_consolab_fast",
  "templates": [
    {
      "layer": 0,
      "chars": " ",
      "font": "C:/Windows/Fonts/consolab.ttf",
      "font_size": 24,
      "char_bound_width": 13,
      "char_bound_height": 22,
      "match_method": "fast"
    },
    {
      "omitted": "the rest of contents have been omitted..."
    }
  ]
}
```

All templates should begin with a dictionary that has a property `name` and a property `templates`.

`name` is not functionally used in code, so technically you can name it anything you want. 

`templates` is more important. It's a list of dictionaries and each dictionary in it is
called a `layer`.

## Object in templates

| field                   | type  | default      | range     | Only effective when                                          | help                                                                                                                                                                                                                                                                                                                  |
|-------------------------|-------|--------------|-----------|--------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| layer                   | int   | 0            |           |                                                              | Not functionally used in code. It's there for you as a memo.                                                                                                                                                                                                                                                          |
| chars                   | str   | **REQUIRED** |           |                                                              | A string that contains all characters you want to use in this layer (gradient level). New line character and duplicated characters will be ignored.                                                                                                                                                                   |
| font                    | str   | **REQUIRED** |           |                                                              | The path that leads to your font. Make sure the font is installed on your PC and is there. Moreover, you can use different fonts across different layers. Just make sure that you set the font size, char_bound_width, char_bound_height values properly for each layer.                                              |
| font_size               | int   | **REQUIRED** | x > 0     |                                                              | The size of the font, must be integer.                                                                                                                                                                                                                                                                                |
| char_bound_width        | int   | **REQUIRED** | x > 0     |                                                              | (Pixel) Width of one single character in the image.                                                                                                                                                                                                                                                                   |
| char_bound_height       | int   | **REQUIRED** | x > 0     |                                                              | (Pixel) Height of one single character in the image.                                                                                                                                                                                                                                                                  |
| approx_ratio            | float | 1            | 0 < x < 1 | Fixed width character bound & `match_method`=`vector`        | Used to approximate the comparison of template matching. Smaller value leads to faster rendering but also degrades the matching quality. This value is completely useless if the `match_method` is not `vector`, like in this case. This value must be between 0 and 1, with 0 being exclusive and 1 being inclusive. |
| vector_top_k            | int   | 5            | x > 0     | Fixed width character bound & `match_method`=`vector`        | Used to filter the matching candidates by pixel amount. Smaller value leads to faster rendering but also could miss retrieve better candidates. This value is completely useless if the `match_method` is not `vector`, like in this case.                                                                            |
| match_method            | str   | fast         |           | Fixed width character bound                                  | The algorithm of template matching.                                                                                                                                                                                                                                                                                   |
| pad_top                 | int   | 0            |           |                                                              | The top padding of each single character. Cropping if this value is negative.                                                                                                                                                                                                                                         |
| pad_bottom              | int   | 0            |           |                                                              | The bottom padding of each single character. Cropping if this value is negative.                                                                                                                                                                                                                                      |
| pad_left                | int   | 0            |           |                                                              | The left padding of each single character. Cropping if this value is negative.                                                                                                                                                                                                                                        |
| pad_right               | int   | 0            |           |                                                              | The right padding of each single character. Cropping if this value is negative.                                                                                                                                                                                                                                       |
| --flow_match_method     | str   | fast         |           | Non-fixed width character bound                              | The algorithm for non-fixed width template (character) matching. Check below for available options.                                                                                                                                                                                                                   |
| --binary_threshold      | str   | 90           | x >= 0    | Non-fixed width character bound & `flow_match_method`=`fast` | The threshold value for converting a grayscale image to binary. This is only used when `flow_match_method=fast`.                                                                                                                                                                                                      |
| --override_layer_weight | float | None         |           | Non-fixed width character bound                              | Set weight for layer if you want to set your own rather than using the default (lower-rank layers weight more).                                                                                                                                                                                                       |
| --override_widths       | list  | None         |           |                                                              | More detail below.                                                                                                                                                                                                                                                                                                    |
| --override_weights      | list  | None         |           | Non-fixed width character bound                              | More detail below.                                                                                                                                                                                                                                                                                                    |

**override_widths**

A list of the following objects. When set, use the overridden bound width rather than
`char_bound_width` for the specified character. Width must be greater than 0.
```txt
{
  "char": (char),
  "width": (int)
}
```

<br>


**override_weights**
A list of the following objects. When set, use the overridden weight rather than the one calculated by
the program for the specified character. Weight can be any number. 💡 Tip: if you want some
characters to appear less frequently in the final result, such as white space, you can set its weight
to a big negative number (such as -10000).
```txt
{
  "char": (char),
  "weight": (float)
}
```

<br>

**match_method**

| code      | help                                                                                                                                |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------|
| slow      | The slowest matching algorithm with the best matching quality. The templates are grayscale.                                         |
| optimized | Almost twice as fast as slow. The templates are binary. The resulting image will look bold compared to slow method.                 |
| fast      | Almost twice as fast as optimized. Utilizes XOR comparison. The resulting image is very similar to optimized method.                |
| vector    | Almost ten times as fast as slow. Vectorize all smaller images and compare the flattened array. The resulting image is much bolder. |

<br>

**flow_match_method**

| code | help                                                                                        |
|------|---------------------------------------------------------------------------------------------|
| slow | The slowest matching algorithm with the best matching quality. The templates are grayscale. |
| fast | Both the image and templates will be converted to binary. Utilizes XOR comparison.          |

<br>

🧑‍🏫 **My tips**: more layers will lead the algorithm to be more precise about the shading levels.
In theory, this will output better quality rendering if you do things correctly.
Usually for the layers in the higher rank you should use less dense characters. For example:
```text
. , '
```
For the layers in the lower rank you should use more dense characters. For example:
```text
% # @
```
The characters are not limited to ASCII characters. You can use other characters as long as 
your font supports them.
