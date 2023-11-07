# distributed_backdoors_search
conda update conda
conda config --add channels conda-forge
conda env create -f environment.yml
source activate multithreading_solver

cd hiredis-1.2.0/
mkdir build && cd build
curl -sL https://github.com/redis/hiredis/archive/refs/tags/v1.2.0.tar.gz | tar -xz
cmake -DCMAKE_INSTALL_PREFIX:PATH=$CONDA_PREFIX ..
make install
cd ../

cd minisat_with_redis_integration
mkdir build && cd build
export HIREDIS_INCLUDE_DIR=$CONDA_PREFIX/include/hiredis
export HIREDIS_LIB=$CONDA_PREFIX/lib
cmake ..
make

cd ../../backdoor-producer/backdoor-searcher
mkdir build && cd build
cmake ..
make

redis-server &

запустите redis
