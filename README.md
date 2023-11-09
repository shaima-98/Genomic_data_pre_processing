The Bash script, 'QC_automation.sh' is exceuted in the command line which is designed to automate the quality control (QC) and organization of DNA sequencing data. It performs the following tasks:

1. Executes the python file, 'Pre_processing.py' to perform the pre-processing steps.
This Python script is designed to automate the pre-processing of DNA sequencing data. It takes the path to an Excel file containing information about barcodes and sample names, the directory containing       compressed FASTQ files, and an output directory where the processed data will be saved. The script reads the Excel file, processes barcode and sample lists, decompresses and joins FASTQ files, creates blank output files, and transfers the combined FASTQ data to their respective output files. It also generates a priority list and conducts pre-processing steps to prepare the data for quality control (QC) analysis. This script streamlines the initial steps of data preparation for downstream sequencing data analysis workflows.

2. Activates a Conda environment named "NanoStat" for running QC tools.  
3. Reads a priority list of sample names from a CSV file.  
4. Executes the NanoStat tool for each sample using its corresponding FASTQ file   
5. Moves the generated QC output files to a specified directory.   
6. Creates a directory for the current run and organizes QC results there.   
7. Provides status messages indicating whether QC was successful or if any errors occurred.
   
The script is intended to be used as part of an automated sequencing data analysis pipeline and streamlines the QC process, making it easier to process and organize large volumes of sequencing data.
