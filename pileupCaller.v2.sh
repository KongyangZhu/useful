#!/bin/bash


dir=/home/KongyangZhu/illumina-Huada/mgiseq-xten/mgiseq
pops=mgiseq
bamfile=$(ls ${dir}/*/*.trim.bam)
samples=""
bamfilein=""
ref=~/ref/hs37d5/hs37d5.fa
ref_snp=~/ref/map/2.2M.XY.snp
ref_pos=~/ref/map/2.2M.XY.pos
for i in ${bamfile};do
        bamfilein="${bamfilein} $i"
        samples=${samples},$(basename $i .trim.bam)
done
samples=${samples:1}
echo ${samples}
echo ${bamfilein}
samtools mpileup -R -B -q30 -Q30 -l ${ref_pos} \
    -f ${ref} \
    ${bamfilein} | \

pileupCaller --randomHaploid --sampleNames ${samples} \
    -f ${ref_snp} \
    -e ${pops} > pileupCaller.log 2>&1
