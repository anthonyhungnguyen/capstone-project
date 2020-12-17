#!/bin/bash

# PYTHONPATH="$(dirname"$(dirname"$(realpath $0)")")"
# echo "PYTHONPATH="${PYTHONPATH}
PYTHONPATH="/home/jetson02/Documents/phuc/facereg_cnn/FCI_Database_P/sources"
location="$(dirname "${PYTHONPATH}")"
# source ${location}/fcienv/bin/activate
source /home/jetson02/Documents/phuc/facereg_cnn/phuc/bin/activate

echo "PYTHONPATH="${PYTHONPATH}
echo "location="${location}

echo "****. Start [python ${PYTHONPATH}/trainning/extracting.py] ..."
cd ${PYTHONPATH}
python streaming/app.py