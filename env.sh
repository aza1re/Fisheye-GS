#!/bin/bash

echo "Setting CUDA_HOME environment variable..."
export CUDA_HOME="/usr/local/cuda-11.8"
echo 'export CUDA_HOME="/usr/local/cuda-11.8"' >> ~/.bashrc
echo 'export PATH="$CUDA_HOME/bin:$PATH"' >> ~/.bashrc

echo "Adding Miniconda to PATH..."
export PATH="$HOME/miniconda3/bin:$PATH"
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc

conda init bash

echo "Setting up Conda environment..."
conda env create --file environment.yml

echo "Updating Conda..."
conda update -n base -c defaults conda -y

echo "Configuring Git..."
git config --global user.email "u3645252@connect.hku.hk"
git config --global user.name "aza1re"

echo "Restart your terminal and run: conda activate fisheye_gs"