#!/bin/sh


alias rmsp='sed "s/^\s*//g" | sed "s/[[:blank:]]\+/\t/g"'
samples_dir=/home/KongyangZhu/data/12.shallow/2022.10.31/Bamfiles
output_dir=/home/KongyangZhu/data/12.shallow/2022.10.31/stats
bc=/home/KongyangZhu/sh/Useful/bc.py
samples=$(ls -l ${samples_dir} | grep drwx | awk '{print $9}')
mkdir -p ${output_dir} ; cd ${output_dir}


# 1. aln.endogenous rate : endogenous rate before Dedup from Samtools flagstats
for i in ${samples};do
    echo -n -e "${i}\t"
    cat ${samples_dir}/${i}/${i}.aln.flagstats | grep mapped | grep % | head -n 1
done | sed 's/(//g' | awk '{print $1,$6}' | rmsp > aln.endogenous_rate.result

# 2. endogenous : endogenous rate after Dedup from Samtools flagstats
for i in ${samples};do
    cat ${samples_dir}/${i}/${i}.flagstats | grep mapped | grep % | head -n 1
done | sed 's/(//g' | awk '{print $5}' > endogenous_rate.result

# 3. duplication : duplication rate from Dedup log
for i in ${samples};do
    cat ${samples_dir}/${i}/${i}.duplication.txt | grep "Duplication Rate:" | awk '{print $3}'
done > duplication.result

# 4. library.length : average length of whole library (including unmapping reads) from Samtools stats
for i in ${samples};do
    cat ${samples_dir}/${i}/${i}.stats | grep "average length:" | awk '{print $4}'
done > library.length

# 5. mapped.length : average length of mapped reads only from Samtools stats
for i in ${samples};do
    cat ${samples_dir}/${i}/${i}.mapped.stats | grep "average length:" | awk '{print $4}'
done > mapped.length

# 6. mapped reads : mapped reads from Samtools stats
for i in ${samples};do
    cat ${samples_dir}/${i}/${i}.mapped.stats | grep "reads mapped:" | awk '{print $4}'
done > mapped.reads

# 7. mapped bases : mapped bases (cigar) from Samtools stats
for i in ${samples};do
    cat ${samples_dir}/${i}/${i}.mapped.stats | grep "bases mapped (cigar):" | awk '{print $5}'
done > mapped.bases

# 8. average quality : average quality of mapped bases
for i in ${samples};do
    cat ${samples_dir}/${i}/${i}.mapped.stats | grep "average quality:" | awk '{print $4}'
done > average.quality

# 9. Coverage : mapped bases/3095693981*100%
cov=$(cat mapped.bases)
for i in ${cov};do
    python ${bc} ${i}/3095693981*100
    echo "%"
done > mapped.coverage

# Summary
body="aln.endogenous_rate.result endogenous_rate.result duplication.result library.length mapped.length mapped.reads mapped.bases average.quality mapped.coverage"
echo -e "Samples\taln.endogenous\tendogenous\tduplication rate\tlibrary.length\tmapped.length\tmapped reads\tmapped bases\taverage quality\tcoverage" > header.tmp
paste ${body} > body.tmp
for i in "Annotation";do
    echo ""
    echo "# aln.endogenous : endogenous rate from Samtools flagstats (before Dedup)"
    echo "# endogenous : endogenous rate from Samtools flagstats (after Dedup)"
    echo "# duplication : duplication rate from Dedup log"
    echo "# library.length : average length of whole library (including unmapping reads) from Samtools stats"
    echo "# mapped.length : average length of reads mapped to human only from Samtools stats"
    echo "# mapped reads : mapped reads from Samtools stats"
    echo "# mapped bases : mapped bases (cigar) from Samtools stats"
    echo "# average quality : average base quality of mapped bases"
    echo "# coverage : mapped bases/3095693981*100%"
done > annotation.tmp
cat header.tmp body.tmp annotation.tmp > Summary.table ; rm *.tmp ${body}