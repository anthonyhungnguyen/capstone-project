#!/bin/bash

PYTHONPATH="$(dirname"$(dirname"$(realpath $0)")")"
echo "PYTHONPATH="${PYTHONPATH}
# PYTHONPATH="/home/jetson02/Documents/phuc/facereg_cnn/FCI_Database_P/sources"
# PYTHONPATH = "/Users/nguyenanhhoangphuc/Documents/Intern/sources"
# location="$(dirname "${PYTHONPATH}")"
# source ${location}/fcienv/bin/activate
# source /Users/nguyenanhhoangphuc/Documents/Intern/sources/phuc/bin/activate

# echo "PYTHONPATH="${PYTHONPATH}
# echo "location="${location}


# echo "1. Executing [python ${PYTHONPATH}/trainning/extracting.py] ..."
# python ${PYTHONPATH}/trainning/extracting.py &&

# echo "2. Executing [python ${PYTHONPATH}/trainning/checking_features.py] ..."
# python ${PYTHONPATH}/trainning/checking_features.py &&

# echo "3. Executing [python ${PYTHONPATH}/trainning/trainning1.py] ..."
# python ${PYTHONPATH}/trainning/trainning1.py

echo "*** Executing [python ${PYTHONPATH}/trainning/train_flow] ..."
python ${PYTHONPATH}/trainning/train_flow.py

exit