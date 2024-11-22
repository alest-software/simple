#!/usr/bin/env python3

import os
from pathlib import Path
import xml.etree.ElementTree as ET
from argparse import ArgumentParser

def write(f, html):
    tree = ET.ElementTree(html)
    ET.indent(tree, space='  ', level=0)
    f.write('<!DOCTYPE html>\n')
    tree.write(f, xml_declaration=True, method='html', encoding='unicode')
    f.write('\n')


def project(directory):
    rval = 0

    html = ET.Element('html')
    body = ET.SubElement(html, 'body')
    with os.scandir(directory) as it:
        for i in it:
            if i.name.endswith('.whl') and i.is_file():
                a = ET.SubElement(body, 'a')
                a.attrib['href'] = f'{i.name}'
                a.text = i.name
                rval += 1

    if rval > 0:
        fname = directory / 'index.html'
        with open(fname, 'w') as f:
            write(f, html)

    return rval


def index(directory):
    html = ET.Element('html')
    body = ET.SubElement(html, 'body')
    with os.scandir(directory) as it:
        for i in it:
            if not i.name.startswith('.') and i.is_dir():
                x = project(directory / Path(i.name))
                if x > 0:
                    a = ET.SubElement(body, 'a')
                    a.attrib['href'] = f'/{i.name}/'
                    a.text = i.name

    fname = directory / 'index.html'
    with open(fname, 'w') as f:
        write(f, html)


def main():
    parser = ArgumentParser()
    parser.add_argument('directory')
    args = parser.parse_args()
    directory = Path(args.directory)
    index(directory)


main()

