We conduct simulations using the Charm-crypto cryptography library based on the Python language to evaluate the effectiveness and efficiency of the LPESCP model.

Our program is running on the Ubuntu 20.04 system.

The python version requires 3.7 to be installed. 

Notice that, all packages used in the code need to be installed by using the command "pip install xxx".(实验中所需要用到的包都需要用pip install xxx安装)


### 1. Install python3.7(安装python3.7)
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7      # 安装Python3.7
sudo apt install python3.7-venv # 安装3.7建立虚拟环境virtualenv
sudo apt install python3.7-dev  # 安装Python3.7-dev(开发版)
sudo update-alternatives --display python
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# update-alternatives: using /usr/bin/python3.8 to provide /usr/bin/python (python) in auto mode

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2

# update-alternatives: using /usr/bin/python3.9 to provide /usr/bin/python (python) in auto mode

sudo update-alternatives --config python
```

After the above operations being confirmed that there is no problem, we recommend uninstalling and reinstalling pip.
```
sudo apt purge python3-pip
sudo apt autoremove
sudo apt install python3-pip
sudo apt-get install python3.7-distutils
```

If there is an error ：ModuleNotFoundError: No module named ‘apt_pkg’, python3-apt should be reinstalled.
```
# 重新安装python3-apt
sudo apt remove python3-apt
sudo apt autoremove  # 此命令慎用，可以先不输入它，看能否解决问题
sudo apt autoclean
sudo apt install python3-apt
```
### 2. Install the Charm-crypto cryptography library(安装Charm-crypto密码学库)

#### 2.1 Checking the toolchain version(检查工具链版本)
```
gcc -v 
make -v
perl -v
```
If gcc, make and perl have been installed, the version number will be showed as follows:
```
gcc  -> 9.4.0
make -> 4.2.1
perl -> 5.30.0
```

Inversely, gcc, make and perl should be installed.(如果没有则安装)
```
sudo apt-get install gcc
sudo apt-get install make
sudo apt-get install perl
```

#### 2.2 Install dependent libraries(安装依赖库)
```
sudo apt-get update
sudo apt-get install m4 flex bison
```

#### 2.3 Install python dependencies(安装python依赖)
```
sudo apt-get install python3-setuptools python3.7-dev libssl-dev
sudo apt-get install python3.7-distutils
pip3 install pyparsing==2.4.6
pip3 install hypothesis
```

### 3. Install GMP(安装GMP)


GMP is an open source software library that provides high-precision arithmetic, supporting operations on signed integers, rational numbers, and floating point numbers.
The download address is https://gmplib.org/download/gmp/ (GMP是一个提供高精度算术的开源软件库，支持对有符号整数、有理数和浮点数进行运算。 下载地址为https://gmplib.org/download/gmp/ )
#### 3.1 Download and unzip the version 5.1.3(下载并解压版本5.1.3)
```
tar -xvf gmp-5.1.3.tar.bz2
```
#### 3.2  Move the unzipped gmp-5.1.3 to usr/local/src/(移动到usr/local/src/下)
```
sudo mv gmp-5.1.3 /usr/local/src/
cd /usr/local/src/gmp-5.1.3
```


#### 3.3  Write configuration(写入配置)
```
sudo ./configure
```


#### 3.4  Install(安装)
```
sudo make 
sudo make install
```

### 4. Install PBC(安装PBC)
This step is similar to step 3 of the installation of GMP.
Download address is https://crypto.stanford.edu/pbc/download.html and the version is 0.5.14(下载地址https://crypto.stanford.edu/pbc/download.html 选择0.5.14) 
#### 4.1 Unzip and install PBC(安装PBC)
```
tar -xvf pbc-0.5.14.tar.gz 
sudo mv pbc-0.5.14 /usr/local/src/
cd /usr/local/src/pbc-0.5.14
sudo ./configure
sudo make
sudo make install
sudo touch /etc/ld.so.conf.d/libpbc.conf
sudo vi /etc/ld.so.conf.d/libpbc.conf
```

#### 4.2  Write(写入以下语句)
```
/usr/local/lib
```
#### 4.3 Conduct the following command(执行以下命令)
```
sudo ldconfig
```



### 5. Install charm(安装charm)
#### 5.1 Download(下载)
```
git clone https://github.com/JHUISI/charm.git
```

#### 5.2  Move(移动)
```
sudo mv charm-dev /usr/local/src/
```

#### 5.3 Enter the catalog and configure(进入目录并配置)
```
cd /usr/local/src/charm-dev
sudo ./configure.sh
```

#### 5.4 Compile and install(编译并安装)
```
sudo make
sudo make install
```


If there is a series of problems such as apt unavailable after reboot, network card loading failure and so on.(如果出现重启后apt不可用、网卡加载失败等一系列问题，执行以下命令)
```
cd /usr/local/lib
sudo rm libgmp*
sudo apt --fix-broken install
```


If the installation is successful, test the following code in the python environment.(安装成功，使用以下python代码进行测试)
```
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
group2 = PairingGroup('SS512')
g = group2.random(G1)
g = group2.random(G2)
```


### 6. Experimental simulations(实验仿真)
Simulations are conducted using the Charm-crypto cryptography library based on the Python language to evaluate the effectiveness and efficiency of the LPESCP model. In the simulation setup, the parameter θ is set to 0.8, KWspace={1, 2, 3, normal, urgent}, EI={(1,2), (2,3), (3,4), (4,5), (5,6)}, and we consider a scenario with Dnum power consumers (0<Dnum<20) and Snum power suppliers (Snum=20-Dnum), that is, a total of 20 users. Three experiments are conducted: Experiment 1-3.

The Experiment directory holds the three Experiment exp1.py, exp2.py, and exp3.py.
```
Experiment
├── exp1.py
├── exp2.py
├── exp3.py
└── tools.py
```

#### 6.1 Experiment 1: exp1.py(实验1：exp1.py)
In Experiment 1, 500 random evaluation groups are conducted to demonstrate the effectiveness of the proposed LPESCP model, that is, the ability to supply and consume power efficiently while considering data confidentiality and data utility, as well as priority and fairness. In each group, the keyword of each user is randomly selected from  KWspace; the keyword corresponding emergency coefficient is randomly selected from the keyword corresponding interval in EI; the weight of each user is randomly generated, as are the power demand of each power consumer and maximum power supply of each power supplier in KW·h. 

#### 6.2 Experiment 2: exp2.py(实验2：exp2.py)
In Experiment 2, the proposed LPESCP model are compared with two other priority-based scheduling algorithms, including weighted max-min fairness (WMMF) and priority-in-priority-out (PIPO), with the same parameter setting method used in Experiment 1 with 500 evaluation groups. The comparison metric is the global satisfaction degree of all users. When applying the WMMF strategy, energy is allocated in multiple rounds based on users' weights that are greater than zero until the available energy is distributed. In each allocation round, energy is allocated according to each user's respective weight ratio (the ratio of each user's weight to the sum of the weights of all users participating in this round) so that energy can be allocated to all users. Users whose needs are not met continue to participate in the next round. Users who are allocated more energy than they need only receive an energy supply equal to the demanded power, and the excess energy will be accumulated for allocation to other users in the next round. Through its unique allocation mechanism, the WMMF strategy comprehensively considers users with different weights, satisfying the needs of users with significant weights and ensuring that the minimum needs of each user are met, thereby balancing priority and fairness to some extent. In the PIPO strategy, power consumers and suppliers are sorted according to their priority, from highest to lowest. High-priority power consumers receive the requested energy first, and only then energy is allocated to low-priority consumers. Similarly, low-priority power suppliers supply energy before high-priority power suppliers are allowed to provide energy. Thus, the higher the priority of power consumers, the earlier the energy is allocated, whereas the lower the priority of power suppliers, the earlier the energy is supplied. 

The Scheduling directory holds the three energy scheduling algorithms LPESCP, PIPO, and WMMF.
```
Scheduling
├── LPESCP.py
├── PIPO.py
├── WMMF.py
```


#### 6.3 Experiment 3: exp3.py(实验3：exp3.py)
In Experiment 3, 500 random evaluation groups are constructed to compare the Lightweight_PAEKS method used in the LPESCP model with four other PEKS schemes in terms of the time overhead measured in milliseconds (ms). In each group, two pairs of public-private keys are randomly generated to simulate the sender and receiver, with keywords of both sender and receiver being set to "urgent".

The Schemes directory holds the five peks algorithms CBEKS, CBSE, PAUKS, Lightweight_PAEKS and PAEKS.
```
Schemes
├── CBEKS.py
├── CBSE.py
├── PAUKS.py
├── Lightweight_PAEKS.py
└── PAEKS.py
```