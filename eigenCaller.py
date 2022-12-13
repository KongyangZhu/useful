# coding:utf-8
# @Time : 2022/12/09 01:29
# @Author : zky
# @Version: 1.0
# @File : eigenCaller.py


import sys
import argparse
from argparse import RawTextHelpFormatter

Usage = """
Use : python3 eigenCaller.py --sampleNames sample1,sample2,sample -f 1240k.XY.snp -e PREFIX -p pops -d 3
this will output:
    PREFIX.ind   -> EIGENSTART format individual information file
    PREFIX.snp   -> EIGENSTRAT format SNP file
    PREFIX.geno  -> EIGENSTRAT format genotype file
"""
parser = argparse.ArgumentParser(description=Usage, formatter_class=RawTextHelpFormatter)
parser.add_argument('--sampleNames', help='sample names seperate by ","', type=str, required=True)
parser.add_argument('-f', '--snpFile', help='reference snp FILE', type=str, required=True)
parser.add_argument('-e', '--eigenstratOut', help='FILE prefix', type=str, required=True)
parser.add_argument('-p', '--popNames', help='Pop Names', type=str, default='Unknown')
parser.add_argument('-d', '--minDepth', help='depth lower than N is tagged as missing phenotype', type=int, default=3)
try:
    args = parser.parse_args()
except:
    print(Usage)
    exit()

Samples = args.sampleNames.strip().split(",")
RefFile = args.snpFile
prefix = args.eigenstratOut
pops = args.popNames
MINDEPTH = args.minDepth


SampleN = len(Samples)

snpfile = open(prefix + '.snp', 'wt', encoding='utf-8')
genofile = open(prefix + '.geno', 'wt', encoding='utf-8')
base_dict = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

with open(prefix + '.ind', 'wt', encoding='utf-8') as file:
    for i in Samples:
        file.write(f'{i}\tU\t{pops}\n')

with open(RefFile, 'rt', encoding='utf-8') as text:
    while True:
        mpileup = sys.stdin.readline()
        if mpileup == "":
            break
        mpileup = mpileup.strip().split()
        mchr, mpos, mref, *rest = mpileup

        line = text.readline()
        _, chr, _, pos, ref, alt = line.strip().split()

        while mchr != chr or mpos != pos:
            genofile.write('9' * SampleN + '\n')
            snpfile.write(line)
            line = text.readline()
            _, chr, _, pos, ref, alt = line.strip().split()
        snpfile.write(line)
        # pheno = ""
        for i in range(SampleN*3):
            if i % 3 == 0:
                count = int(rest[i])
            if i % 3 == 1:
                if count < MINDEPTH:  # depth filter: count < MINDEPTH [DEFAULT: 3]
                    genofile.write('9')  # pheno += '9'
                    continue
                st = rest[i].replace(",", mref).replace(".", mref).upper()
                count_li = st.count('A') / count, st.count('C') / count, st.count('G') / count, st.count('T') / count
                if count_li[base_dict[ref]] >= 0.9:
                    genofile.write('2')  # pheno += '2'
                elif count_li[base_dict[alt]] >= 0.9:
                    genofile.write('0')  # pheno += '0'
                elif count_li[base_dict[ref]] >= 0.25 and count_li[base_dict[alt]] >= 0.25 and (count_li[base_dict[ref]] + count_li[base_dict[alt]]) >= 0.9:
                    genofile.write('1')  # pheno += '1'
                else:
                    genofile.write('9')  # pheno += '9'
        genofile.write('\n')  # genofile.write(pheno + '\n')
snpfile.close()
genofile.close()

