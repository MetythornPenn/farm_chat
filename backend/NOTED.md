- python -m venv env

- source env/bin/activate

- mkdir src && cd src

- pip install -r requirements.txt (copy from project leader)

- mkdir core db

- touch .env main

- config postgres with fastapi using orm sqlalchemy

- config alembic for db migration 
    - alembic init 
    - alembic revision --autogenerate -m "first commit" 
    - alembic upgrade head (to migrate model to database)
    - create data model and then run : alembic revision --autogenerate -m "create user & blog tables" (create table from class models : user & blog)
    - alembic upgrade head (to migrate model to database)

- create table models with sqlalchemy

- pydantic schema for user registration

- dependency injection to get a db session

- pawssword hashing


config tensorflow :
1. install cuda 
- sudo apt update
    -  Error : copy error to search in google (stack overflow ) 
- sudo apt install nvidia-cuda-toolkit
- nvcc --version
- sudo wget -O /etc/apt/preferences.d/cuda-repository-pin-600 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
- sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
- sudo add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
- sudo apt update
- sudo apt install cuda : if error follow this 
    - wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
    -   sudo dpkg -i cuda-keyring_1.0-1_all.deb
    -   sudo apt update
    -   sudo apt upgrade
    -   sudo apt install libnvidia-extra-530
    -   sudo apt install cuda
- echo 'export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}' >> ~/.bashrc
- nvcc --version
- nvidia-smi
- pip3 install tensorflow==2.4.0
- sudo apt update
- sudo apt install cudatool-kit-11.6



Sareoun Z1Data (Consultant), [24 Oct 2023 at 9:00:25 AM]:
1. api/v1/merchants
2. api/v1/merchants?location=lat,lng
3. api/v1/merchants?name=merchant_name
4. api/v1/merchants?location=lat,long&name=merchant_name

Objective for today
1. defind  schema for merchants get request paramater
2. defind schema for merchants get respond attributes
3. defind request errros response



[backend source code](https://github.com/renaldyhidayatt/ecomfastapireact)

[backend 2](https://github.com/Olukeye/fastapi-shop-app)