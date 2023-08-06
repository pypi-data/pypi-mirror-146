
# **NEAT**
**NEar-Axis opTimisation**

![GitHub](https://img.shields.io/github/license/rogeriojorge/neat)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/rogeriojorge/NEAT/CI)
[![Documentation Status](https://readthedocs.org/projects/neat-docs/badge/?version=latest)](https://neat-docs.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/rogeriojorge/NEAT/branch/main/graph/badge.svg?token=8515A2RQL3)](https://codecov.io/gh/rogeriojorge/NEAT)

NEAT is a python framework that is intended to find optimized stellarator configurations for fast particle confinement using the near-axis expansion formalism.
The magnetic field is calculated using the code [pyQSC](https://github.com/landreman/pyQSC/), the particle orbits are traced using the code [gyronimo](https://github.com/prodrigs/gyronimo) (included as a submodule) and the optimization is done using the code [simsopt](https://github.com/hiddenSymmetries/).

To download clone NEAT including its submodules, use the following command:

```bash
git clone --recurse-submodules https://github.com/rogeriojorge/NEAT.git
```
or, alternatively, after downloading this repository, in the root folder, run:

```bash
git submodule init
git submodule update
```

# Usage

NEAT could be run either directly by installing the requirements pyQSC, gyronimo and SIMSOPT, and then compiling the [NEAT.cc](src/NEAT.cc) file in the *[src](src/)* folder, or using the provided Docker image. The usage of the Docker image is recommended.

# Installation

Make sure that you have installed all of the python packages listed in the file [requirements.txt](requirements.txt). A simple way of doing so is by running

```
pip install -r requirements.txt
```

## CMake

On NEAT's root directory run

```
python setup.py build
python setup.py install --user
```

To clean the build folders and all folders not being tracked by GIT, run

```
git clean -d -f -x
```

## Docker

This section explains how to build the docker container for NEAT. It can be used to compile gyronimo, install pyQSC, simsopt and compile NEAT in a docker image directly.

### Using Docker Hub

The easiest way to get simsopt docker image which comes with NEAT and all of its dependencies such as gyronimo and VMEC pre-installed is to use Docker Hub. After installing docker, you can run the simsopt container directly from the simsopt docker image uploaded to Docker Hub.

```
docker run -it --rm rjorge123/neat # Linux users, prefix the command with sudo
```

The above command should load the terminal that comes with the NEAT docker container. When you run it first time, the image is downloaded automatically, so be patient. You should now be able to import the module from python:

```
python3
import neat
```

### Build locally

To build the image locally, instead of downloading from DockerHub, you can use the commands below:


1. Build the docker image by running the `docker build` command in the repo root directory:
   ```bash
   docker build -t neat -f docker/Dockerfile.NEAT .
   ```
This process yields an image with roughly 2 GB and may take minute to build.

2. Run the docker image using the `docker run` command including your results folder:
    ``` bash
    docker run -v "$(pwd)/results:/home/results" neat
    ```

3. Your results folder will be populated with NEAT's results

4. In case the input parameters are changed, there is no need to rebuild the image, just include your inputs file after the docker run command
    ``` bash
    docker run -v "$(pwd)/inputs.py:/home/neat/src/inputs.py" -v "$(pwd)/results:/home/neat/results" neat
    ```

#### Optional
If you want to run NEAT and continue working in the container, instead run the docker image using the flag **-it** and end with **/bin*bash**
    ```bash
    docker run -it --entrypoint /bin/bash neat
    ```

## Development

### Requirements
To run NEAT, you'll need the following libraries

* gsl
* boost
* gcc10

and the python packages specified in [requirements.txt](requirements.txt) .

### Install gyronimo
In NEAT's root folder, run

```bash
cd external/gyronimo
mkdir build
cd build
CXX=g++ cmake -DCMAKE_INSTALL_PREFIX=../../../build -DSUPPORT_OPENMP=ON -DSUPPORT_VMEC=ON ../
cmake --build . --target install
```

If you want to build documentation with doxygen, run

```bash
cmake --build . --target doc
```


### Compile NEAT

Compilation is done in the src/ folder of the repo. The fields and metrics need to be compiled before compiling the main file NEAT.cc in the src/neatpp folder

#### Example on MacOS

```bash
cd src/neatpp

cd fields_NEAT
g++-mp-11 -O2 -Wall -std=c++20 equilibrium_stellna_qs.cc -I$(pwd)/../../build/include -I$(pwd)/.. -c

cd ../metrics_NEAT
g++-mp-11 -O2 -Wall -std=c++20 metric_stellna_qs.cc -I$(pwd)/../../build/include -I$(pwd)/.. -c

cd ../neatpp
```

Compile the serial version (no parallelization)
```bash
g++ -O2 -Wall -shared -std=c++20 -undefined dynamic_lookup  NEAT.cc ../neatpp/fields_NEAT/equilibrium_stellna_qs.o ../metrics_NEAT/neatpp/metric_stellna_qs.o -o NEAT.so $(python3 -m pybind11 --includes) -I/opt/local/include -L/opt/local/lib -lgsl -L$(pwd)/../../build/lib -lgyronimo -I$(pwd)/.. -I$(pwd)/../../build/include -Wl,-rpath $(pwd)/../../build/lib -Wl,-rpath $(pwd)/..
```

Compile the OpenMP version
```bash
g++ -O2 -Wall -std=c++20 -fopenmp NEAT_openmp.cc ../neatpp/fields_NEAT/equilibrium_stellna_qs.o ../neatpp/metrics_NEAT/metric_stellna_qs.o -o NEAT_openmp -I/opt/local/include -L/opt/local/lib -lgsl -L$(pwd)/../../build/lib -lgyronimo -I$(pwd)/.. -I$(pwd)/../../build/include -Wl,-rpath $(pwd)/../../build/lib
```

The number of threads can be changed using the command

```bash
export OMP_NUM_THREADS=[number of threads]
```

#### Example on Linux

```bash
cd src/neatpp

cd fields_NEAT
g++-10 -O2 -Wall -std=c++20 equilibrium_stellna_qs.cc -I$(pwd)/../../build/include -I$(pwd)/.. -c

cd ../metrics_NEAT
g++-10 -O2 -Wall -std=c++20 metric_stellna_qs.cc -I$(pwd)/../../build/include -I$(pwd)/.. -c

cd ../neatpp
g++-10 -std=c++2a -fPIC -shared NEAT.cc -o NEAT.so $(python3 -m pybind11 --includes) -L/usr/lib -lgsl -L$(pwd)/../../build/lib -lgyronimo -I$(pwd)/.. -I$(pwd)/../../build/include  -Wl,-rpath $(pwd)/../../build/lib
```

### Install SIMPLE
In NEAT's root folder, run

```bash
cd external/simple
mkdir build
cd build
CXX=g++ cmake -DCMAKE_INSTALL_PREFIX=../../../build ../
cmake --build . --target install
cp simple.x ../../../build/bin
```

The last command copies the executable of SIMPLE to the folder build/bin

### Install VMEC
First, in the external/vmec folder, change the file cmake_config_file.json to your machine using an example from the cmake/machines templates. Here is a template for MacOS running gcc11

```
{
    "comment": "This configuration file works on a macbook on which gcc and netcdf have been installed using macports.",
    "cmake_args": [
           "-DCMAKE_C_COMPILER=mpicc",
           "-DCMAKE_CXX_COMPILER=mpicxx",
           "-DCMAKE_Fortran_COMPILER=mpif90",
           "-DNETCDF_INC_PATH=/opt/local/include",
           "-DNETCDF_LIB_PATH=/opt/local/lib",
           "-DCMAKE_Fortran_FLAGS=-fallow-argument-mismatch"]
}
```

Then, in NEAT's root folder, run

```bash
cd external/vmec
pip install numpy
pip install cmake scikit-build ninja f90wrap
python setup.py build_ext
python setup.py install
```

To test VMEC's installation, you can run

```
python -c "import vmec; print('success')"
```

# FAQ

## pybind11 not found by cmake

Please use the following command to install ```pybind11[global]``` instead of ```pybind11```

```
pip install "pybind11[global]"
```