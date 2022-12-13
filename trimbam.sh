#!/bin/bash
# @Time : 2021/7/30 12:13
# @Author : zky
# @Version : V 0.1
# @File : trim.bam


dir="/home/KongyangZhu/data/Dawenkou_new/bamfile"
outdir="/home/KongyangZhu/data/Dawenkou_new/trimbam"
thread=11
files=$(ls ${dir}/*/*.mapped.bam)
for i in ${files};do
        sample=$(basename $i .mapped.bam)
        bam trimBam ${i} ${outdir}/${sample}.trim.bam 3
        samtools index -@ ${thread} ${outdir}/${sample}.trim.bam
done
