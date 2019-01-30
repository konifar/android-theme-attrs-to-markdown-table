# -*- coding: utf-8 -*-
# Output image:
#   attr name | android_framework | app_compat | material_component
#   :-- | :--: | :--: | :--:
#   textAppearance | ◯ | ◯ | ー
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

def getEachCellValue(key, attribute):
    if (attribute.has(key)):
        return '◯'
    else:
        return 'ー'

outputFileName = 'outputs/window_configuration_attrs.md'
attributesDict = {}

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
        if not (re.search('theme', styleableName, re.IGNORECASE)) and (styleableName != 'Window'):
            continue

        for attr in styleable.iter('attr'):
            format = str(attr.get('format'))
            name = str(attr.get('name'))

            if (re.search('window', name, re.IGNORECASE) and format == 'boolean'):
                if (re.search('android:', name)):
                    continue

                if (attributesDict.has_key(name)):
                    attribute = attributesDict[name]
                else:
                    attribute = Attribute(name)

                attribute.put(baseName, True)
                attributesDict[name] = attribute

# Print markdown table
f = open(outputFileName, 'w')
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
