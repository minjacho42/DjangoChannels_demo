#!/bin/bash

docker stop ft_transendence
docker rm ft_transendence
docker rmi ft_transendence
docker build -t ft_transendence .
docker run --name ft_transendence -d -p 8000:8000 ft_transendence