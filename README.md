# distributed_backdoors_search
conda update conda
conda config --add channels conda-forge
conda env create -f environment.yml
source activate multithreading_sat_solver
redis-server &
export HIREDIS_INCLUDE_DIR=/usr/local/include/hiredis
export HIREDIS_LIB=/usr/local/lib
запустите redis
