# Workshop on Domain-Specific Languages for Performance-Portable Weather and Climate Models

Material of the workshop held together with NOAA in 2020

## Setup on Orion

1. ```ssh <user>@orion-login.hpc.msstate.edu``` (log on to Orion)
2. `git clone https://github.com/VulcanClimateModeling/dsl_workshop.git workshop` (check out the repository for the workshop)
3. Add the line `if [ -f ~/workshop/setup/jupyter_env ] ; then source ~/workshop/setup/jupyter_env ; fi` to the file `.bashrc` just before the line `if [ -z "$PS1" ]; then return; fi`
4. `exec bash` (make sure current `.bashrc` is active)
5. Check `gcc --version` is 8.3.0 and `python --version` is 7.5.0
6. `cd workshop` (go to workshop directory)
7. `source ./setup/setup_venv` (install virtual environment, install Python packages, install IPython kernel, setup IPyParallel profile for MPI)

Important: At the end of the workshop you will want to remove the modification to your `~/.bashrc` again, if you continue to use the Orion system.

## Connect to Jupyter on Orion

1. Point your browser to https://orion-ood.hpc.msstate.edu/
2. Click "Jupyter Notebook" under the "Interactive Apps" dropdown menu
3. Configure your session (Account Name = "gfdlhires", Partition Name = "development") and launch you session.
4. Once the session has started, click "Connect to Jupyter"
5. The material for the workshop is under `workshop/notebooks`
6. Check you setup by executing the `Check-Setup.ipynb` notebook
