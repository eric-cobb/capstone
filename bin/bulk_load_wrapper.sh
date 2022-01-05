#!/bin/bash

for year in $(seq 1990 2021); do
    echo "Bulk loading year $year"
  python3 bulk_load_accidents.py output/cases$year.ndjson
done
