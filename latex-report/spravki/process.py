# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 22:59:42 2024

@author: ostap
"""

import csv
import subprocess
import io

def generate_file(template, id, user):
    filename = f'certificate_{id}.tex'
    with open(filename, 'w', encoding='utf-8') as latex_file:
        latex = template.replace(r'\VAR{USER}', user)
        latex_file.write(latex)
    print(f'Generated {filename}')
    subprocess.call(['latexmk', '-pdf', filename])

with open('spravka_template_sliv.tex', encoding='utf-8') as template_file:
    global latex_code
    latex_code = template_file.read()
    print (latex_code)

with open('input_sliv.csv', encoding='utf8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            generate_file(latex_code, row[0], row[1])
            line_count += 1
    print(f'Processed {line_count} lines.')