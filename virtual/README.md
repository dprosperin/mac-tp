You need to make a link so that the qemu program can be run from everywhere. Copy and past the line in a terminal (in the current folder), root access required:

```
sudo ln -s `pwd`/qemu-system-arm /usr/local/bin/qemu-system-arm
```
You can check the correct link with:

```
ls -l /usr/local/bin/qemu-system-arm
```
It should point to a correct location!! If you made a mistake (wrong directory), just remove the wrong link:
```
sudo rm /usr/local/bin/qemu-system-arm
```

qemu depends in the libc6:
```
sudo apt install libc6
```

The python script have dependancies with PyQt5 and posix_ipc:

```
sudo apt install python3-pyqt5 python3-pip python3-dev
pip3 install posix_ipc
```

## Extra

Qemu can be compiled from sources:
```
git clone https://github.com/mbriday/qemu.git
cd qemu
git checkout -b stm32f303 origin/stm32f303
mkdir build
cd build
../configure --enable-debug --target-list="arm-softmmu" --disable-werror --disable-libssh
time make -j8
```
