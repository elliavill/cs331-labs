You should expect your output to look like the following:

Have yourself a god jul och a gott nytt år please.
Caesar cipher? I much prefer Caesar salad!
usage: 4_scripts_w_dicts.py [-h] [-v] -i <input file> -o <output file> (-e | -d)
4_scripts_w_dicts.py: error: the following arguments are required: -i/--input, -o/--output

If you run the program as py 4_scripts_w_dicts.py -h, you might see something like this:

Have yourself a god jul och a gott nytt år please.
Caesar cipher? I much prefer Caesar salad!
usage: 4_scripts_w_dicts.py [-h] [-v] -i <input file> -o <output file> (-e | -d)

translate file using ROT 13

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i <input file>, --input <input file>
                        path to the file that should be processed
  -o <output file>, --output <output file>
                        path where the results will be saved to
  -e, --encode          specify that the input file should be encoded
  -d, --decode          specify that the input file should be decoded

If you run the program as py 4_scripts_w_dicts.py -v, you might see something like this:

Have yourself a god jul och a gott nytt år please.
Caesar cipher? I much prefer Caesar salad!
4_scripts_w_dicts.py 1.0.0

If you run the program as py 4_scripts_w_dicts.py -i 4_scripts_w_dicts.py -o lab4_output.txt -e, you might see something like this:

Have yourself a god jul och a gott nytt år please.
Caesar cipher? I much prefer Caesar salad!

After running the previous command, you might want to try running type lab4_output.txt or more < lab4_output.txt to see something like the following:

#! /hfe/ova/rai clguba3
# -*- pbqvat: hgs-8 -*-
"""Yno frg 4 - Clguba fpevcgf hfvat qvpgvbanel.

These are the first three lines. If you then run the program as py 4_scripts_w_dicts.py -i lab4_output.txt -o lab4_code.txt -d, you can run type lab4_code.txt or more < lab4_code.txt to see something like this:

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lab set 4 - Python scripts using dictionary.

Again, these are the first three lines of the file.