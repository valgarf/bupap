# BUPAP
This repository is a proof of concept for a "**b**ottom **up** **a**gile **p**lanning" tool.
Currently you can only install it and browse the testdata, it is **NOT YET A USEFUL TOOL**.

# Getting Started

## Installation

You can either run the application as a simple python application or use the docker image.

### python package
You can install the python package using  
```
pip[x] install bupap
```
and run it with  
```
bupap
```

### docker

You can run a new docker container by calling
```
docker run -p 8123:80 --name bupap [-it|--detach] valgarf/bupap:latest
```

## First login

The first start will take a short while to create testdata. 
Afterwards you should be able to see a webpage on `http://127.0.0.1:8123`

On standard configuration you can log in using:
```
Username: admin
Password: admin
```

Passwords of all the other users are their username as well, for example you can log in using `cmarmo` / `cmarmo`.

