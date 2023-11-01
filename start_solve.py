import os
import click
import subprocess

def run_docker_compose():
    # Define the command to run Docker Compose
    docker_compose_command = "docker compose up"

    try:
        # Execute the Docker Compose command
        subprocess.run(docker_compose_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

async def solve(task_path, max_learning, max_buffer_size, tmp_dir, n, ea_num_runs, ea_instance_size, ea_num_iters):
    task_awaitable = build_and_run_minisat_with_redis_integration(task_path, max_learning, max_buffer_size)
    backdoor_producers_awaitable = run_backdoor_producer(task_path, tmp_dir, n, ea_num_runs, ea_instance_size, ea_num_iters)
    await task_awaitable.wait()
    for task in backdoor_producers_awaitable:
        task.cancel()


def run_backdoor_producer(task_path, tmp_dir, n, ea_num_runs, ea_instance_sizes, ea_num_iters):
    os.chdir("backdoor-producer")
    tasks = []
    command = f"python star_producer.py --cnf {task_path} --tmp {tmp_dir}"
    for ea_num_run, ea_instance_size, ea_num_iters in zip(ea_num_runs, ea_instance_sizes, ea_num_iters):
        params = f"--ea-num-runs {ea_num_run} --ea-instance-size {ea_instance_size} --ea-num-iters {ea_num_iters}"
        tasks.append(asyncio.create_subprocess_shell(command + " " + params))
    return tasks

def build_and_run_minisat_with_redis_integration(task_path, max_learning, max_buffer_size):
    # Save the current directory
    current_directory = os.getcwd()

    # Change to the "minisat_with_redis_integration" directory
    os.chdir("minisat_with_redis_integration")

    # Create the "build" directory and change to it
    os.makedirs("build", exist_ok=True)
    os.chdir("build")

    # Run the "cmake .." command
    subprocess.run("cmake ..", shell=True, check=True)

    # Run the "make" command
    subprocess.run("make", shell=True, check=True)

    # Run command "./minisat"
    command = f"./minisat {task_path} --max-clause-len {max_learning} --redis-buffer {max_buffer_size}"
    task_awaitable = asyncio.create_subprocess_shell(command)

    # Restore the original directory (if necessary)
    os.chdir(current_directory)

    return task_awaitable



@click.command()
@click.argument('task_path', required=True, type=click.Path(exists=True))
@click.option('--max-learning', type=int, default=10, help='Maximum length of lernt for Redis)
@click.option('--max-buffer-size', type=int, default=5000, help='Maximum buffer size for Redis')
@click.option('-tmp', '--tmp-dir', default='backdoor-producer/tmp', help='Path to temporary directory')
@click.option('-n', type=int, required=True, help='Number of different backdoor-producer runs')
@click.option('--ea-num-runs', type=int, required=True, help='Number of backdoors')
@click.option('--ea-instance-size', type=int, required=True, help='Backdoor size')
@click.option('--ea-num-iters', type=int, required=True, help='Number of iterations')
def main(task_path, max_learning, max_buffer_size, tmp_dir, n, ea_num_runs, ea_instance_size, ea_num_iters):
    """
    This script executes the solver
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

    run_docker_compose()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(solve(task_path, max_learning, max_buffer_size, tmp_dir, n, ea_num_runs, ea_instance_size, ea_num_iters))



if __name__ == '__main__':
    main()
