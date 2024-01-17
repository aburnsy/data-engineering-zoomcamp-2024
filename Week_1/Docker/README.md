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


## Important Notes on Docker Build
When you run the docker build command, the Docker client gathers all files that need to be sent to the Docker daemon, so it can build the image. This 'package' of files is called the context.

### What files and directories are added to the context?
The context contains all files and subdirectories in the directory that you pass to the docker build command. For example, when you call
```
docker build img:tag dir_to_build
```
the context will be everything inside dir_to_build.

If the Docker client does not have sufficient permissions to read some of the files in the context, you get the error checking context: 'can't stat ' <FILENAME> error.

### How can this problem be solved?

#### Solution 1
Move your Dockerfile, together with the files that are needed to build your image, to a separate directory separate_dir that contains no other files/subdirectories. When you now call docker build img:tag separate_dir, the context will only contain the files that are actually required for building the image. (If the error still persists that means you need to change the permissions on your files so that the Docker client can access them).

#### Solution 2
Exclude files from the context using a .dockerignore file. Most of the time, this is probably what you want to be doing.
From the official Docker documentation:
> Before the docker CLI sends the context to the docker daemon, it looks for a file named .dockerignore in the root directory of the context. If this file exists, the CLI modifies the context to exclude files and directories that match patterns in it.

### Solution 3
We could build without a context, using a remote file [Relevant Link](https://docs.docker.com/build/building/context/#how-to-build-without-a-context)

## Docker Compose
### What is Docker Compose?
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services. Then, with a single command, you create and start all the services from your configuration.

### What features does Docker Compose provice?
The key features of Compose that make it effective are:
* Have multiple isolated environments on a single host
* Preserve volume data when containers are created
* Only recreate containers that have changed
* Support variables and moving a composition between environments

## Docker Ignore
A .dockerignore is a configuration file that describes files and directories that you want to exclude when building a Docker image.
By specifying files not to be included in the context in .dockerignore, the size of the image can be reduced. Reducing the size of the Docker image has the following advantages:
* Faster speed when doing Docker pull/push.
* Faster speed when building Docker images.

More information on Docker ignore files can be found [here](https://shisho.dev/blog/posts/how-to-use-dockerignore/)
