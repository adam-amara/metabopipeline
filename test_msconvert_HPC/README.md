
# msconvert on HPC with Singularity

This folder contains the shell script to run the `msconvert` Singularity image on the IARC HPC.

It actually works exactly as explained in the main README.md for the `msconvert` Docker image on the local machine.

The data folder has to be organised with one subfolder for each condition (Blank, QC, Sample, ...). In each of these subfolders are located the .d raw files.

Then, the following command has te be run :
```bash
./dtomzML.sh <path_to_classes_subfolders>
```
Here, for our example :
```bash
./dtomzML.sh data
```

The shell script `dtomzML.sh` first builds the msconvert Singularity image from the Docker image `chambm/pwiz-skyline-i-agree-to-the-vendor-licenses`, then browses the subfolders to convert the .d files into .mzML.

The output is a folder `mzML` with the same organisation as the `data` folder.






