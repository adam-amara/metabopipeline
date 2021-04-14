

## Organisation of .d files

    dataHCC
        ├── dataHCC_d
        │   ├── Blank
        │   │   ├── Blank_001.d
        │   ├── QC
        │   │   ├── QC41_013.d
        │   │   ├── QC41_026.d
        │   ├── Sample
        │   │   ├── LivCan_085_018.d
        │   │   ├── LivCan_086_019.d
        │   │   ├── LivCan_299_014.d
        │   │   ├── LivCan_300_015.d
        │   │   ├── LivCan_309_020.d
        │   │   ├── LivCan_363_016.d
        │   ├── MSMS
        │   │   ├── AutoMSMS_018.d
        │   │   ├── AutoMSMS_293.d
        │   │   ├── AutoMSMS_351.d
        
## Conversion .d to .mzML

### Blank - QC - Sample

```bash
msconvert *.d --zlib --filter "peakPicking true [1,2]" -o $FOL
```

Tests :
- with and without peakPicking
- filter to keep only MS1 spectra or MS1 and MS2 spectra

### MSMS

```bash
msconvert *.d --zlib --filter "peakPicking true 2" --filter "msLevel 2" -o $FOL
```

Tests :
- with and without peakPicking
- filter to keep only MS2 spectra or MS1 and MS2 spectra



## Organisation of .mzML files (same as .d files)

    dataHCC
        ├── mzML
        │   ├── Blank
        │   │   ├── Blank_001.mzML
        │   ├── QC
        │   │   ├── QC41_013.mzML
        │   │   ├── QC41_026.mzML
        │   ├── Sample
        │   │   ├── LivCan_085_018.mzML
        │   │   ├── LivCan_086_019.mzML
        │   │   ├── LivCan_299_014.mzML
        │   │   ├── LivCan_300_015.mzML
        │   │   ├── LivCan_309_020.mzML
        │   │   ├── LivCan_363_016.mzML
        │   ├── MSMS
        │   │   ├── AutoMSMS_018.mzML
        │   │   ├── AutoMSMS_293.mzML
        │   │   ├── AutoMSMS_351.mzML
        
    
## Prepare metaboigniter pipeline

    test_metaboigniter
        ├── dataHCC
        │   ├── hmdb_2017-07-23.csv
        │   ├── mzML
        ├── metaboigniter
        ├── prepare_metaboigniter.py
        ├── run_all.sh

Here is the content of `run_all.sh` :
```bash
python3 prepare_metaboigniter.py

nextflow run metaboigniter/main.nf -profile docker
```

In a terminal, run de command `./run_all.sh`

First, it launches the python script to set the most important parameters :
- data to .mzML files : `dataHCC/mzML`
- type of ionization : `POS`
- need centroiding : `false`
- remove signal from blank samples : `true`
- rename output files : `false`
- class of the blank samples : `Blank`
- class of the biological samples : `Sample`
- class of the QC samples : `QC`
- perform identification : `true`
- class of the MS2 samples : `MSMS`

It changes all these parameters in the congig file : `metaboigniter/conf/parameters.config`

Then metaboigniter is run with the `nextflow` command.



## Metaboigniter processes

- get_software_versions
- process_masstrace_detection_pos_xcms_noncentroided
- process_collect_rdata_pos_xcms
- process_align_peaks_pos_xcms
- process_group_peaks_pos_N1_xcms
- process_blank_filter_pos_xcms
- process_annotate_peaks_pos_camera
- process_group_peaks_pos_camera
- process_find_addcuts_pos_camera
- process_find_isotopes_pos_camera
- process_read_MS2_pos_msnbase
- process_mapmsms_tocamera_pos_msnbase
- process_mapmsms_toparam_pos_msnbase
- process_ms2_identification_pos_csifingerid (FAILS HERE)
- process_identification_aggregate_pos_csifingerid
- process_pepcalculation_csifingerid_pos_passatutto
- process_output_quantid_pos_camera_csifingerid






    
    
