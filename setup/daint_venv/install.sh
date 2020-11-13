#!/bin/bash

version=sn_1.0
env_file=env.daint.sh
dst_dir=./venv

# versions
fv3config_url="git+git://github.com/VulcanClimateModeling/fv3config.git@2212b33a2ec8e2e05df10e1c9ca0f1815d4f9a8d"
gt4py_url="git+git://github.com/VulcanClimateModeling/gt4py.git@workshop"
fv3util_url="git+git://github.com/VulcanClimateModeling/fv3gfs-util.git@7c1367348037474711da454ca3dc5b50bf79e17d"
cuda_version=cuda102

# module environment
source ./env.sh
source ./env/machineEnvironment.sh
source ./env/${env_file}

# echo commands and stop on error
set -e
set -x

# setup virtual env
if [ -d ${dst_dir} ] ; then /bin/rm -rf ${dst_dir} ; fi
python3 -m venv ${dst_dir}
source ${dst_dir}/bin/activate

pip install --upgrade pip
pip install --upgrade wheel

# installation of standard packages
pip install numpy
pip install matplotlib
pip install cupy-${cuda_version}
pip install ipykernel ipyparallel

# installation of our packages
pip install ${fv3config_url}
pip install ${gt4py_url}#egg=gt4py[${cuda_version}]
python -m gt4py.gt_src_manager install
pip install ${fv3util_url}

pip freeze > requirements_`date +"%Y-%m-%d-%H:%M"`.txt

module load jupyter-utils
kernel-create -n workshop

deactivate

# add note when activated
cat >> ${dst_dir}/bin/activate <<EOF1

# echo module environment
echo "Note: this virtual env has been created on `hostname` using the folowing module environment:"
cat <<'EOF'
EOF1
cat ./env/${env_file} >> ${dst_dir}/bin/activate
cat >> ${dst_dir}/bin/activate <<EOF2
EOF

EOF2

echo "Now copy or append the jupyterhub.env file to your ~/jupyterhub.env file and fire up JupyterHub"
# done
exit 0

