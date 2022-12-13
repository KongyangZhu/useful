#!/bin/bash
# @Time : 2022/10/09 12:49
# @Author : cewinhot
# @Version：0.1
# @File : bamstats


bam=$1
thread=11
sample=$(basename ${bam} .bam)
samtools stats    -@ ${thread} ${bam} > ${sample}.stats
samtools idxstats -@ ${thread} ${bam} > ${sample}.idxstats
samtools flagstat -@ ${thread} ${bam} > ${sample}.flagstats
