import os
import re

log = "log"

for dir in os.listdir(log):
        dir_path = os.path.join(log, dir)
        if os.path.isdir(dir_path):


def get_backdoor_producer_name(log_dir):
    for dir in os.listdir(log):
        dir_path = os.path.join(log, dir)
        if os.path.isdir(dir_path):
            pattern = r"(\d+)"

            integers = list(map(int, re.findall(pattern, dir)))

            backdoor_producer = {"instance": integers[0],
                                 "ea_num_run": integers[1],
                                 "ea_instance_size": integers[2],
                                 "ea_num_iters": integers[3],
                                 "full_name": dir}


get_backdoor_producer_name()