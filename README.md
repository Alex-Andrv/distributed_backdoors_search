# distributed_backdoors_search

```
git clone git@github.com:Alex-Andrv/distributed_backdoors_search.git

git submodule update --init --recursive


conda update conda 

conda config --add channels conda-forge

conda env create -f environment.yml

source activate multithreading_solver




curl -sL https://github.com/redis/hiredis/archive/refs/tags/v1.2.0.tar.gz | tar -xz

cd hiredis-1.2.0/

mkdir build && cd build

cmake -DCMAKE_INSTALL_PREFIX:PATH=$CONDA_PREFIX ..

make install

cd ../




cd distributed_backdoors_search

cd minisat_with_redis_integration

export HIREDIS_INCLUDE_DIR=$CONDA_PREFIX/include/hiredis

export HIREDIS_LIB=$CONDA_PREFIX/lib

mkdir build && cd build

cmake ..

make



cd ../../backdoor-producer/backdoor-searcher

mkdir build && cd build

cmake ..

make
```

запустите скрипт [run_lec_DvC_12.sh](run_lec_DvC_12.sh)

# Полезное
redis-server &

redis-cli SHUTDOWN

export HIREDIS_INCLUDE_DIR=/usr/local/include/hiredis

export HIREDIS_LIB=/usr/local/lib
