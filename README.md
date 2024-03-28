```
Our program is running on an Ubuntu 20.04 system
The python version requires 3.7 to be installed
Here are the commands to install some environments
```

```
sudo apt install vim
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7      # 安装Python3.7
sudo apt install python3.7-venv # 安装3.7建立虚拟环境virtualenv
sudo apt install python3.7-dev  # 安装Python3.7-dev(开发版)
sudo update-alternatives --display python
```

```
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# update-alternatives: using /usr/bin/python3.8 to provide /usr/bin/python (python) in auto mode

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2

# update-alternatives: using /usr/bin/python3.9 to provide /usr/bin/python (python) in auto mode

sudo update-alternatives --config python

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
# update-alternatives: using /usr/bin/python3.8 to provide /usr/bin/python (python) in auto mode


sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
# update-alternatives: using /usr/bin/python3.9 to provide /usr/bin/python (python) in auto mode

sudo update-alternatives --config python3

#After the above operations to confirm that there is no problem, we recommend uninstalling and reinstalling pip
sudo apt purge python3-pip
sudo apt autoremove
sudo apt install python3-pip
sudo apt-get install python3.7-distutils
wyy@ubuntu:~/Desktop$ pip --version
pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.7)
```



### If there is an error ：ModuleNotFoundError: No module named ‘apt_pkg’
```
# 重新安装python3-apt
sudo apt remove python3-apt
sudo apt autoremove  # 此命令慎用，可以先不输入它，看能否解决问题
sudo apt autoclean
sudo apt install python3-apt
```

Checking the toolchain version
```
gcc -v 
make -v
perl -v
```

```
gcc  -> 9.4.0
make -> 4.2.1
perl -> 5.30.0
```



If not then install
```
sudo apt-get install gcc
sudo apt-get install make
sudo apt-get install perl
```


Installation of dependent libraries
```
sudo apt-get install m4 flex bison
```


Install python dependencies

```
sudo apt-get install python3-setuptools python3.7-dev libssl-dev
sudo apt-get install python3.7-distutils
pip3 install pyparsing==2.4.6
pip3 install hypothesis
```

Compile and Install OpenSSL
```
openssl version
# Using the default version 1.1.1, the installation was successful.
```

Installation of GMP
GMP is an open source software library that provides high-precision arithmetic, supporting operations on signed integers, rational numbers, and floating point numbers.
For the download address https://gmplib.org/download/gmp/ , select 5.1.3. unzip:
```
tar -xvf gmp-5.1.3.tar.bz2
```

Move under usr/local/src/
```
sudo mv gmp-5.1.3 /usr/local/src/
cd /usr/local/src/gmp-5.1.3
```
Write Configuration
```
sudo ./configure
```

```
sudo make 
sudo make install
```

Compile and install PBC
Download address https://crypto.stanford.edu/pbc/download.html , select 0.5.14
Unzip, move
```
tar -xvf pbc-0.5.14.tar.gz 
sudo mv pbc-0.5.14 /usr/local/src/
cd /usr/local/src/pbc-0.5.14
sudo ./configure
sudo make
sudo make install
```

```
sudo touch /etc/ld.so.conf.d/libpbc.conf
```
Edit libpbc.conf
```
sudo vi /etc/ld.so.conf.d/libpbc.conf
# /usr/local/lib
sudo ldconfig
```

Install charm
Download
```
git clone https://github.com/JHUISI/charm.git
```
Or download the zip package and unzip it
```
unzip charm-dev.zip 
```

```
sudo mv charm-dev /usr/local/src/
```
Enter the catalog and configure
```
cd /usr/local/src/charm-dev
sudo ./configure.sh
```
Compile and install
```
sudo make
sudo make install
```

```
cd /usr/local/lib
sudo rm libgmp*
sudo apt --fix-broken install
```


If the installation is successful, test the following code in the python environment
```
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair

group2 = PairingGroup('SS512')

g = group2.random(G1)
g = group2.random(G2)
```
All packages used in the code need to be pip installed.

The ABE directory holds the attribute-based encryption scheme
```
ABE
├── __init__.py
├── __pycache__
├── ac17
│   ├── __init__.py
│   └── __pycache__
├── bsw07
│   └── __init__.py
├── cgw15
│   └── __init__.py
├── msp
│   ├── __init__.py
│   └── __pycache__
└── waters11
    └── __init__.py
```

The experiment directory holds the code for our experiments.
```
experiment
├── exp1.py
├── exp2.py
├── exp3.py
├── plt1.py
├── plt2.py
├── plt3.py
└── tools.py
```

The satisfaction directory holds the satisfaction data for the LPESCP, PIPO, and WMMF scenarios in Experiment 2
For the sake of aesthetics in the drawing, we have done a zoom-in process
```
satisfy
├── LPESCP.txt
├── PIPO.txt
├── WMMF.txt
├── deflation.py
├── processed_LPESCP.txt
├── processed_PIPO.txt
└── processed_WMMF.txt
```


The Scheduling directory holds the three energy scheduling algorithms LPESCP, PIPO, and WMMF
```
Scheduling
├── LPESCP.py
├── PIPO.py
├── WMMF.py
└── __pycache__
```


The scheme_result and scheme directories store the result data of the searchable encryption scheme in Experiment 3 and the algorithm program, respectively.
```
scheme_result
├── CBEKS.txt
├── CBSE.txt
├── PAUKS.txt
├── lightweight_peaks.txt
├── paeks.txt
├── peks.txt
└── user-friendly-PAEKS.txt

schemes
├── CBEKS.py
├── CBSE.py
├── PAUKS.py
├── __pycache__
├── abe.py
├── lightweight_peaks.py
├── paeks.py
├── peks.py
└── user-friendly-PAEKS.py

```