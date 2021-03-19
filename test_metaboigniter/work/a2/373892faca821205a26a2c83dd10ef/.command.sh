#!/bin/bash -euo pipefail
echo 1.0.0 > v_pipeline.txt
echo 20.10.0 > v_nextflow.txt
scrape_software_versions.py &> software_versions_mqc.yaml
