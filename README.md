# distributed_backdoors_search
conda update conda
conda config --add channels conda-forge
conda env create -f environment.yml
source activate multithreading_solver

curl -sL https://github.com/redis/hiredis/archive/refs/tags/v1.2.0.tar.gz | tar -xz
cmake -DCMAKE_INSTALL_PREFIX:PATH=$CONDA_PREFIX ..
make install

redis-server &
export HIREDIS_INCLUDE_DIR=$CONDA_PREFIX/include/hiredis
export HIREDIS_LIB=$CONDA_PREFIX/lib
запустите redis
