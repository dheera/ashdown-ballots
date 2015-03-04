#!/usr/bin/env python3

import sys, random
from subprocess import call
from tempfile import mktemp

if len(sys.argv)<2:
  print("Usage: %s sample-list.txt" % sys.argv[0])
  exit(0)

filename_list = sys.argv[1]

with open(filename_list) as f:
  # read nonempty lines only
  names = [l for l in (line.strip() for line in f) if l]

numpages = 100

latex = ""
latex += """
\\documentclass[letterpaper,12pt]{article}
\\pagestyle{empty}
\\usepackage{setspace}
\\usepackage[left=0cm,top=0cm,right=0cm,bottom=0cm,nohead,nofoot]{geometry}
\\usepackage[absolute]{textpos}
\\setstretch{2.0}
\\setlength\\parindent{0cm}
\\setlength\\parskip{0cm}
\\TPGrid[1mm,1mm]{216}{279}
\\begin{document}
\\newpage\\tiny .
"""

for n in range(0,numpages):
  for i in range(0,2):
    for j in range(0,2):
      x = 15 + i*108;
      y = 15 + j*140;
      random.shuffle(names)
      latex += "\\begin{textblock}{93}(%s,%s)" % (x,y)
      latex += "\\large"
      for name in names:
        latex += "$\\bigcirc$ %s\\\\" % name
      latex += "\\end{textblock}"
  latex += "\\newpage\\tiny .\n"
latex += "\\end{document}"

filename_latex = mktemp('tex')

file_latex = open(filename_latex, "w")
file_latex.write(latex)
file_latex.close()

call(["pdflatex", "-jobname", "ballots-output", "-output-directory", ".", filename_latex])
