#!/bin/bash -i
source activate multithreading_solver
cd ~/distributed_backdoors_search
redis-server &
python start_solve.py ./data/snake-in-a-box/s-n-b_8_98.cnf --max-learning 15 --max-buffer-size 10000 -tmp ./backdoor-producer/tmp/s-n-b_8_98.cnf --log-dir ./log/s-n-b_8_98.cnf -n 5 -er 1 -er 1 -er 1 -er 1 -er 1 -es 10 -es 10 -es 12 -es 12 -es 14 -ei 1000 -ei 1000 -ei 1000 -ei 1000 -ei 1000 -c 0 -c 0 -c 0 -c 0 -c 0
redis-cli SHUTDOWN