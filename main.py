# from email.policy import default
# from fileinput import filename
import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
import mainwindow, about, strings, seccomp, syscall_table, jtdisasm
import hashlib
import zlib
import magic
import json
import binascii
from capstone import *


class JollyTrollz(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    filename = ''
    barray = bytearray()
    
    default_os_abi = ["No extensions or unspecified", "Hewlett-Packard HP-UX", "NetBSD", "GNU", "<unknown: 4>", "<unknown: 5>", "Sun Solaris", "AIX", "IRIX", "FreeBSD", "Compaq TRU64 UNIX", "Novell Modesto", "Open BSD", "Open VMS", "Hewlett-Packard Non-Stop Kernel", "Amiga Research OS", "The FenixOS highly scalable multi-core OS", "Nuxi CloudABI", "Stratus Technologies OpenVOS"]
    
    default_type = ["NONE/No file type", "REL/Relocatable file", "EXEC/Executable file", "DYN/Shared object file", "CORE/Core file", "LOOS/Operating system-specific", "HIOS/Operating system-specific", "LOPROC/Processor-specific", "HIPROC/Processor-specific"]
    
    default_machine = ["No machine", "AT&T WE 32100", "SPARC", "Intel 80386", "Motorola 68000", "Motorola 88000", "Intel MCU", "Intel 80860", "MIPS I Architecture", "IBM System/370 Processor", "MIPS RS3000 Little-endian", "Reserved for future use", "Reserved for future use", "Reserved for future use", "Reserved for future use", "Hewlett-Packard PA-RISC", "Reserved for future use", "Fujitsu VPP500", "Enhanced instruction set SPARC", "Intel 80960", "PowerPC", "64-bit PowerPC", "IBM System/390 Processor", "IBM SPU/SPC", "Reserved for future use", "Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use", "NEC V800", "Fujitsu FR20", "TRW RH-32", "Motorola RCE","ARM 32-bit architecture (AARCH32)", "Digital Alpha", "Hitachi SH", "SPARC Version 9", "Siemens TriCore embedded processor", "Argonaut RISC Core, Argonaut Technologies Inc.", "Hitachi H8/300", "Hitachi H8/300H", "Hitachi H8S", "Hitachi H8/500", "Intel IA-64 processor architecture", "Stanford MIPS-X", "Motorola ColdFire", "Motorola M68HC12", "Fujitsu MMA Multimedia Accelerator", "Siemens PCP", "Sony nCPU embedded RISC processor", "Denso NDR1 microprocessor", "Motorola Star*Core processor", "Toyota ME16 processor", "STMicroelectronics ST100 processor", "Advanced Logic Corp. TinyJ embedded processor family", "AMD x86-64 architecture", "Sony DSP Processor", "Digital Equipment Corp. PDP-10", "Digital Equipment Corp. PDP-11", "Siemens FX66 microcontroller", "STMicroelectronics ST9+ 8/16 bit microcontroller", "STMicroelectronics ST7 8-bit microcontroller", "Motorola MC68HC16 Microcontroller", "Motorola MC68HC11 Microcontroller", "Motorola MC68HC08 Microcontroller", "Motorola MC68HC05 Microcontroller", "Silicon Graphics SVx", "STMicroelectronics ST19 8-bit microcontroller", "Digital VAX", "Axis Communications 32-bit embedded processor", "Infineon Technologies 32-bit embedded processor", "Element 14 64-bit DSP Processor", "Logic 16-bit DSP Processor", "Donald Knuth's educational 64-bit processor", "Harvard University machine-independent object files", "SiTera Prism", "Atmel AVR 8-bit microcontroller", "Fujitsu FR30", "Mitsubishi D10V", "Mitsubishi D30V", "NEC v850", "Mitsubishi M32R", "Matsushita MN10300", "Matsushita MN10200", "picoJava", "OpenRISC 32-bit embedded processor", "ARC International ARCompact processor (old spelling/synonym: EM_ARC_A5)", "Tensilica Xtensa Architecture", "Alphamosaic VideoCore processor", "Thompson Multimedia General Purpose Processor", "National Semiconductor 32000 series", "Tenor Network TPC processor", "Trebia SNP 1000 processor", "STMicroelectronics (www.st.com) ST200 microcontroller", "Ubicom IP2xxx microcontroller family", "MAX Processor", "National Semiconductor CompactRISC microprocessor", "Fujitsu F2MC16", "Texas Instruments embedded microcontroller msp430", "Analog Devices Blackfin (DSP) processor", "S1C33 Family of Seiko Epson processors", "Sharp embedded microprocessor", "Arca RISC Microprocessor", "Microprocessor series from PKU-Unity Ltd. and MPRC of Peking University", "eXcess: 16/32/64-bit configurable embedded CPU", "Icera Semiconductor Inc. Deep Execution Processor", "Altera Nios II soft-core processor", "National Semiconductor CompactRISC CRX microprocessor", "Motorola XGATE embedded processor", "Infineon C16x/XC16x processor", "Renesas M16C series microprocessors", "Microchip Technology dsPIC30F Digital Signal Controller", "Freescale Communication Engine RISC core", "Renesas M32C series microprocessors", "Reserved for future use", "Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use", "Altium TSK3000 core", "Freescale RS08 embedded processor", "Analog Devices SHARC family of 32-bit DSP processors", "Cyan Technology eCOG2 microprocessor", "Sunplus S+core7 RISC processor", "New Japan Radio (NJR) 24-bit DSP Processor", "Broadcom VideoCore III processor", "RISC processor for Lattice FPGA architecture", "Seiko Epson C17 family", "The Texas Instruments TMS320C6000 DSP family", "The Texas Instruments TMS320C2000 DSP family", "The Texas Instruments TMS320C55x DSP family", "Texas Instruments Application Specific RISC Processor, 32bit fetch","Texas Instruments Programmable Realtime Unit", "Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use","Reserved for future use", "STMicroelectronics 64bit VLIW Data Signal Processor", "Cypress M8C microprocessor", "Renesas R32C series microprocessors","NXP Semiconductors TriMedia architecture family", "QUALCOMM DSP6 Processor","Intel 8051 and variants","STMicroelectronics STxP7x family of configurable and extensible RISC processors","Andes Technology compact code size embedded RISC processor family","Cyan Technology eCOG1X family","Dallas Semiconductor MAXQ30 Core Micro-controllers","New Japan Radio (NJR) 16-bit DSP Processor","M2000 Reconfigurable RISC Microprocessor","Cray Inc. NV2 vector architecture","Renesas RX family","Imagination Technologies META processor architecture","MCST Elbrus general purpose hardware architecture","Cyan Technology eCOG16 family","National Semiconductor CompactRISC CR16 16-bit microprocessor","Freescale Extended Time Processing Unit","Infineon Technologies SLE9X core","Intel L10M","Intel K10M","Reserved for future Intel use","ARM 64-bit architecture (AARCH64)","Reserved for future ARM use","Atmel Corporation 32-bit microprocessor family","STMicroeletronics STM8 8-bit microcontroller","Tilera TILE64 multicore architecture family","Tilera TILEPro multicore architecture family","Xilinx MicroBlaze 32-bit RISC soft processor core","NVIDIA CUDA architecture","Tilera TILE-Gx multicore architecture family","CloudShield architecture family","KIPO-KAIST Core-A 1st generation processor family","KIPO-KAIST Core-A 2nd generation processor family","Synopsys ARCompact V2","Open8 8-bit RISC soft processor core","Renesas RL78 family","Broadcom VideoCore V processor","Renesas 78KOR family","Freescale 56800EX Digital Signal Controller (DSC)","Beyond BA1 CPU architecture","Beyond BA2 CPU architecture","XMOS xCORE processor family","Microchip 8-bit PIC(r) family", "Reserved by Intel","Reserved by Intel","Reserved by Intel","Reserved by Intel","Reserved by Intel","KM211 KM32 32-bit processor","KM211 KMX32 32-bit processor","KM211 KMX16 16-bit processor","KM211 KMX8 8-bit processor","KM211 KVARC processor","Paneve CDP architecture family","Cognitive Smart Memory Processor","Bluechip Systems CoolEngine","Nanoradio Optimized RISC","CSR Kalimba architecture family","Zilog Z80","Controls and Data Services VISIUMcore processor","FTDI Chip FT32 high performance 32-bit RISC architecture","Moxie processor family","AMD GPU architecture"]

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.openFile)
        self.killerUPX.clicked.connect(self.killUPX)
        self.actionGrep.triggered.connect(self.grepGad)
        self.actionAbout.triggered.connect(self.about)
        self.actionStrings.triggered.connect(self.strings)
        self.actionSeccomp_tools.triggered.connect(self.seccomp_func)
        self.actionSyscall_table.triggered.connect(self.syscall_func)
        self.actionJTDisasm.triggered.connect(self.jtDisasm_func)

    def openFile(self):
        file = QtWidgets.QFileDialog.getOpenFileName()
        if(len(file[0]) != 0):
            self.filename = str(file[0])
            self.openedFile.setText(self.filename)
            with open(self.filename, 'rb') as tmp:
                self.barray = bytearray(tmp.read())
            self.firstAnalys()

    def firstAnalys(self):
        self.filetype.clear()
        self.filesize.clear()
        self.endianness.clear()
        self.architecture.clear()
        self.type.clear()
        self.textEditHex.clear()
        self.textEditFromHex.clear()
        self.listWidgetHashes.clear()
        self.listWidgetReadElf.clear()
        self.grepGadget.clear()
        self.ropgadgets.clear()
        self.countGatget.clear()
        self.textEditFileAbout.clear()
        self.checksec.clear()
        
        md5_hash = hashlib.md5()
        md5_hash.update(self.barray)
        self.listWidgetHashes.addItem("MD5 " + md5_hash.hexdigest())

        sha1_hash = hashlib.sha1()
        sha1_hash.update(self.barray)
        self.listWidgetHashes.addItem("SHA1 " + sha1_hash.hexdigest())

        sha256_hash = hashlib.sha256()
        sha256_hash.update(self.barray)
        self.listWidgetHashes.addItem("SHA256 " + sha256_hash.hexdigest())

        sha512_hash = hashlib.sha512()
        sha512_hash.update(self.barray)
        self.listWidgetHashes.addItem("SHA512 " + sha512_hash.hexdigest())

        crc32_hash = hex(zlib.crc32(self.barray))
        self.listWidgetHashes.addItem("CRC32 " + crc32_hash)

        mime = magic.Magic(mime=True)
        self.filetype.setText(mime.from_file(self.filename))

        self.filesize.setText(str(os.path.getsize(self.filename)) + " " + "bytes")

        if(self.barray[4] == 1 or self.barray[236] == 0x4C):
            self.architecture.setText("32-bit")
        elif(self.barray[4] == 2):
            self.architecture.setText("64-bit")
        
        if(self.barray[5] == 1):
            self.endianness.setText("little-endian")
        elif(self.barray[5] == 2):
            self.endianness.setText("big-endian")
        else:
            self.endianness.setText("non-endian")

        if((chr(self.barray[1]) + chr(self.barray[2])) == "EL"):
            self.type.setText("ELF")
        elif((chr(self.barray[0]) + chr(self.barray[1])) == "MZ"):
            self.type.setText("PE")
            self.endianness.setText("little-endian")
        elif(self.barray[0] == 0xFA and self.barray[1] == 0xDE):
            self.type.setText("Mach-O")
        else:
            self.type.setText("unknown format")
        self.toHex()      

    def toHex(self):
        tmp = ""
        self.textEditHex.clear()
        for i in range(len(self.barray)):
            if(i%8 == 0 and i != 0):
                tmp += "\n"
            if(self.barray[i] < 16):
                tmp += "0" + hex(self.barray[i])[2:] + " "
            else:
                tmp += hex(self.barray[i])[2:] + " "
        self.textEditHex.setText(tmp)
        self.fromHex()
    
    def fromHex(self):
        tmp = ""
        self.textEditFromHex.clear()
        for i in range(len(self.barray)):
            if(i%16 == 0 and i != 0):
                tmp += "\n"
            tmp += chr(self.barray[i])
        self.textEditFromHex.setText(tmp)   
        self.readelf()

    def readelf(self):
        self.listWidgetReadElf.clear()

        magic_str = "Magic: "
        for i in range(16):
            if(self.barray[i] < 16):
                magic_str += "0" + hex(self.barray[i])[2:] + " "
            else:
                magic_str += hex(self.barray[i])[2:] + " " 
        self.listWidgetReadElf.addItem(magic_str)

        class_str = "Class: "
        if(self.barray[4] == 1):
            class_str += "ELF32"
        elif(self.barray[4] == 2):
            class_str += "ELF64"
        self.listWidgetReadElf.addItem(class_str)

        data_str = "Data: "
        if(self.barray[5] == 1):
            data_str += "little-endian"
        elif(self.barray[5] == 2):
            data_str += "big-endian"
        else:
            data_str += "non-endian"
        self.listWidgetReadElf.addItem(data_str)

        version_str = "Version: " + str(self.barray[6])
        if(self.barray[6] == 1):
            version_str += " " + "(current)"
        elif(self.barray[6] == 0):
            version_str += " " + "(none)"
        self.listWidgetReadElf.addItem(version_str)

        os_abi_str = "OS/ABI: " + "UNIX - "
        if(self.barray[7] > 0x12):
            os_abi_str += "<unknown: " + hex(self.barray[7])[2:] + ">"
        else:
            for i in range(len(self.default_os_abi)):
                if(self.barray[7] == i):
                    os_abi_str += self.default_os_abi[i]
                    break
        self.listWidgetReadElf.addItem(os_abi_str)

        abi_version_str = "ABI Version: " + hex(self.barray[8])[2:]
        self.listWidgetReadElf.addItem(abi_version_str)

        type_str = "Type: " 
        if(self.barray[16] == 0 and self.barray[17] != 0xFE):
            type_str += self.default_type[0]
        elif(self.barray[16] == 1):
            type_str += self.default_type[1]
        elif(self.barray[16] == 2):
            type_str += self.default_type[2]
        elif(self.barray[16] == 3):
            type_str += self.default_type[3]
        elif(self.barray[16] == 4):
            type_str += self.default_type[4]
        elif(self.barray[16] == 0x00 and self.barray[17] == 0xFE):
            type_str += self.default_type[5]
        elif(self.barray[16] == 0xFF and self.barray[17] == 0xFE):
            type_str += self.default_type[6]
        elif(self.barray[16] == 0x00 and self.barray[17] == 0xFF):
            type_str += self.default_type[7]
        elif(self.barray[16] == 0xFF and self.barray[17] == 0xFF):
            type_str += self.default_type[8]
        self.listWidgetReadElf.addItem(type_str)

        machine_str = "Machine: "
        for i in range(len(self.default_machine)):
                if(self.barray[18] == i):
                    machine_str += self.default_machine[i]
                    break
        if(self.barray[i] == 243):
            machine_str += "RISC-V"
        if(self.barray[18] > 224 and self.barray[18] < 243):
            machine_str += "NONE"
        self.listWidgetReadElf.addItem(machine_str)

        version_str_2 = "Version: " + str(self.barray[20])
        self.listWidgetReadElf.addItem(version_str_2)

        entry_point_address_str = "Entry point address: " + "0x" + hex(self.barray[25])[2:] + hex(self.barray[24])[2:]
        self.listWidgetReadElf.addItem(entry_point_address_str)

        self.fileAbout()

    def fileAbout(self):
        self.textEditFileAbout.clear()

        info = ""
        os.system("file " + self.filename + " > file_temp.txt")
        with open("file_temp.txt", 'r') as tmp:
            temp_file = tmp.read()
        os.system("rm file_temp.txt")
        info += temp_file
        self.textEditFileAbout.setText(info)
        
        self.detectUPX()

    def detectUPX(self):
        if((chr(self.barray[236]) + chr(self.barray[237]) + chr(self.barray[238]) + chr(self.barray[239])) == "UPX!"):
            self.lineEditDectorUPX.setText("UPX HAS BEEN DETECTED !!!")
        else:
            self.lineEditDectorUPX.setText("< CLEAR >")

        self.checksection()

    def checksection(self):
        os.system("./checksec --file=" + self.filename + " --output=json" + " > tmp_checksec.json")
        check_res = ""
        with open('tmp_checksec.json', 'r') as tmp_json:
            doc_json = json.load(tmp_json)
        os.system("rm tmp_checksec.json")

        relro_str = "RELRO:\t\t" + doc_json[self.filename]['relro']
        canary_str = "CANARY:\t\t" + doc_json[self.filename]['canary']
        nx_str = "NX:\t\t" + doc_json[self.filename]['nx']
        pie_str = "PIE:\t\t" + doc_json[self.filename]['pie']
        rpath_str = "RPATH:\t\t" + doc_json[self.filename]['rpath']
        symbols_str = "SYMBOLS:\t\t" + doc_json[self.filename]['symbols']
        fortify_source_str = "FORTIFY SOURCE:\t" + doc_json[self.filename]['fortify_source']
        fortified_str = "FORTIFIED:\t" + doc_json[self.filename]['fortified']
        fortify_able_str = "FORTIFY-ABLE:\t" + doc_json[self.filename]['fortify-able']
        self.checksec.addItem(relro_str)
        self.checksec.addItem(canary_str)
        self.checksec.addItem(nx_str)
        self.checksec.addItem(pie_str)
        self.checksec.addItem(rpath_str)
        self.checksec.addItem(symbols_str)
        self.checksec.addItem(fortify_source_str)
        self.checksec.addItem(fortified_str)
        self.checksec.addItem(fortify_able_str)

        self.ropGadgets()

    def ropGadgets(self):
        self.ropgadgets.clear()
        os.system("python3 ROPgadget.py --binary " + self.filename + " > gadgets.txt")
        with open("gadgets.txt", 'r') as tmp:
            tmp_gadgets = tmp.read()
        os.system("rm gadgets.txt")
        str_gadgets = tmp_gadgets.split("\n")
        for i in range(2, len(str_gadgets)-3):
            self.ropgadgets.addItem(str_gadgets[i])
        self.countGatget.setText("Unique gadgets found: " + str(self.ropgadgets.count()))

    def killUPX(self):
        if(len(self.filename) > 0 and len(self.barray) > 0):
            os.system("upx -d " + self.filename)
            self.openFile()
    
    def grepGad(self):
        if(len(self.grepGadget.text()) == 0):
            self.ropgadgets.clear()
            self.ropGadgets()
        else:
            textReg = self.grepGadget.text()
            self.countGatget.clear()
            reg = QtCore.QRegExp(textReg)
            tmp_gadget = []
            for i in range(self.ropgadgets.count()):
                pos = reg.indexIn(self.ropgadgets.item(i).text(),0)
                while pos != -1:
                    find_string = self.ropgadgets.item(i).text()[pos : pos + reg.matchedLength()]
                    tmp_gadget.append(self.ropgadgets.item(i).text())
                    pos += reg.matchedLength()
                    pos = reg.indexIn(self.ropgadgets.item(i).text(), pos)
            self.ropgadgets.clear()
            for i in range(len(tmp_gadget)):
                self.ropgadgets.addItem(tmp_gadget[i])
            self.countGatget.setText("Unique gadgets found: " + str(self.ropgadgets.count()))
    
    def about(self):
        self.about = AboutApp()
        self.about.show()
    
    def strings(self):
        if(len(self.filename) != 0):
            os.system("strings " + self.filename + " > tmp_strings.txt")
            self.strings = StringsApp()
            self.strings.show()
    
    def seccomp_func(self):
        if(len(self.filename) != 0):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("seccomp-tool wait action\n you have to check terminal and enter values")
            msgBox.setWindowTitle("ATTENTION")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('[*] seccomp-tool wait action')
            os.system("./$pwd/seccomp-tools/bin/seccomp-tools dump " + self.filename + " > seccomp_tmp.txt")
            self.seccomp = SeccompApp()
            self.seccomp.show()
    
    def syscall_func(self):
        self.syscll = SyscallHelpApp()
        self.syscll.show()
    
    def jtDisasm_func(self):
        self.jtd = JTDisasmApp()
        self.jtd.show()


class AboutApp(QtWidgets.QWidget, about.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(467, 841)
        
class StringsApp(QtWidgets.QWidget, strings.Ui_Form):
    result = ""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.strings()
        self.actionGrepStrings.triggered.connect(self.grepStr)

    def strings(self):
        with open("tmp_strings.txt", 'r') as tmp:
            str_tmp = tmp.read()
        os.system("rm tmp_strings.txt")
        self.result = ""
        self.result = str_tmp.split("\n")
        self.showStrings()
    
    def showStrings(self):
        for i in range(len(self.result)):
            self.listWidget.addItem(self.result[i])
    
    def grepStr(self):
        if(len(self.lineEdit.text()) == 0):
            self.listWidget.clear()
            self.showStrings()
        else:
            textReg = self.lineEdit.text()
            reg = QtCore.QRegExp(textReg)
            tmp_strings = []
            for i in range(self.listWidget.count()):
                pos = reg.indexIn(self.listWidget.item(i).text(),0)
                while pos != -1:
                    find_string = self.listWidget.item(i).text()[pos : pos + reg.matchedLength()]
                    tmp_strings.append(self.listWidget.item(i).text())
                    pos += reg.matchedLength()
                    pos = reg.indexIn(self.listWidget.item(i).text(), pos)
            self.listWidget.clear()
            for i in range(len(tmp_strings)):
                self.listWidget.addItem(tmp_strings[i])
        
class SeccompApp(QtWidgets.QWidget, seccomp.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.seccomp_function()
    
    def seccomp_function(self):
        all = []
        with open("seccomp_tmp.txt", 'r') as tmp:
            tmp_read = tmp.read()
        os.system("rm seccomp_tmp.txt")
        # self.listWidget.addItem("line ")
        for i in range(len(tmp_read.split("\n"))):
            if(tmp_read.split("\n")[i] == "================================="):
                self.listWidget.addItem(" line  CODE  JT   JF      K")
                for j in range(i+1, len(tmp_read.split("\n"))):
                    self.listWidget.addItem(tmp_read.split("\n")[j])
                break

class SyscallHelpApp(QtWidgets.QWidget, syscall_table.Ui_Form):
    columns = ['NR','syscall name','references','rax','arg0 (rdi)','arg1 (rsi)','arg2 (rdx)','arg3 (r10)','arg4 (r8)', 'arg5 (r9)']

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.x86_table()
        self.x86_64_table()
        self.arm_32_bit_EABI_table()
        self.arm_64_table()

    def x86_table(self):
        self.tableWidget86.clear()
        self.tableWidget86.setColumnCount(len(self.columns))
        self.tableWidget86.setHorizontalHeaderLabels(self.columns) 
        with open("./syscall_table/x86.txt",'r') as tmp:
            read_tmp = tmp.read()
        tmp_1 = read_tmp.split("\n")
        self.tableWidget86.verticalHeader().setVisible(False)
        self.tableWidget86.setRowCount(len(tmp_1))
        for i in range(len(tmp_1)):
            for j in range(len(tmp_1[i].split("\t"))):
                self.tableWidget86.setItem(i, j, QtWidgets.QTableWidgetItem(tmp_1[i].split("\t")[j]))

    def x86_64_table(self):
        self.tableWidget86_64.clear()
        self.tableWidget86_64.setColumnCount(len(self.columns))
        self.tableWidget86_64.setHorizontalHeaderLabels(self.columns) 
        with open("./syscall_table/x86_64.txt",'r') as tmp:
            read_tmp = tmp.read()
        tmp_1 = read_tmp.split("\n")
        self.tableWidget86_64.verticalHeader().setVisible(False)
        self.tableWidget86_64.setRowCount(len(tmp_1))
        for i in range(len(tmp_1)):
            for j in range(len(tmp_1[i].split("\t"))):
                self.tableWidget86_64.setItem(i, j, QtWidgets.QTableWidgetItem(tmp_1[i].split("\t")[j]))

    def arm_32_bit_EABI_table(self):
        self.tableWidgetarm32.clear()
        self.tableWidgetarm32.setColumnCount(len(self.columns))
        self.tableWidgetarm32.setHorizontalHeaderLabels(self.columns) 
        with open("./syscall_table/arm_32_bit_EABI.txt",'r') as tmp:
            read_tmp = tmp.read()
        tmp_1 = read_tmp.split("\n")
        self.tableWidgetarm32.verticalHeader().setVisible(False)
        self.tableWidgetarm32.setRowCount(len(tmp_1))
        for i in range(len(tmp_1)):
            for j in range(len(tmp_1[i].split("\t"))):
                self.tableWidgetarm32.setItem(i, j, QtWidgets.QTableWidgetItem(tmp_1[i].split("\t")[j]))

    def arm_64_table(self):
        self.tableWidgetarm64.clear()
        self.tableWidgetarm64.setColumnCount(len(self.columns))
        self.tableWidgetarm64.setHorizontalHeaderLabels(self.columns) 
        with open("./syscall_table/arm64.txt",'r') as tmp:
            read_tmp = tmp.read()
        tmp_1 = read_tmp.split("\n")
        self.tableWidgetarm64.verticalHeader().setVisible(False)
        self.tableWidgetarm64.setRowCount(len(tmp_1))
        for i in range(len(tmp_1)):
            for j in range(len(tmp_1[i].split("\t"))):
                self.tableWidgetarm64.setItem(i, j, QtWidgets.QTableWidgetItem(tmp_1[i].split("\t")[j]))

class JTDisasmApp(QtWidgets.QMainWindow, jtdisasm.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bytecode = bytearray()
        self.actionOpen.triggered.connect(self.openFile)
        self.actionDisassembly.triggered.connect(self.disasm)

    def openFile(self):
        file = QtWidgets.QFileDialog.getOpenFileName()
        if(len(file[0]) != 0):
            with open(file[0], 'rb') as tmp:
                barray = bytearray(tmp.read())
            self.bytecode = barray
            self.disasm()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Can't open file")
            msgBox.setWindowTitle("ATTENTION")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                return 0

    def disasm(self):
        TEXT_CS_ARCH = 0
        TEXT_CS_MODE = 0
        instr = ""
        self.listWidget.clear()

        if(self.comboBox.currentText() == 'ARCH_X86'):
            TEXT_CS_ARCH = CS_ARCH_X86
        elif(self.comboBox.currentText() == 'ARCH_ARM'):
            TEXT_CS_ARCH = CS_ARCH_ARM
        elif(self.comboBox.currentText() == 'ARCH_MIPS'):
            TEXT_CS_ARCH = CS_ARCH_MIPS
        elif(self.comboBox.currentText() == 'ARCH_PPC'):
            TEXT_CS_ARCH = CS_ARCH_PPC

        if(self.comboBox_2.currentText() == 'MODE_32'):
            TEXT_CS_MODE = CS_MODE_32
        elif(self.comboBox_2.currentText() == 'MODE_ARM'):
            TEXT_CS_MODE = CS_MODE_ARM
        elif(self.comboBox_2.currentText() == 'MODE_THUMB'):
            TEXT_CS_MODE = CS_MODE_THUMB
        elif(self.comboBox_2.currentText() == 'MODE_64'):
            TEXT_CS_MODE = CS_MODE_64
        elif(self.comboBox_2.currentText() == 'MODE_MIPS_32'):
            TEXT_CS_MODE = CS_MODE_MIPS32
        elif(self.comboBox_2.currentText() == 'MODE_MIPS_64'):
            TEXT_CS_MODE = CS_MODE_MIPS64
        elif(self.comboBox_2.currentText() == 'MODE_MIPS_32R6'):
            TEXT_CS_MODE = CS_MODE_MIPS32R6

        if(self.lineEdit.text().isdigit()):
            entryPoint = int(self.lineEdit.text())
        else:
            entryPoint = 0x400000

        try:
            md = Cs(TEXT_CS_ARCH, TEXT_CS_MODE)
            md.syntax = CS_OPT_SYNTAX_INTEL
            md.detail = True
            count = 0
            for i in md.disasm(self.bytecode, entryPoint):
                tmp_byte = str(binascii.hexlify(bytearray(i.bytes)))[2:]
                self.listWidget.addItem("0x{}:\t{}\t{}\t{}".format(i.address, tmp_byte[:len(tmp_byte)-1], i.mnemonic, i.op_str))
        except:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Can't disassembly")
            msgBox.setWindowTitle("ATTENTION")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                return 0
        self.toHex()
            
    def toHex(self):
        tmp = ""
        self.hexTextEdit.clear()
        for i in range(len(self.bytecode)):
            if(i%8 == 0 and i != 0):
                tmp += "\n"
            if(self.bytecode[i] < 16):
                tmp += "0" + hex(self.bytecode[i])[2:] + " "
            else:
                tmp += hex(self.bytecode[i])[2:] + " "
        self.hexTextEdit.setText(tmp)
        self.fromHex()
    
    def fromHex(self):
        tmp = ""
        self.fromHexTextEdit.clear()
        for i in range(len(self.bytecode)):
            if(i%16 == 0 and i != 0):
                tmp += "\n"
            tmp += chr(self.bytecode[i])
        self.fromHexTextEdit.setText(tmp) 

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = JollyTrollz()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()