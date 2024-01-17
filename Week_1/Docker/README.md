# Intro To Docker

## What is Docker?
Docker is a set of platform as a service products that use virtualisation to deliver software in packages called containers.
Containers are isolated from one another and bundle their own software, libraries and config files. 
Containers can communicate with each other through well-defined channels.
A single host can run multiple Containers.
Containers run in complete isolation such that a single host could have multiple versions of the same application or for example a database.

### Why do we use Docker?
In data Engineering, we can use Docker within our data pipeline. A simple example would involve a Docker container with a python script, which consumes a csv file and pushes that data to a PostgreSQL db. 

### What is a Docker Image
A Docker image can be thought of as a snapshot of our container. An image contains all the instructions needed to reproduce the container on another host. 

### Why care about Docker
* Reproducability
* Local Experiments
* Integration tests (within CICD pipeline)
* Run pipelines on Cloud(AWS, Kns)
* Spark
* Serverless (AWS Lambda) - we can define env as Docker image

## What are the basic Docker commands?
* docker run -> Runs a Docker container with the image provided
    Examples:
    1. docker run hello-world -> runs the hello-world image
    2. docker run -it ubuntu bash -> runs the ubuntu image in interactive mode. Everything after image name is passed to container. In this case, we are running bash command after image created.
    3. docker run -it python:3.9 -> pass tag 3.9 to image
    Page explaining difference between CMD and ENTRYPOINT https://www.cloudbees.com/blog/understanding-dockers-cmd-and-entrypoint-instructions
    -e : flag for environmental variables
    -v : mount a volume to the container. This can be a working directory on the current machine. Relative paths can be used. 
* docker build -t test:pandas . -> Builds a docker image with the Dockerfile present in cwd
    Full set of params: https://docs.docker.com/engine/reference/commandline/build/
    -t is shorthand for --tag  in the name:tag format
    build will utilise CACHED images if possible to speed up overall build
* docker create network -> Creates a new network. Bridge networks are isolated networks on a single Engine installation. If you want to create a network that spans multiple Docker hosts each running an Engine, you must enable Swarm mode, and create an overlay network. To read more about overlay networks with Swarm mode 
    full params = https://docs.docker.com/engine/reference/commandline/network_create/#usage


** Docker Compose
***What is Docker Compose?
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services. Then, with a single command, you create and start all the services from your configuration.

*** What features does Docker Compose provice?
The key features of Compose that make it effective are:
* Have multiple isolated environments on a single host
* Preserve volume data when containers are created
* Only recreate containers that have changed
* Support variables and moving a composition between environments