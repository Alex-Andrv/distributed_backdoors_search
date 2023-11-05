import asyncio
import glob
import os
import shutil

import click
import subprocess

import redis

import random


async def run_docker_compose(_, redis_port, container_name="docker_redis"):
    # Define the command to run Docker Compose
    command = f"docker run --name {container_name} -p {redis_port}:{redis_port} -d redis"
    docker_compose_command = "docker compose up"
    return await asyncio.create_subprocess_shell(docker_compose_command,
                                                 stdin=asyncio.subprocess.PIPE,
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE
                                                 )


def ping_redis(redis_host, redis_port):
    with redis.Redis(host=redis_host, port=redis_port) as redis_client:
        response = redis_client.ping()
        if response:
            print("Redis server is up and running. Response to PING:", response)
        else:
            print("Failed to connect to the Redis server. Check that Redis is running.")
            raise redis.exceptions.ConnectionError()



def clean_dir(path_dir):
    files = glob.glob(path_dir + '/*')

    for file in files:
        try:
            if os.path.isdir(file):
                shutil.rmtree(file)  # Удаление файла
            else:
                os.remove(file)
            print(f'The {file} has been successfully deleted')
        except Exception as e:
            print(f'Error when deleting file {file}: {e}')
            raise e


async def solve(task_path, max_learning, max_buffer_size, tmp_dir, log_dir, random_seed, no_compile, redis_host,
              redis_port, n, ea_num_runs, ea_instance_size,
              ea_num_iters):
    clean_dir(log_dir)
    task_awaitable = await build_and_run_minisat_with_redis_integration(task_path, max_learning, max_buffer_size,
                                                                        log_dir, redis_host, redis_port, no_compile)
    await asyncio.sleep(2)
    backdoor_producers_awaitable = await run_backdoor_producer(task_path, tmp_dir, n, random_seed, ea_num_runs,
                                                               ea_instance_size,
                                                               ea_num_iters, log_dir, redis_host, redis_port, no_compile)
    return_code = await task_awaitable.wait()
    print(f"return code = {return_code}")
    for task in backdoor_producers_awaitable:
        task.kill()


def build_backdoor_searcher():
    current_directory = os.getcwd()
    os.chdir("backdoor-searcher")

    clean_dir("build")

    # Create the "build" directory and change to it
    os.makedirs("build", exist_ok=True)
    os.chdir("build")

    # Run the "cmake .." command
    subprocess.run("cmake ..", shell=True, check=True)

    # Run the "make" command
    subprocess.run("make", shell=True, check=True)
    os.chdir(current_directory)


async def run_backdoor_producer(task_path, tmp_dir, n, random_seed, ea_num_runs, ea_instance_sizes, ea_num_iters,
                                root_log_dir, redis_host, redis_port, no_compile):
    current_directory = os.getcwd()
    os.chdir("backdoor-producer")
    if not no_compile:
        build_backdoor_searcher()

    random.seed(random_seed)

    tasks = []
    command = f"python star_producer.py --cnf {'../' + task_path}"
    for i, (ea_num_run, ea_instance_size, ea_num_iters) in enumerate(zip(ea_num_runs, ea_instance_sizes, ea_num_iters)):
        log_dir = '../' + root_log_dir + f"/backdoor-producer-instance:{i}-ea_num_run:{ea_num_run}-ea_instance_size:{ea_instance_size}-ea_num_iters:{ea_num_iters}"
        experement_dir = os.path.join(log_dir, "experement")
        os.makedirs(log_dir)
        stdout_log_file = log_dir + "/backdoor-producer-stdout"
        stderr_log_file = log_dir + "/backdoor-producer-stderr"
        new_seed = random.randint(1, 10000)
        params = (f"--tmp {tmp_dir + str(i)} --random-seed {new_seed} --ea-num-runs {ea_num_run} --ea-instance-size {ea_instance_size} --ea-num-iters {ea_num_iters} "
                  f"--root-log-dir {experement_dir} --redis-host {redis_host} --redis-port {redis_port}")
        redirect = f" > {stdout_log_file} 2> {stderr_log_file}"
        tasks.append(await asyncio.create_subprocess_shell(command + " " + params + " " + redirect))
        print("run star_producer with param: " + params + " " + redirect)

    os.chdir(current_directory)
    return tasks


async def build_and_run_minisat_with_redis_integration(task_path, max_learning, max_buffer_size, log_dir,
                                                       redis_host, redis_port, no_compile):
    # Save the current directory
    current_directory = os.getcwd()

    if not no_compile:
        # Change to the "minisat_with_redis_integration" directory
        os.chdir("minisat_with_redis_integration")

        clean_dir("build")

        # Create the "build" directory and change to it
        os.makedirs("build", exist_ok=True)
        os.chdir("build")

        # Run the "cmake .." command
        subprocess.run("cmake ..", shell=True, check=True)

        # Run the "make" command
        subprocess.run("make", shell=True, check=True)

    stdout_log_file = "../../" + log_dir + "/minisat-stdout"
    stderr_log_file = "../../" + log_dir + "/minisat-stderr"
    # Run command "./minisat"
    command = (f"./minisat {'../../' + task_path} -max-clause-len={max_learning} -redis-buffer={max_buffer_size} "
               f"-redis-host={redis_host} -redis-port={redis_port}")
    task_awaitable = await asyncio.create_subprocess_shell(f"{command} > {stdout_log_file} 2> {stderr_log_file}")
    # Restore the original directory (if necessary)
    os.chdir(current_directory)

    print("run minisat")

    return task_awaitable


def flushall_redis(redis_host, redis_port):
    with redis.Redis(host=redis_host, port=redis_port) as redis_client:
        redis_client.flushall()
        print("Executed the FLUSHALL command to delete all data")


@click.command()
@click.argument('task_path', required=True, type=click.Path(exists=True))
@click.option('--max-learning', type=int, default=10, help='Maximum length of lernt for Redis')
@click.option('--max-buffer-size', type=int, default=5000, help='Maximum buffer size for Redis')
@click.option('-tmp', '--tmp-dir', type=click.Path(exists=False), default='./backdoor-producer/tmp',
              help='Path to temporary directory')
@click.option('-log', '--log-dir', type=click.Path(exists=False), default='./log',
              help='Path to log file')
@click.option('-seed', '--random-seed', type=int, default=42,
              help='Random seed')
@click.option(
    "--no-compile/--compile", "no_compile", default=True, help="no compile"
)
@click.option('--redis-host', default='localhost', help='Redis server host')
@click.option('--redis-port', default=6379, help='Redis server port')
@click.option('-n', type=int, required=True, help='Number of different backdoor-producer runs')
@click.option('-er', '--ea-num-runs', type=int, required=True, multiple=True, help='Number of backdoors')
@click.option('-es', '--ea-instance-size', type=int, required=True, multiple=True, help='Backdoor size')
@click.option('-ei', '--ea-num-iters', type=int, required=True, multiple=True, help='Number of iterations')
def main(task_path, max_learning, max_buffer_size, tmp_dir, log_dir, random_seed, no_compile,
         redis_host, redis_port, n, ea_num_runs, ea_instance_size, ea_num_iters):
    """
    This script executes the solver
    example:
    python start_solve.py ./data/mult/lec_CvK_12.cnf  --max-learning 15 --max-buffer-size 10000 -tmp tmp --log-dir log -n 5 -er 2 -er 5 -er 10 -er 10 -er 10 -es 8 -es 10 -es 12 -es 14 -es 16 -ei 800 -ei 1000 -ei 2000 -ei 2000 -ei 2000
    """
    click.echo(f'Path to the task: {task_path}')
    click.echo(f'Maximum length of lernt for Redis: {max_learning}')
    click.echo(f'Maximum buffer size for Redis: {max_buffer_size}')
    click.echo(f'Path to temporary directory: {tmp_dir}')
    click.echo(f'Number of different backdoor-producer runs: {n}')
    click.echo(f'Number of backdoors: {ea_num_runs}')
    click.echo(f'Backdoor size: {ea_instance_size}')
    click.echo(f'Number of iterations: {ea_num_iters}')
    assert (len(ea_num_runs) == len(ea_instance_size) == len(ea_num_iters) == n), "Dimensions do not match"

    os.makedirs(log_dir, exist_ok=True)
    print(f"log dir: {log_dir}")

    ping_redis(redis_host, redis_port)
    flushall_redis(redis_host, redis_port)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        solve(task_path, max_learning, max_buffer_size, tmp_dir, log_dir, random_seed, no_compile, redis_host,
              redis_port, n, ea_num_runs, ea_instance_size,
              ea_num_iters))


if __name__ == '__main__':
    main()
