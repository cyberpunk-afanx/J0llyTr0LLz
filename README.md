# J0llyTr0LLz
automation for primary binary analysis

### REMEMBER

INSTALL MODES___.TTF

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

1. sudo apt install python3-pyqt5
2. sudo apt install upx
3. sudo apt-get install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential
4. python3 -m pip install --upgrade pip
5. pip install hashlib
6. pip install zlib-state
7. pip install python-magic
8. pip install jsonlib

### RECOMENDATION

git clone repository to root directory (~/) and create alias at .zshrc (last line):

`$ sudo nano .zshrc`

This is at last line:

`alias J0llyTr0LLz="python3 ~/J0llyTr0LLz/main.py"`

CYBERPUNK AFANX
