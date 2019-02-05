# -*- coding: utf-8 -*-
# Parameters:
#   - background
#   - color
#   - shape_appearance
#   - text_appearance
#   - theme
#   - widget_style
#   - window_configuration
# Output image:
#   attr name | android_framework | app_compat | material_component
#   :-- | :--: | :--: | :--:
#   editTextBackground | ◯ | ◯ | ー
__author__ = 'konifar'
import requests, xml.etree.ElementTree as ET
import os
import sys
import re

class Attribute:
    def __init__(self, name):
        self.name = name
        self.dict = {}

    def put(self, key, value):
        self.dict[key] = value

    def has(self, key):
        return self.dict.has_key(key)

class Category:
    def __init__(self, name):
        self.name = name

    def checkStyleableName(self, styleableName):
        if self.name == 'theme':
            return not re.search('theme', styleableName, re.IGNORECASE) and styleableName != 'Window'
        if self.name == 'window_configuration':
            return not (re.search('theme', styleableName, re.IGNORECASE)) and (styleableName != 'Window')
        else:
            return not re.search('theme', styleableName, re.IGNORECASE)

    def check(self, format, attrName):
        if self.name == 'background':
            return re.search('(reference|None)', format) and re.search('(background|divider|indicator|highlight)', attrName, re.IGNORECASE) and not re.search('(color|style)', attrName, re.IGNORECASE)
        elif self.name == 'color':
            return format == 'color' or re.search('color', attrName, re.IGNORECASE)
        elif self.name == 'shape_appearance':
            return re.search('shape', attrName, re.IGNORECASE)
        elif self.name == 'text_appearance':
            return re.search('textAppearance', attrName, re.IGNORECASE)
        elif self.name == 'theme':
            return re.search('theme', attrName, re.IGNORECASE)
        elif self.name == 'widget_style':
            return re.search('style', attrName, re.IGNORECASE)
        elif self.name == 'window_configuration':
            return re.search('window', attrName, re.IGNORECASE) and format == 'boolean'


def getEachCellValue(key, attribute):
    if (attribute.has(key)):
        return '◯'
    else:
        return 'ー'

attributesDict = {}

args = sys.argv

category = Category(args[1])

# Parse attr xml files
attrFiles = os.listdir('attrs')
for file in attrFiles:
    fileName = 'attrs/' + file
    baseName = os.path.splitext(file)[0]
    print("Start parsing: " + fileName)
    tree = ET.ElementTree(file=fileName)
    root = tree.getroot()
    for styleable in root.iter('declare-styleable'):
        styleableName = str(styleable.get('name'))
        if category.checkStyleableName(styleableName):
            continue

        for attr in styleable.iter('attr'):
            format = str(attr.get('format'))
            name = str(attr.get('name'))

            if category.check(format, name):
                if (re.search('android:', name)):
                    continue

                if (attributesDict.has_key(name)):
                    attribute = attributesDict[name]
                else:
                    attribute = Attribute(name)

                attribute.put(baseName, True)
                attributesDict[name] = attribute

# Print markdown table
outputFileName = category.name + '_attrs.md'
f = open('outputs/' + outputFileName, 'w')
f.write('attr name | android_framework | appcompat | material_components')
f.write('\n')
f.write(':-- | :--: | :--: | :--:')
f.write('\n')

for key in sorted(attributesDict):
    attribute = attributesDict[key]
    f.write('[' + attribute.name + '](https://developer.android.com/reference/android/R.attr.html#' + attribute.name + ')')
    f.write(' | ')
    f.write(getEachCellValue('android_framework', attribute))
    f.write(' | ')
    f.write(getEachCellValue('appcompat', attribute))
    f.write(' | ')
    f.write(getEachCellValue('material_components', attribute))
    f.write('\n')

f.close()
