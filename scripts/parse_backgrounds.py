# -*- coding: utf-8 -*-
# Output image:
#   attr name | android_framework | app_compat | material_component
#   :-- | :--: | :--: | :--:
#   editTextBackground | ◯ | ◯ | ー
__author__ = 'konifar'
import requests, xml.etree.ElementTree as ET
import os
import sys
import re

class BackgroundAttr:
    def __init__(self, name):
        self.name = name
        self.dict = {}

    def put(self, key, value):
        self.dict[key] = value

    def has(self, key):
        return self.dict.has_key(key)

def getEachCellValue(key, backgroundAttr):
    if (backgroundAttr.has(key)):
        return '◯'
    else:
        return 'ー'

backgroundAttrsDict = {}

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
        if not (re.search('theme', styleableName, re.IGNORECASE)):
            continue

        for attr in styleable.iter('attr'):
            format = str(attr.get('format'))
            name = str(attr.get('name'))

            if (format == 'reference' and re.search('background', name, re.IGNORECASE)):
                if (re.search('android:', name)):
                    continue

                if (backgroundAttrsDict.has_key(name)):
                    backgroundAttr = backgroundAttrsDict[name]
                else:
                    backgroundAttr = BackgroundAttr(name)

                backgroundAttr.put(baseName, True)
                backgroundAttrsDict[name] = backgroundAttr

# Print markdown table
f = open('outputs/background_attrs.md', 'w')
f.write('attr name | android_framework | appcompat | material_components')
f.write('\n')
f.write(':-- | :--: | :--: | :--:')
f.write('\n')

for key in sorted(backgroundAttrsDict):
    backgroundAttr = backgroundAttrsDict[key]
    f.write(backgroundAttr.name)
    f.write(' | ')
    f.write(getEachCellValue('android_framework', backgroundAttr))
    f.write(' | ')
    f.write(getEachCellValue('appcompat', backgroundAttr))
    f.write(' | ')
    f.write(getEachCellValue('material_components', backgroundAttr))
    f.write('\n')

f.close()
