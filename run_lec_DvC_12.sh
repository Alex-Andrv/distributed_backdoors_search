#!/bin/bash -i
source activate multithreading_solver
cd ~/distributed_backdoors_search
redis-server &
python start_solve.py data/mult/lec_DvC_12.cnf --max-learning 15 --max-buffer-size 10000 -tmp ./backdoor-producer/tmp/lec_DvC_12 --log-dir ./log/lec_DvC_12 -n 5 -er 1 -er 1 -er 1 -er 1 -er 1 -es 6 -es 8 -es 10 -es 12 -es 14 -ei 800 -ei 800 -ei 1000 -ei 1000 -ei 2000 -c 3000 -c 3000 -c 3000 -c 2000 -c 2000
redis-cli SHUTDOWN