# coding:utf-8
# @Time : 2022/9/6 11:55
# @Author : cewinhot 
# @Version：V 1.0
# @File : snp_depth1.py
# 指定一个BAM文件和SNP[同EIGENSTRAT .snp格式]文件,输出BAM文件在每个SNPs位点的#A, #C, #G, #T, #REF, #ALT读数

import pysam
import argparse
from argparse import RawTextHelpFormatter

Usage = """
Use : python3 snp_depth.py BAM REF
this will output:
    chr pos #A #C #G #T #REF #ALT
"""
parser = argparse.ArgumentParser(description=Usage, formatter_class=RawTextHelpFormatter)
parser.add_argument('BAM', help='specify bam file', type=str)
parser.add_argument('REF_SNP', help='specify reference snp file', type=str)
args = parser.parse_args()
bam = args.BAM
snps = args.REF_SNP

dic = {"A": 0, "C": 1, "G": 2, "T": 3}

samfile = pysam.AlignmentFile(bam, "rb")
for line in open(snps):
    _, chr, _,  pos, ref, alt = line.split()  # chr, pos, ref, alt
    pos = int(pos)
    if chr == '23':
        chr = 'X'
    if chr == '24':
        chr = 'Y'
    li = samfile.count_coverage(contig=chr, start=pos - 1, stop=pos)
    print(chr, pos, li[0][0], li[1][0], li[2][0], li[3][0], li[dic[ref]][0], li[dic[alt]][0])  # A,C,G,T
