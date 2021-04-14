

# Metabopipeline

The objective of this pipeline is to automate as much as possible the workflow in untargeted metabolomics, from the raw data to the identification of relevant compound.

Here is an example with HCC dataset.

## Data structure

Below is the organisation of our data.

In the folder pipeline_dataHCC, we have 2 subfolders and 2 scripts :
    - dataHCC : where the data are converted and saved 
    - metaboigniter : GitHub repository from nf-core/metaboigniter
    - prepare_metaboigniter.py
    - run_all.sh


    pipeline_dataHCC
        ├── dataHCC
        │   ├── dtomzML
        │   │   ├── dataHCC_d
        │   │   │   ├── Blank
        │   │   │   │   ├── Blank_001.d
        │   │   │   ├── MSMS
        │   │   │   │   ├── AutoMSMS_018.d
        │   │   │   ├── QC
        │   │   │   │   ├── QC41_013.d
        │   │   │   │   ├── QC41_026.d
        │   │   │   ├── Sample
        │   │   │   │   ├── LivCan_085_018.d
        │   │   │   │   ├── LivCan_086_019.d
        │   │   │   │   ├── LivCan_299_014.d
        │   │   │   │   ├── LivCan_300_015.d
        │   │   │   │   ├── LivCan_309_020.d
        │   │   │   │   ├── LivCan_363_016.d
        │   │   ├── dockerfile
        │   │   ├── dtomzML.sh
        │   ├── hmdb
        │   │   ├── hmdb_2017-07-23.csv
        ├── metaboigniter
        ├── prepare_metaboigniter.py
        ├── run_all.sh
        
In the first part, we will convert the raw data (.d files into .mzML).

In the second part, we will run the metaboigniter pipeline with our data (.mzML files) and our specific parameters.


## 1 - Convert .d to .mzML files with dockerized msconvert

The point of this first step is to convert the .d into .mzML files. For that, we will use the command :
```bash
cd dataHCC/dtomzML
```

Then, we run the command :
```bash
./dtomzML.sh <path_to_classes_subfolders>
```

For our example :
```bash
./dtomzML.sh dataHCC_d
```

The shell script uses the dockerized image of msconvert to perform the conversion and peak picking of the raw data. In `pipeline_dataHCC/dataHCC/dtomzML`, we now have a folder named `mzML` with the same structure as the folder `dataHCC_d` and our converted files.



## 2 - Run metaboigniter pipeline

Now that we have our mzML files, let's run metaboigniter to perform the quantification and identification !

We run the command to set the working directory to `pipeline_dataHCC` :
```bash
cd ../..
```

Now we run the shell script `run_all.sh` :
```bash
./run_all.sh
```

The script first launches the python script `prepare_metaboigniter.py` to set the most important parameters needed to set to the metaboigniter config file `metaboigniter/conf/parameters.config` .
Here are the input which work on our data :
- Enter relative path to the folder containing all the subfolders (one for each condition) which contain the mzML files : `dataHCC/dtomzML/mzML`
- What type of ionization do you have ? Enter POS, NEG or BOTH : `POS`
- Does the workflow has to perform the centroiding ? Enter true or false : `false`
- Do you want to remove signal from blank samples ? Enter true or false : `true`
- Do you want to rename the samples in the output file ? Enter true or false : `false`
- Enter the name of the class of the blank samples : `Blank`
- Enter the name of the class of the biological samples : `Sample`
- Entre the name of the class of the quality controls : `QC`
- Do you want to perform identification ? Enter true or false : `true`
- Enter the name of the class of the MS2 samples : `MSMS`
- Enter relative path to csv database : `dataHCC/hmdb/hmdb_2017-07-23.csv`

Then the shell script runs metaboigniter through nextflow and the docker image.



:white_check_mark: We have now a `results` folder with the outputs of metaboigniter :sunglasses:









