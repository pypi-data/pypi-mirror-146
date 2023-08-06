# Lisflood OS

This repository hosts source code of LISFLOOD model.
Go to [Lisflood OS page](https://ec-jrc.github.io/lisflood/) for more information.

Other useful resources

| **Project**         | **Documentation**                                         | **Source code**                                              |
| ------------------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| Lisflood            | [Model docs](https://ec-jrc.github.io/lisflood-model/)    | https://github.com/ec-jrc/lisflood-code (this repository)    |
|                     | [User guide](https://ec-jrc.github.io/lisflood-code/)     |                                                              |
| Lisvap              | [Docs](https://ec-jrc.github.io/lisflood-lisvap/)         | https://github.com/ec-jrc/lisflood-lisvap                    |
| Calibration tool    | [Docs](https://ec-jrc.github.io/lisflood-calibration/)    | https://github.com/ec-jrc/lisflood-calibration               |
| Lisflood Utilities  |                                                           | https://github.com/ec-jrc/lisflood-utilities                 |
| Lisflood Usecases   |                                                           | https://github.com/ec-jrc/lisflood-usecases                  |


## Notes for Release 3.2.0

This release includes the following changes:
- a new xarray reader for the water abstraction demand maps;
- a unit test to verify the functioning of the reader for the water abstraction maps;
- bug fixes and improvements to the caching function and the chunking function;
- improvements of the management of latitude and longitude grids to allow maximum precision of the reference system;
- improvements of the definition of the output variables.

All of the changes above improve the code capability to handle input and outputs.
The modelling of the hydrological processes has not been changed.

IMPORTANT NOTE: the results of the unit tests of this release are different from the results of the unit tests of the release 3.1.1. The differences are due exclusively to a different use of of the optional moduels (e.g. groundwatersmooth) within the .xml setttings file of the unit tests. When using the same settings of .xml file, and the same dataset, v3.1.1 and v3.2.0 provide the same results.

## Quick start

You can use conda environment to easily install dependencies.

* Install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
* Create a conda env named "lisflood" and install dependencies:

```bash
conda create --name lisflood python=3.7 -c conda-forge
conda activate lisflood
conda install -c conda-forge pcraster
```

* Install lisflood-model pypi package
```bash
pip install lisflood-model
```

Command above will also install the executable `lisflood` in the conda env, so that you can run LISFLOOD with the following:
```bash
lisflood /absolute_path/to/my/local/folder/TestCatchment/settings/cold_day_base.xml
```

You can also clone the repository which contains datasets to test the model.
Follow this instruction for a basic test (included in this repository under [tests/data/TestCatchment1](https://github.com/ec-jrc/lisflood-code/tree/master/tests/data/TestCatchment1))

* Clone the master branch of this repository (you need to have git installed on your machine).

```bash
git clone --single-branch --branch master https://github.com/ec-jrc/lisflood-code.git
```

* **Install requirements into a python 3 conda env**

```bash
conda create --name lisflood python=3.7 -c conda-forge
conda activate lisflood
conda install -c conda-forge pcraster
cd lisflood-code
pip install -r requirements.txt
```

If you don't use conda but a plain virtualenv, you need to install PCRaster and GDAL by your own and include its python interface in PYTHONPATH environment variable.
For details, please follow instruction on [official docs](http://pcraster.geo.uu.nl/getting-started/pcraster-on-linux/).


3. Compile the cython module kinematic_wave_parallel_tool

To compile this Cython module to enable OpenMP multithreading (parallel kinematic wave):

* Delete the files *.so (if any) in directory hydrological-modules  

* Inside the hydrological_modules folder, execute "python compile_kinematic_wave_parallel_tools.py build_ext --inplace"  

Important: the module has to be compiled on the machine where the model is run - the resulting binary is not portable.  

Then in the settings file the option "numberParallelThreadsKinematicWave" may take the following values:
    - "0"           : auto-detection of the machine/node's number of CPUs (all CPUs are used minus 1) (do not set it if other simulations are running on the same machine/node)
    - "1"           : serial execution (not parallel)
    - "2", "3", ... : manual setting of the number of parallel threads.
                      (if exceeding the number of CPUs, the option is set to "0") -->  
```xml
<textvar name="numCPUs_parallelKinematicWave" value="3"/>
```
4. Run a cold run for the test catchment

Now your environment should be set up to run lisflood. Try with a prepared settings file for one of the two test catchments:

```bash
python src/lisf1.py tests/data/TestCatchment/settings/cold_day_base.xml
```

If the command above successed without errors, producing dis.nc into tests/data/TestCatchment1/outputs folder, your lisflood installation was correct.

### Docker image

You can use the updated docker image to run lisflood, so without taking care to install dependencies on your system.

#### Pull image from repository:

```bash
docker pull jrce1/lisflood:latest
```

#### Run test catchments in image:

```bash
docker run -v /absolute_path/to/my/local/folder:/usecases jrce1/lisflood:latest usecases
```

After this command, you can find all files to run tests against catchments under the directory you mapped: `/absolute_path/to/my/local/folder/`

```
/absolute_path/to/my/local/folder/LF_ETRS89_UseCase
/absolute_path/to/my/local/folder/LF_lat_lon_UseCase
```

Now, you can run LISFLOOD as a docker container to test included catchments. Only thing you need to do is to map the test catchment folder to the container folder `input`, by using -v option. 

In the XML settings file, all paths are adjusted to be relative to the very same settings file, so you don't need to edit paths, as long as you keep same folders structure.


#### Execute lisflood with a Docker image:

```bash
docker run -v /absolute_path/to/my/local/folder/LF_ETRS89_UseCase:/input jrce1/lisflood /input/settings/cold.xml
```

Once LISFLOOD finished, you find reported maps in `/absolute_path/to/my/local/folder/LF_ETRS89_UseCase/out/` folder.

### Pypi packaged LISFLOOD

LISFLOOD is also distributed as a standard python package. You can install the pip package in your Python 3 virtualenv:

```bash
pip install lisflood-model
```

Command above will also install the executable `lisflood` in the virtualenv, so that you can run LISFLOOD with the following:

```bash
lisflood /absolute_path/to/my/local/folder/TestCatchment/settings/cold_day_base.xml
```

### IMPORTANT NOTE

Please note that there are known issues when installing the LISFLOOD code on Windows (source code and pypi package). We cannot provide Windows support and strongly recommend using LINUX to install the LISFLOOD code.
Windows users are recommended to execute LISFLOOD with a Docker image.



## Collaborate

If you find an issue in our code, please follow the [GitHub flow](https://guides.github.com/introduction/flow/) to propose your changes (Fork, commit your changes and ask for a Pull Request).
You are required to run unit tests during your development and before to propose a pull request.

To execute unit tests:

```bash
pytest tests/
```

Furthermore, before to propose a pull request, there are additional tests we ask you to execute: 

```bash
pytest tests/ -m "slow
```

These tests could take 30 minutes or several hours, depending on your machine.

You can find full description and implementation details at [Test documentation](https://ec-jrc.github.io/lisflood-code/4_annex_tests/) page.

**Note**: If yuor pull request is about a new feature you may want to integrate in LISFLOOD,
ensure to include tests with good coverage for it.

For more info about pytest, see [official website](https://docs.pytest.org/en/latest/).
