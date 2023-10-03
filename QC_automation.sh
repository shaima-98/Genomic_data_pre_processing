#!/usr/bin/bash
echo "Let's begin!"
python Pre_processing.py --xlsx $1 --fastq_pass $2 --output_dir $3 
raw_folder=raw_fastq
run_no=Run_20                 #change it with every new run
cd "$3/$raw_folder"
eval "$(conda shell.bash hook)"
conda activate NanoStat
samples="/media/decodeage/d1672139-af38-4080-8ce9-3acbf29c35a5/Decode_biome_pipeline/QC_automation/Sample_names.csv"
file=$(cut -d',' -f1 "$samples"| tr -d '\r')
while IFS= read -r sample
do
    NanoStat --fastq ${sample}.fastq -o ./ -n ./${sample}.txt 
done <<< "$file"
if [ $? -eq 0 ]; then
    echo "QC complete!"
else
    echo "Error in QC!"
fi
mkdir "$4/$run_no"
mv *.txt -t "$4/$run_no"
if [ $? -eq 0 ]; then
    echo "Success! See you again in the next run!"
else
    echo "Error occured!"
fi

#arguments needed= $1 $2 $3 $4 