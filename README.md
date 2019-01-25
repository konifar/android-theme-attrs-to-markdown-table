# android-theme-attrs-to-markdown-table
Simple tool to parse Android theme attrs.xml to markdown table.

## Outputs
- [colors](https://github.com/konifar/android-theme-attrs-to-markdown-table/blob/master/outputs/color_attrs.md)
- [backgrounds](https://github.com/konifar/android-theme-attrs-to-markdown-table/blob/master/outputs/background_attrs.md)
- [text_appearances](https://github.com/konifar/android-theme-attrs-to-markdown-table/blob/master/outputs/textappearance_attrs.md)
- [component_styles](https://github.com/konifar/android-theme-attrs-to-markdown-table/blob/master/outputs/widget_style_attrs.md)
- [themes](https://github.com/konifar/android-theme-attrs-to-markdown-table/blob/master/outputs/theme_attrs.md)

## Run
### Color attributes
```shell
$ python ./scripts/parse_colors.py
# => outputs/color_attrs.md
```

### Background Attributes
```shell
$ python ./scripts/parse_backgrounds.py
# => outputs/background_attrs.md
```

### TextAppearance Attributes
```shell
$ python ./scripts/parse_text_appearances.py
# => outputs/text_appearance_attrs.md
```

### Widget style Attributes
```shell
$ python ./scripts/parse_widget_styles.py
# => outputs/widget_style_attrs.md
```

### Theme Attributes
```shell
$ python ./scripts/theme_styles.py
# => outputs/theme_attrs.md
```
