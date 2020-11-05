# Workshop on Domain-Specific Languages for Performance-Portable Weather and Climate Models

Material of the workshop held together with NOAA in 2020

## Setup on Orion

1. Log on to orion with `ssh <user>@orion-login.hpc.msstate.edu`
2. Check out the repository for the workshop `git clone https://github.com/VulcanClimateModeling/dsl_workshop.git workshop`
3. Copy the environment `cp workshop/setup/jupyter_env ~/.jupyter_env`
4. Add the line `source /home/<user>/.jupyter_env` to the file `.bashrc` just before the line `if [ -z "$PS1" ]; then return; fi`
5. Make sure current `.bashrc` is active by typing `exec bash`
6. Check `gcc --version` is 8.3.0
7. Load a current version of Python with `module load python/3.7.5`
8. Install GT4Py and setup Python virtual environment as Jupyter kernel with `source workshop/setup/setup_venv`

## Connect to Jupyter on Orion

1. Point your browser to https://orion-ood.hpc.msstate.edu/
2. Click "Jupyter Notebook" under the "Interactive Apps" dropdown menu
3. Configure your session (Account Name = "gfdlhires", Partition Name = "development") and launch you session.
4. Once the session has started, click "Connect to Jupyter"
5. The material for the workshop is under `workshop/notebooks`

