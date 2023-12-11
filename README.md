# `distributed_backdoors_search`

## Build instructions

Clone the repo and initizlie submodules (sorry for using them):
```
git clone https://github.com/Alex-Andrv/distributed_backdoors_search
cd distributed_backdoors_search
git submodule update --init --recursive
cd ..
```

Setup Conda environment:
```
conda config --add channels conda-forge
conda env create -f environment.yml
conda activate multithreading_solver
```

Compile hiredis from sources:
```
curl -sL https://github.com/redis/hiredis/archive/refs/tags/v1.2.0.tar.gz | tar -xz
cd hiredis-1.2.0/
make PREFIX=$(realpath install) -j install
cd ..
```

Compile the solver (MiniSat with Redis integration) (deprecate, use mapl):
```
cd distributed_backdoors_search
cd minisat_with_redis_integration
cmake -B build -DCMAKE_BUILD_TYPE=Release -DHIREDIS_INCLUDE_DIR=$(realpath ../../hiredis-1.2.0/install/include/hiredis) -DHIREDIS_LIB=$(realpath ../../hiredis-1.2.0/install/lib)
cmake --build build
cd ..
```

Compile the solver (Maple_LCM_Dist_Chrono with Redis integration):
```
export HIREDIS_INCLUDE_DIR=~/hiredis-1.2.0/install/include/hiredis
export HIREDIS_LIB=~/hiredis-1.2.0/install/lib
export LD_LIBRARY_PATH=~/hiredis-1.2.0/install/lib:$LD_LIBRARY_PATH

cd Maple_LCM_Dist_Chrono_with_redis/sources/core
make clean
make r
cd ~
```

Compile the backdoor searcher:
```
cd backdoor-producer/backdoor-searcher
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
cd ../../
```

Run [`run_lec_DvC_12.sh`](run_lec_DvC_12.sh).

---

### Other

```
redis-server &
redis-cli SHUTDOWN
export HIREDIS_INCLUDE_DIR=/usr/local/include/hiredis
export HIREDIS_LIB=/usr/local/lib
```
