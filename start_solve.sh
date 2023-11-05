#!/bin/bash

# Запуск Docker, замените <имя образа> на фактическое имя образа Docker.
docker compose up

# Ожидание, чтобы убедиться, что Docker-контейнер запущен (это может потребовать некоторого времени).
sleep 10

./run_minisat_with_redis_integration.sh "$@"




# Запуск проекта с определенными параметрами, замените <параметры> на фактические параметры.
./minisat <параметры>

# Запуск цикла для backdoor-producer с разными гиперпараметрами (n раз)
n=<n>
for i in $(seq 1 $n)
do
    # Здесь замените <гиперпараметры> на фактические гиперпараметры.
    ./backdoor-producer <гиперпараметры>
done