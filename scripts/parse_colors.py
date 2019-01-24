# -*- coding: utf-8 -*-
# Output image:
#   attr name | android_framework | app_compat | material_component
#   :-- | :--: | :--: | :--:
#   colorPrimary | ◯ | ◯ | ー
__author__ = 'konifar'
import requests, xml.etree.ElementTree as ET
import os
import sys
import re

class ColorAttr:
    def __init__(self, name):
        self.name = name
        self.dict = {}

    def put(self, key, value):
        self.dict[key] = value

    def has(self, key):
        return self.dict.has_key(key)

def getEachCellValue(key, colorAttr):
    if (colorAttr.has(key)):
        return '◯'
    else:
        return 'ー'

colorAttrsDict = {}

# Parse attr xml files
attrFiles = os.listdir('attrs')
for file in attrFiles:
    fileName = 'attrs/' + file
    baseName = os.path.splitext(file)[0]
    print("Start parsing: " + fileName)
    tree = ET.ElementTree(file=fileName)
    root = tree.getroot()

    for attr in root.iter('attr'):
        format = str(attr.get('format'))
        name = str(attr.get('name'))

        if (format == 'color' or re.search('color', name, re.IGNORECASE)):
            if (re.search('android:', name)):
                continue

            if (colorAttrsDict.has_key(name)):
                colorAttr = colorAttrsDict[name]
            else:
                colorAttr = ColorAttr(name)

            colorAttr.put(baseName, True)
            colorAttrsDict[name] = colorAttr

# Print markdown table
f = open('outputs/color_attrs.md', 'w')
f.write('attr name | android_framework | appcompat | material_components')
f.write('\n')
f.write(':-- | :--: | :--: | :--:')
f.write('\n')

for key in sorted(colorAttrsDict):
    colorAttr = colorAttrsDict[key]
    f.write(colorAttr.name)
    f.write(' | ')
    f.write(getEachCellValue('android_framework', colorAttr))
    f.write(' | ')
    f.write(getEachCellValue('appcompat', colorAttr))
    f.write(' | ')
    f.write(getEachCellValue('material_components', colorAttr))
    f.write('\n')

f.close()
