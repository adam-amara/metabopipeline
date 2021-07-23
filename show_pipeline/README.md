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

The output of this notebook is the csv file `peakTable_HILIC_POS.csv`.


### 2-explore_data.ipynb

This notebook takes the previously created file `peakTable_HILIC_POS.csv` as input.

The objective of this notebook is to explore the peak table cleaned in the previous notebook (1-clean_RPpos_peakTable) with a few visualisations on :
- target (here the Sample Group, i.e. Incident vs. Non-case)
- missing values
- outliers
- ...

#### Basic checklist :

__Form analysis__ :
- __target__ : Groups
- __shape (rows & columns)__ : 186 rows (samples) x 558 columns (556 compounds)
- __features types__ :
    - quantitative : 2 (Group, SampleID)
    - qualitative : 556 (compounds)
- __missing values__ :
    - compounds can be in every sample (0% of missing values), in most of them or just in a few
    - the maximum of missing value for a variable is 49.5%, i.e. this variable is absent from 49.5% of the samples
    - (samples seem to be more easily separated with not too much missing values (logic))

__Content analysis__ :
- __target visualisation__ :
    - ratio 1:1 (93 Cancer - 93 Healthy)
- __feature visualisation__ :
    - on the first 10 compounds, most of them follow a normal distribution
    - some of them follow a double normal distribution
    - maybe one distribution for each class (Healthy vs Cancer) --> hypothesis
- __relation features/target__ :
    - on the first 10 compounds, we don't see a clear difference of intensity between the Cancer and Healthy samples --> previous hypothesis rejected on these compounds --> may be true of others
- __relation features/features__ : strong correlations between some of the features --> need to reduce the dimension for further analysis
- __t-test__ : this is a huge approximation but a first t-test allows to have a first view on potential important variables

This t-test is a huge approximation as it considers the feature's intensities independant, but we know that they highly interact. We can still observe that, for a few compounds, there exists a significant difference of intensity between the cancer and healthy samples.



### 3-missing_value_imputation.ipynb

This notebook takes the csv file `peakTable_HILIC_POS.csv` (created in the notebook `1-clean_peakTable.ipynb`) as input.

The purpose of this notebook is to use different methods to fill the missing values in our peak table :

- __Univariate__ feature imputation :
    - __zero__ (or __one__ or any other constant value to avoid further analytical problems)
    - __mean__
    - __median__
    - __mode__ (most frequent)
    - __minimum__
    - __half minimum__
- __Multivariate__ feature imputation :
    - __MICE__ (inspired by the R `MICE` package)
- __KNN imputation__

These methods come from the scikitlearn documentation : [cf. doc scikitlearn](https://scikit-learn.org/stable/modules/impute.html#marking-imputed-values)

One type of imputation algorithm is __univariate__, which imputes values in the i-th feature dimension __using only non-missing values in that feature dimension__ (e.g. `impute.SimpleImputer`>). By contrast, __multivariate__ imputation algorithms __use the entire set of available feature dimensions__ to estimate the missing values (e.g. `impute.IterativeImpute`).


The scikitlearn `IterativeImputer` is still experimental, so we will also use directly the R `MICE` package  ([documentation](https://www.rdocumentation.org/packages/mice/versions/3.13.0/topics/mice)) in the separate R notebook `3.2-missing_value_imputation_MICE` (in this directory)

Here is a link where the [MICE algorithm is explained](https://cran.r-project.org/web/packages/miceRanger/vignettes/miceAlgorithm.html).

The MICE (Multivariate Imputation by Chained Equations) algorithm is a multivariate method to impute missing values. Each missing value is imputed using a separate model with the other variables in the dataset. Iterations should be run until it appears that convergence has been met.


For each of these methods, we can save the imputed peak table as a new csv file.




### 4-normalisation_scaling_pipeline.ipynb

This notebook takes an imputed peak table as input, imputed with any of the previous methods, as long as it has no NAs left.

The purpose of this notebook is to use different methods to normalise/scale the data in our peak table.

The function `normPeakTable` takes a peak table and a list of methods to normalise the peak table. The available methods are :
- log10 : base-10 logarithm
- std : standard scaler
- min-max normalisation
    - minmax : across features
    - minmax_rows : across samples
- scale to unit norm (vector length). If $x$ is the vector of length $n$, the normalized vector is $y=x/z$ then $z$ is defined as followed according to the chosen norm :
    - norm_l1 : with l1 norm $\rightarrow z = \| x\|_1 = \sum_{i=1}^n |x_i|$
    - norm_l2 : with l2 norm $\rightarrow z = \| x\|_2 = \sqrt{\sum_{i=1}^n x_i^2}$
    

It is possible to apply different normalisation/scaling methods to the peak table. You should provide as parameter the list of the methods in the order you want it to be applied to the peak table. Example, for _normPeakTable(X_KNN, ['std', 'norm_l2'])_, a standard scaler will first be applied, followed by a norm l2 scaling.

The normalised/scaled peak tables (output of the function `normPeakTable`) can be saved as csv file.








