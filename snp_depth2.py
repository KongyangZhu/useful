# coding:utf-8
# @Time : 2022/9/6 11:55
# @Author : cewinhot 
# @Version：V 1.0
# @File : snp_depth2.py
# 指定一个BAM文件和位置CHR1:POS1 CHR2:PO2,输出BAM文件在每个SNPs位点的#A, #C, #G, #T, #REF, #ALT读数

import sys
import pysam
from argparse import RawTextHelpFormatter

Usage = """
Use : python3 snp_depth.py BAM CHR1:POS1 CHR2:PO2
this will output:
    chr pos #A #C #G #T #REF #ALT
"""

print(Usage)
dic = {"A": 0, "C": 1, "G": 2, "T": 3}
bam = sys.argv[1]
li = sys.argv[2:]
samfile = pysam.AlignmentFile(bam, "rb")

for i in li:
    chr, pos = i.split(":")
    pos = int(pos)
    if chr == '23':
        chr = 'X'
    if chr == '24':
        chr = 'Y'
    li = samfile.count_coverage(contig=chr, start=pos - 1, stop=pos)
    print(chr, pos, li[0][0], li[1][0], li[2][0], li[3][0])  # A,C,G,T
