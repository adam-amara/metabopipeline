

# Metabopipeline

The objective of this pipeline is to automate as much as possible the workflow in untargeted metabolomics, from the raw data to the identification of relevant compound.


## Convert .d to .mzML files with dockerized msconvert

The point of this first step is to convert your .d into .mzML files. For that, you will use the folder  [test_msconvert](https://github.com/adam-amara/metabopipeline/tree/main/test_msconvert). We will also perform centroiding on spectra, to match with metaboigniter, the next step of the workflow.

### Prepare your data

In the folder [test_msconvert](https://github.com/adam-amara/metabopipeline/tree/main/test_msconvert), you have to copy your data folder. This data folder has to be organised in a certain form, with an example below :

    data
        ├── Batch1
        │   ├── Blanks
        │   │   ├── Blank_1.d
        │   │   ├── Blank_2.d
        │   ├── CCs
        │   │   ├── CC_1.d
        │   │   ├── CC_2.d
        │   ├── QCs
        │   │   ├── QC_1.d
        │   │   ├── QC_2.d
        │   ├── Samples
        │   │   ├── Sample_1.d
        │   │   ├── Sample_2.d

Your data folder has to verify a two conditions :
- The .d files has to be organised in separate subfolders, one for each experimental class (Blanks, CCs, QCs, Samples, ...)
- The subfolder names, corresponding to the experimental classes (Blanks, CCs, QCs, Samples, ...) must not have space characters.

### Run the shell script

In the folder [test_msconvert](https://github.com/adam-amara/metabopipeline/tree/main/test_msconvert), you will find the shell script `dtomzML.sh`.

Running it will create a mzML folder in the working directory. The mzML folder will contain the same subfolders (one for each experimental class) as the organised data folder :

    mzML
        ├── Blanks
        │   ├── Blank_1.mzML
        │   ├── Blank_2.mzML
        ├── CCs
        │   ├── CC_1.mzML
        │   ├── CC_2.mzML
        ├── QCs
        │   ├── QC_1.mzML
        │   ├── QC_2.mzML
        ├── Samples
        │   ├── Sample_1.mzML
        │   ├── Sample_2.mzML

To run the script, you will need to run the command :
```shell
./dtomzML.sh <path_to_classes_subfolders>
```
For the example above, the `path_to_classes_subfolders` is `data/Batch1`.

:white_check_mark: Congratulations, you now have your .d files converted in .mzML ! :sunglasses:
