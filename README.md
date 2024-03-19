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

以上操作确认没问题后建议卸载重装pip
sudo apt purge python3-pip
sudo apt autoremove
sudo apt install python3-pip
sudo apt-get install python3.7-distutils
wyy@ubuntu:~/Desktop$ pip --version
pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.7)
```



### ModuleNotFoundError: No [module](https://so.csdn.net/so/search?q=module&spm=1001.2101.3001.7020) named ‘apt_pkg’

```
# 重新安装python3-apt
sudo apt remove python3-apt
sudo apt autoremove  # 此命令慎用，可以先不输入它，看能否解决问题
sudo apt autoclean
sudo apt install python3-apt
```















检查工具链版本

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

```
sudo apt-get install gcc
sudo apt-get install make
sudo apt-get install perl
```


安装依赖库

```
sudo apt-get install m4 flex bison
```


安装python依赖

```
sudo apt-get install python3-setuptools python3.7-dev libssl-dev
sudo apt-get install python3.7-distutils
pip3 install pyparsing==2.4.6
pip3 install hypothesis
```


编译安装OpenSSL

```
openssl version
使用默认1.1.1版本，安装成功。
```

安装GMP

GMP是一个提供高精度算术的开源软件库，支持对有符号整数、有理数和浮点数进行运算。

下载地址，选择5.1.3。解压：

```
tar -xvf gmp-5.1.3.tar.bz2
移动到usr/local/src/下
```

```
sudo mv gmp-5.1.3 /usr/local/src/
cd /usr/local/src/gmp-5.1.3
写入配置
```

```
sudo ./configure
```

```
sudo make 
sudo make install
```





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
编辑libpbc.conf
sudo vi /etc/ld.so.conf.d/libpbc.conf
# /usr/local/lib
sudo ldconfig
```



```
unzip charm-dev.zip 

移动

sudo mv charm-dev /usr/local/src/

进入目录并配置

cd /usr/local/src/charm-dev
sudo ./configure.sh

编译并安装

sudo make
sudo make install
```

```
cd /usr/local/lib
sudo rm libgmp*
sudo apt --fix-broken install
```



```
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair

group2 = PairingGroup('SS512')

g = group2.random(G1)
g = group2.random(G2)
```



snap问题解决办法:

1、查看安装详情，命令如下：

```
snap changes
1
```

如图：

ID=7的进程是我之前安装失败的。

2、清除当前安装，然后再重新安装，命令如下：

```
snap abort 7
```

```
ocean@ubuntu:~$ service network restart
Failed to restart network.service: Unit network.service not found.
ocean@ubuntu:~$ service network-manager restart 
```

