#!/bin/bash -i
source activate multithreading_solver
cd ~/distributed_backdoors_search
redis-server --port 6382 &
PID=$!
python start_solve.py ./data/mults_inversion_cnfs/MultColumn32x32_randinp_2.cnf --max-learning 15 --redis-port 6382 --max-buffer-size 10000 -tmp ./backdoor-producer/tmp/MultColumn32x32_randinp_2 --log-dir ./log/MultColumn32x32_randinp_2 -n 5 -er 1 -er 1 -er 1 -er 1 -er 1 -es 10 -es 10 -es 12 -es 12 -es 14 -ei 1000 -ei 1200 -ei 1500 -ei 1500 -ei 2000 -c 0 -c 0 -c 1000 -c 2000 -c 3000
redis-cli SHUTDOWN
kill -9 $PID