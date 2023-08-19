# J0llyTr0LLz
automation for primary binary analysis

### ABOUT

J0llyTr0LLz shows a number of characteristics of the executable file, ELF FORMAT ONLY.

1.  File type
2.  File size
3.  Endianness
4.  Architecture
5.  Binary Type (ELF, PE, Mach-O)
6.  HEX-view
7.  Hashes
8.  Information about ELF
9.  Protection types
10. ROPGadgets and find gadgets

### J0llyTroLLz contains:

1. readelf -h programm
2. file
3. checksec (pwntool)
4. ROPGadget
5. HEX-View
6. Hashes

### INSTALL

sudo apt install python3-pyqt5
sudo apt install upx
sudo apt-get install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential
python3 -m pip install --upgrade pip
pip install hashlib
pip install zlib-state
pip install python-magic
pip install jsonlib
