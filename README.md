```
Our program is running on the Ubuntu 20.04 system
The python version requires 3.7 to be installed
Here are the commands to install some environments
```

```
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
```

After the above operations to confirm that there is no problem, we recommend uninstalling and reinstalling pip
```
sudo apt purge python3-pip
sudo apt autoremove
sudo apt install python3-pip
sudo apt-get install python3.7-distutils
```


If there is an error ：ModuleNotFoundError: No module named ‘apt_pkg’
```
# 重新安装python3-apt
sudo apt remove python3-apt
sudo apt autoremove  # 此命令慎用，可以先不输入它，看能否解决问题
sudo apt autoclean
sudo apt install python3-apt
```

检查工具链版本
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

如果没有则安装
If not then install
```
sudo apt-get install gcc
sudo apt-get install make
sudo apt-get install perl
```

安装依赖库
Installation of dependent libraries
```
sudo apt-get update
sudo apt-get install m4 flex bison
```

安装python依赖
Install python dependencies
```
sudo apt-get install python3-setuptools python3.7-dev libssl-dev
sudo apt-get install python3.7-distutils
pip3 install pyparsing==2.4.6
pip3 install hypothesis
```

编译安装OpenSSL
Compile and Install OpenSSL
```
openssl version
```
使用默认1.1.1版本，安装成功。
Using the default version 1.1.1, the installation was successful.

安装GMP
GMP是一个提供高精度算术的开源软件库，支持对有符号整数、有理数和浮点数进行运算。
下载地址https://gmplib.org/download/gmp/，选择5.1.3。解压：
Installation of GMP
GMP is an open source software library that provides high-precision arithmetic, supporting operations on signed integers, rational numbers, and floating point numbers.
For the download address https://gmplib.org/download/gmp/ , select 5.1.3. unzip:
```
tar -xvf gmp-5.1.3.tar.bz2
```

移动到usr/local/src/下
Move under usr/local/src/
```
sudo mv gmp-5.1.3 /usr/local/src/
cd /usr/local/src/gmp-5.1.3
```

写入配置
Write Configuration
```
sudo ./configure
```

安装
install
```
sudo make 
sudo make install
```

编译安装PBC
下载地址https://crypto.stanford.edu/pbc/download.html，选择0.5.14
解压,移动
进入目录，配置
编译
安装
在/etc/ld.so.conf.d/目录下新建一个libpbc.conf,
Compile and install PBC
Download address https://crypto.stanford.edu/pbc/download.html , select 0.5.14
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
write
```
/usr/local/lib
```
```
sudo ldconfig
```

安装charm
下载
Install charm
Download
```
git clone https://github.com/JHUISI/charm.git
```
或者下载压缩包，解压
Or download the zip package and unzip it
```
unzip charm-dev.zip 
```
移动
move
```
sudo mv charm-dev /usr/local/src/
```
进入目录并配置
Enter the catalog and configure
```
cd /usr/local/src/charm-dev
sudo ./configure.sh
```
编译并安装
Compile and install
```
sudo make
sudo make install
```

如果出现重启后apt不可用，网卡加载失败等一系列问题。执行以下命令
If there is a series of problems such as apt unavailable after reboot, network card loading failure and so on.
```
cd /usr/local/lib
sudo rm libgmp*
sudo apt --fix-broken install
```

安装成功，使用以下python代码进行测试
If the installation is successful, test the following code in the python environment
```
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
group2 = PairingGroup('SS512')
g = group2.random(G1)
g = group2.random(G2)
```

实验中所需要用到的包都需要用pip install xxx安装
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


We conduct simulations using the Charm-crypto cryptography library based on the Python language to evaluate the effectiveness and efficiency of the LPESCP model. In the simulation setup, the parameter θ is set to $0.8$, and we consider a scenario with Dnum power consumers (0<Dnum<20) and Snum power suppliers ($\textit{Snum}=20-\textit{Dnum}$), i.e., a total of $20$ users. We conduct three experiments, i.e., \emph{Experiment} $1$ -- $3$.
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

In Experiment 1, we conduct 500 random evaluation groups to demonstrate the effectiveness of our proposed LPESCP model, i.e., the ability to supply and consume power efficiently while considering data confidentiality and data utility, as well as priority and fairness. In each group, the weight of each user is randomly generated, as are the demanded power consumption of each power consumer and the maximum power supply of each power supplier in KW·h. 

In Experiment 2, we compare our proposed LPESCP model with two other priority-based scheduling algorithms, including weighted max-min fairness (WMMF)  and priority-in-priority-out (PIPO) with the same parameter settings used in Experiment 1 with 500 evaluation groups, and the metric for comparison is the global satisfaction degree of all users. When applying the WMMF strategy, energy will be allocated in multiple rounds based on users' weights which are greater than 0 until the available energy is distributed. In each allocation round, energy is allocated according to each user's respective weight ratio (the ratio of each user's weight to the sum of weights of all users participated in this round), so all users can be allocated energy. Among them, users who fail to meet their needs will continue to participate in the next round. Users who are allocated more energy than they needs will only receive energy supply equal to their demanded power, and the excess energy will be accumulated in the next round for allocation to other users. Through its unique allocation mechanism, the WMMF strategy achieves comprehensive consideration of users with different weights, meeting the needs of users with significant weights and ensuring that the minimum needs of each user are met, thereby balancing priority and fairness to some extent. In the PIPO strategy, power consumers and suppliers are sorted in accordance with their priority from highest to lowest. The high-priority power consumers receive the demand energy first and only then energy is allocated to the low-priority ones. Similarly, the lower-priority power suppliers supply energy before the high-priority power suppliers are allowed to provide energy. In short, the higher the priority of the power consumers, the earlier the energy is allocated, while the lower the priority of the power suppliers, the earlier the energy is supplied. 

The satisfaction directory holds the satisfaction data for the LPESCP, PIPO, and WMMF scenarios in Experiment 2
For the sake of aesthetics in the drawing, we have done a zoom-in process


The Scheduling directory holds the three energy scheduling algorithms LPESCP, PIPO, and WMMF
```
Scheduling
├── LPESCP.py
├── PIPO.py
├── WMMF.py
└── __pycache__
```

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




In Experiment 3, we also conduct 500 random evaluation groups to compare our proposed LPESCP model with four other PEKS schemes in terms of time overhead measured in milliseconds (ms). The same as Experiment 1, in each group, the demanded energy of each power consumer, the maximum energy supply of each power supplier, and the weight of each user are randomly generated.

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