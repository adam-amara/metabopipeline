# Metabopipeline

The objective of this pipeline is to automate as much as possible the workflow in untargeted metabolomics, from the raw data to the identification of relevant compound.

Here is an example with the EPIC Liver dataset.

## 0 - Data structure

Below is the organisation of our data.

In the folder EPIC-Liver-Metabolome, we have 2 subfolders and 2 scripts :


    EPIC-Liver-Metabolome
        ├── HILIC_POS
        
        │   ├── msconvert_dtomzML
        │   │   ├── data_d
        │   │   │   ├── Blanks
        │   │   │   │   ├── EPIC_Liver_Cancer_NR160809_001_Blank_001.d
        │   │   │   │   ├── ...
        │   │   │   ├── MSMS
        │   │   │   │   ├── AutoMSMS_018.d
        │   │   │   │   ├── ...
        │   │   │   ├── QCs
        │   │   │   │   ├── EPIC_Liver_Cancer_NR160809_013_QC41_013.d
        │   │   │   │   ├── ...
        │   │   │   ├── Samples
        │   │   │   │   ├── EPIC_Liver_Cancer_NR160809_003_61-LivCan_127_003.d
        │   │   │   │   ├── ...
        │   │   ├── dtomzML.sh
        │   │   ├── slurm_msconvert.sb
        
        │   ├── run_metaboigniter
        │   │   ├── data
        │   │   │   ├── database
        │   │   │   │   ├── hmdb_2017-07-23.csv
        │   │   │   │   ├── biomarkers_and_microbial_metabolites.csv
        │   │   ├── run_metaboigniter.sb
        
        

In the first part, we will convert the raw data (.d into .mzML files).

In the second part, we will run the metaboigniter pipeline with our data (.mzML files) and our specific parameters.


## 1 - Convert .d to .mzML files with dockerized msconvert

The point of this first step is to convert the .d into .mzML files. In the folder `msconvert_dtomzML`, you have :
- the folder `data_d`, containing the .d files in subfolders corresponding to their class (Blanks, MSMS, QCs, Samples)
- the shell script `dtomzML.sh`, which pulls the `msconvert` singularity image from the DockerHub and performs the conversion on each .d file. We also decided to apply a centroiding on MS1-level but keeping the spectrum on MS2-level, with the option `--filter "peakPicking true 1"`.
- the slurm script `slurm_msconvert.sb` to manage the HPC configurations for the conversion

Once the data structure is set, you have to change the present working directory to `msconvert_dtomzML` with the `cd` command :
```bash
cd EPIC-LIVER-Metabolome/HILIC_POS/msconvert_dtomzML
```

Then, you can change the options for the `sbatch` command directly in the  `slurm_msconvert.sb` file, especially the node names on which you want to launch the process. Then, use the `sbatch` command with one argument, the relative path to the folder containing all the .d files, to submit the job. For our example :
```bash
sbatch slurm_msconvert.sb data_d
```

Have a break, have a KitKat, and after a while, in `EPIC-LIVER-Metabolome/HILIC_POS/msconvert_dtomzML`, you now have a folder `mzML` with the same structure as the folder `data_d` and your converted files !

Your data structure should look like that :

    msconvert_dtomzML
    ├── data_d
    │   ├── Blanks
    │   │   ├── EPIC_Liver_Cancer_NR160809_001_Blank_001.d
    │   │   ├── ...
    │   ├── MSMS
    │   │   ├── AutoMSMS_018.d
    │   │   ├── ...
    │   ├── QCs
    │   │   ├── EPIC_Liver_Cancer_NR160809_013_QC41_013.d
    │   │   ├── ...
    │   ├── Samples
    │   │   ├── EPIC_Liver_Cancer_NR160809_003_61-LivCan_127_003.d
    │   │   ├── ...
    ├── dtomzML.sh
    ├── img_msconvert
    ├── mzML
    │   ├── Blanks
    │   │   ├── EPIC_Liver_Cancer_NR160809_001_Blank_001.mzML
    │   │   ├── ...
    │   ├── MSMS
    │   │   ├── AutoMSMS_018.mzML
    │   │   ├── ...
    │   ├── QCs
    │   │   ├── EPIC_Liver_Cancer_NR160809_013_QC41_013.mzML
    │   │   ├── ...
    │   ├── Samples
    │   │   ├── EPIC_Liver_Cancer_NR160809_003_61-LivCan_127_003.mzML
    │   │   ├── ...
    ├── slurm-XXXXXXX.out
    ├── slurm_msconvert.sb
    
The newly created folders and files are :
- the folder `img_msconvert`, the `msconvert` singularity image
- the file `slurm-XXXXXXX.out`, logs of your submitted job (XXXXXXX corresponding the job ID)
- the most important, the folder `mzML`, containing the mzML files !



## 2 - Run metaboigniter pipeline

Now that you have your mzML files, you can run `metaboigniter` to perform the quantification and identification !

First, change the present working directory to  run the command to set the working directory to the folder `run_metaboigniter`. If you didn't already change it after the conversion, you should just have to run this :
```bash
cd ../run_metaboigniter
```

Ideally, we would like to automatise the pipeline as much as possible, to make it general and applicable for different datasets. For now, we made a few steps by hand to make it fit for the EPIC Liver dataset. Therefore, the data structure of `run_metaboigniter` is as followed :

    │   ├── run_metaboigniter
    │   │   ├── data
    │   │   │   ├── database
    │   │   │   │   ├── hmdb_2017-07-23.csv
    │   │   │   │   ├── biomarkers_and_microbial_metabolites.csv
    │   │   │   ├── mzML
    │   │   │   ├── mzML_POS_ID
    │   │   │   │   ├── ................
    │   │   │   │   ├── ...all MSMS mzML files...
    │   │   │   │   ├── ................
    │   │   │   ├── mzML_POS_Quant
    │   │   │   │   ├── ................
    │   │   │   │   ├── ...all Blanks, QCs and Samples mzML files
    │   │   │   │   ├── ................
    │   │   │   ├── phenotype_files
    │   │   │   │   ├── phenotype_HILIC_POS.csv
    │   │   ├── metaboigniter
    │   │   ├── run_metaboigniter.sb

The `data` folder contains :
- a folder `mzML`, the one containing all the mzML files we converted previously
- a folder `mzML_POS_Quant`, containing all mzML files needed for the quantification subpipeline (i.e. from Blanks, QCs and Samples classes)
- a folder `mzML_POS_ID`, containing all mzML files needed for the identification subpipeline (i.e. from MSMS class)
- a folder `phenotype_files`, containing a csv file with the mzML metadata : for each mzML file needed for the quantification, its name, the corresponding class (Blanks, QCs, Samples) and if Sample, the corresponding Group (Incident or Non_case)

The `metaboigniter` folder comes from the [nf-core/metaboigniter repository](https://github.com/nf-core/metaboigniter), with a few modifications to fit the EPIC Liver data :
- parameters changed in configuration file `metaboigniter/conf/paramaters.config`
- add of  `metaboigniter/conf/custom.config` to manage HPC resources
- change of one parameter in `bin/run_metfrag.sh` to manage HPC resources


Once this is all set, we can launch the pipeline by submitting the job with slurm :
```bash
sbatch run_metaboigniter.sb
```

Have a break, have a coffee this time because it will take a while to compute !

At the end of the pipeline, your data structure should look like that :

    │   ├── run_metaboigniter
    │   │   ├── data
    │   │   │   ├── database
    │   │   │   │   ├── hmdb_2017-07-23.csv
    │   │   │   │   ├── biomarkers_and_microbial_metabolites.csv
    │   │   │   ├── mzML
    │   │   │   ├── mzML_POS_ID
    │   │   │   │   ├── ................
    │   │   │   │   ├── ...all MSMS mzML files...
    │   │   │   │   ├── ................
    │   │   │   ├── mzML_POS_Quant
    │   │   │   │   ├── ................
    │   │   │   │   ├── ...all Blanks, QCs and Samples mzML files
    │   │   │   │   ├── ................
    │   │   │   ├── phenotype_files
    │   │   │   │   ├── phenotype_HILIC_POS.csv
    │   │   ├── metaboigniter
    │   │   ├── results
    │   │   │   ├── pipeline_info
    │   │   │   │   ├── ................
    │   │   │   │   ├── ...html and dag files to report and display the pipeline's steps
    │   │   │   │   ├── ................
    │   │   │   ├── process_identification_aggregate_pos_metfrag
    │   │   │   ├── process_output_quantid_pos_camera_metfrag
    │   │   │   │   ├── metadataPOSout_pos_metfrag.txt
    │   │   │   │   ├── peaktablePOSout_pos_metfrag.txt
    │   │   │   │   ├── varsPOSout_pos_metfrag.txt
    │   │   │   ├── process_pepcalculation_metfrag_pos_passatutto   
    │   │   ├── run_metaboigniter.sb
    │   │   ├── slurm-XXXXXXX.out
    │   │   ├── work

The newly created folders and files are :
- the file `slurm-XXXXXXX.out`, logs of your submitted job (XXXXXXX corresponding the job ID)
- the folder `work`, containing all process work directories of the `metaboigniter` pipeline (classical nextflow sh*t)
- the folder `results`, with the subfolder `process_output_quantid_pos_camera_metfrag`, in which we get the three most important txt files, detailed in the [metaboigniter repository](https://github.com/nf-core/metaboigniter/blob/master/docs/output.md#final-output)



        
        

## 3 - Jupyter notebooks to identify potential biomarkers

Now that we have our peak table and the associated metadata, we can apply various machine learning methods to identify potential biomarkers.

The objective is to find compounds which differentiate the __Incident__ from the __Non-case__ samples.

### 1-clean_peakTable.ipynb

This notebook takes the file `peaktablePOSout_pos_metfrag.txt` from metaboigniter results as input.

Initially, the txt file looks like that :
| dataMatrix      | EPIC_Liver_Cancer_NR160809_007_41_LivCan_153_007.mzML | EPIC_Liver_Cancer_NR160809_008_41_LivCan_154_008.mzML | ... |
| :-------------- | :-----------:| :----------: | :---: |
| variable_3      | 19.7617... | 19.7352... | ... |
| variable_5      | 14.5368... | 15.1933... | ... |
| variable_6      | 22.1855... | 20.8314... | ... |
| ...                   | ...              | ...              | ... |

It contains variables in rows and samples in columns.

For further analysis, we prefer to have variables (i.e. compounds) in columns and samples in rows. Moreover, in this notebook, we add two columns :
- SampleID : LivCan-XXX, which is the suffix of the filename
- Groups : Incident or Non-case

At the end of this notebook, our peak table looks like that :
| SampleID               | Groups     | variable_3  | variable_5 | ... |
| :--------------------- | :----------: | :----------: | :----------: | :---: |
| LivCan_153.mzML | Incident    | 19.7617... | 14.5368... | ... |
| LivCan_154.mzML | Non-case | 19.7352... | 15.1933... | ... |
| ...                            | ...              | ...              | ...              | ... |






