import argparse
import pandas as pd
import os
import re
import shutil
import gzip
import glob
from Bio import SeqIO

# Parse command line inputs
parser = argparse.ArgumentParser(description='Takes the paths of the input files for doing the processing and the path where the results will be saved')
parser.add_argument('--xlsx', type=str, help='Path to the QC excel file')
parser.add_argument('--fastq_pass', type=str, help='Path to the fastq_pass folder')
parser.add_argument('--output_dir', type=str, help='Path to the output directory')
args = parser.parse_args()

#create the raw_fast folder
os.makedirs(os.path.join(args.output_dir, "raw_fastq"), exist_ok=True)
raw=os.path.join(args.output_dir, "raw_fastq")

# Function to read the excel file
def read_xlsx_file(xlsx_path):
    return pd.read_excel(xlsx_path, header=0, dtype=str)

folder_name_list = []
output_name_list = []

# Function to process barcode and sample lists
def process_lists(barcode_list, sample_list):
    for barcode, sample in zip(barcode_list, sample_list):
        folder_name_list.append(re.sub(r'NB', 'barcode', str(barcode)))
        tmp_out = f"{barcode}_{sample}.fastq"
        output_name_list.append(tmp_out)
    return folder_name_list, output_name_list

# Function to write priority list to a excel file
def write_priority_list(priority_list):
    priority = pd.DataFrame(priority_list, dtype=str)
    priority.to_csv("Sample_names.csv", index=False, header=False)
    
# Function to decompress and join fastq files
def decompress_and_join_files(gz_dir, folder_name):
    os.chdir(gz_dir)
    gz_files = os.listdir(gz_dir)
    for i in gz_files:
        if i.endswith(".gz"):      
            with gzip.open(i, "rt") as file_obj:
                contents = SeqIO.parse(file_obj, "fastq")
                name = re.sub(r'.gz', '', i)
                with open(name, 'wt') as file:
                    SeqIO.write(contents, file, "fastq")

    file_list = glob.glob("*.fastq")
    with open("combined.fastq", 'a') as c_file:   
        for file_path in file_list:
            with open(file_path, "rt") as infile:
                file_contents = SeqIO.parse(file_path, "fastq")
                SeqIO.write(file_contents, c_file, "fastq")   
    print(f"The fastq files have been combined for: {folder_name}")

# Function to create blank output files
def create_blank_output_files(raw, output_name_list):
    for out_name in output_name_list:
        with open(os.path.join(raw, out_name), "w") as out_file:
            pass

# Function to transfer combined fastq files to respective output files
def transfer_files_to_output(gz_dir, raw, folder_name, output_name_list):
    b_no = re.sub(r"barcode", "", folder_name)
    source_path = os.path.join(gz_dir, "combined.fastq")
    for name in output_name_list:
        tmp_name = re.sub(r"NB", "", name)
        if tmp_name.startswith(b_no):
            dest_path= os.path.join(raw, name)
            dest = shutil.copyfile(source_path, dest_path)
            print(f"Destination folder for {name}: {dest}")



# Main function to execute the entire workflow
def main(xlsx_path, fastq_pass, raw):
    # Read excel file
    xlsx_file = read_xlsx_file(xlsx_path)
    
    # Process barcode and sample lists
    barcode_list = xlsx_file.iloc[:,0].astype(str).values.tolist()
    sample_list = xlsx_file.iloc[:,1].astype(str).values.tolist()
    folder_name_list, output_name_list = process_lists(barcode_list, sample_list)
    print("SAMPLES:")
    for name in output_name_list:
        print(name)
    
    # Write priority list to a excel file
    priority_list = [re.sub(r".fastq", "", name) for name in output_name_list]
    write_priority_list(priority_list)
    
    # Decompress and join fastq files
    for folder_name in folder_name_list:
        gz_dir = os.path.join(fastq_pass, folder_name)
        decompress_and_join_files(gz_dir, folder_name)
    
    # Create blank output files
    create_blank_output_files(raw, output_name_list)
    
    # Transfer combined fastq files to respective output files
    for folder_name in folder_name_list:
        gz_dir = os.path.join(fastq_pass, folder_name)
        transfer_files_to_output(gz_dir, raw, folder_name, output_name_list)
    print("Pre-processing complete! Proceeding with QC.")

# Call the main function with command line arguments
main(args.xlsx, args.fastq_pass, raw)