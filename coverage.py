# coding:utf-8
# @Time : 2021/8/31 23:33
# @Author : cewinhot
# @Version：V 0.1
# @File : coverage.py

import sys

Usage = """
use: python3 coverage.py PREFIX
output samples' coverage information
"""
if len(sys.argv) < 2:
    sys.exit(Usage)


def detect(a):
    if a == "1" or a == "2" or a == "0":
        return True
    else:
        return False


path = sys.argv[1]
total = 0
path = path.split(sep=".geno")[0]
path = path.split(sep=".ind")[0]
path = path.split(sep=".snp")[0]
ln = len(open(path + ".geno").readline().strip())
s = [0 for _ in range(ln)]
for line in open(path + ".geno"):
    for k in range(len(line)):
        if detect(line[k]):
            s[k] += 1
    total += 1

print("total snp position : {}".format(total))
print("snps\tcoverage\tindividuals\tsexsual\tpopulation")
with open(path + ".ind") as file:
    for i, j in zip(s, file):
        if i != 0:
            print(i, round(i / total, 3), j, sep="\t", end="")

