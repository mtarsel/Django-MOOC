#!/bin/bash

echo "Run as sudo"

echo"Updating repos..."

sudo apt-get install

mkdir ${HOME}/software-d-and-d 
cd ${HOME}/software-d-and-d

echo "Created directory software-d-and-d in the home directory"

echo "Creating virtual environment"

pip install virtualenv

virtualenv ${HOME}/software-d-and-d/venv --distribute

echo "Entering vm..."
source ${HOME}/software-d-and-d/venv/bin/activate

echo "Changing directory"

cd ${HOME}/software-d-and-d/dream-girlz

pwd

echo "Pulling code and installing packages..."

pip install django-toolbelt

git init

git clone https://github.com/mtarsel/dream-girlz.git

echo "#######################################"
echo "#######################################"
echo "##     IMPORTANT INFORMATION	   ##"
echo "##				   ##"
echo "##    To activate virtualenv:        ##"
echo "##				   ##"
echo "##    source venv/bin/activate	   ##"
echo "##				   ##"
echo "##    DONT FORGET TO DELETE OLD	   ##"
echo "##	   PROJECT		   ##"
echo "##				   ##"
echo "##	 You are now in		   ##"
echo "##				   ##"
echo "##    ~/software-d-and-d		   ##"
echo "##				   ##"
echo "##				   ##"
echo "#######################################"
echo "#######################################"
