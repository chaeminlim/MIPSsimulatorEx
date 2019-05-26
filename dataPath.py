from ALU import ALU
from readbinary import readbinary
from memoryAccess import MemoryAccess
from decodeAsm import decodeAssembly
import sys
import os
import time


def getRs(value):
    return (value & 0x03E00000) >> 21
def getRt(value):
    return (value & 0x001F0000) >> 16
def getRd(value):
    return (value & 0x0000F800) >> 11
def getShamt(value):
    return (value & 0x000007C0) >> 6
def getOffset(value):
    return value & 0x0000FFFF
def getAddress(value):
    return value & 0x03FFFFFF
def getFunct(value):
    return value & 0x0000003F
class dataPath:
    def __init__(self):
        self.Registers = [0 for _ in range(32)]
        self.Registers[29] = 0x7ffff1f8
        self.ProgramCounter = 0x00400000
        self.inst_log = []
        self.Registers_log = []
        self.R_type = ['add', 'sub', 'and', 'jr', 'sll', 'sra', 'srl', 'syscall', 'or',
                       'nor', 'xor', 'addu']


    def run(self, fileDirectory="", isAssembly = None):
        # 메모리 객체 생성
        self.Mem.stackMEM[0xff1f8] = 0x2

        if isAssembly == None:
            # 파일 읽어오기
            self.readBin.changeEndian(self.readBin.openreadfile(fileDirectory))
            # 4바이트 씩 나누어 리스트에 저장됨
            for i in range(2, len(self.readBin.codeList), 1):
                self.Mem.MEM(self.ProgramCounter + 0x24, self.readBin.codeList[i], 1, 2)  # 0x24부터 저장
                self.ProgramCounter += 4
                # 저장 후 프로그램 카운터 초기화
            self.ProgramCounter = 0x00400000

        if isAssembly == 1:
            self.decodeAssembly.fopen(fileDirectory)
            self.instList, a, _ = self.decodeAssembly.encode(self.Mem)
            for i in range(len(self.instList)):
                self.Mem.MEM(self.ProgramCounter + 0x24, self.instList[i], 1, 2)  # 0x24부터 저장
                self.ProgramCounter += 4

            self.ProgramCounter = 0x00400000

    def setup(self):

        self.Mem = MemoryAccess()
        self.F_ProgramCounter = 0x00400000

        for i in range(9):
            sys_list = [
                0x8fa40000, 0x27a50004,
                0x24a60004, 0x00041080,
                0x00c23021, 0x0c100009,
                0x00000000, 0x3402000a,
                0x0000000c]
            self.Mem.MEM(self.F_ProgramCounter,sys_list[i], 1 ,2)
            self.F_ProgramCounter += 4
        self.readBin = readbinary()
        self.decodeAssembly = decodeAssembly()


    def step(self, isAssembly=None):
            z = 1
            value = 0

            #alu 객체 생성
            alu = ALU()
            # 명령어 하나씩 읽어오기
            value = self.Mem.MEM(self.ProgramCounter, value, 0, 2)
            #log appending
            self.inst_log.append(value)
            list1 = []
            list1 = self.Registers[0:31]
            self.Registers_log.append(list1)

            # opCode를 해석
            opCode = self.readBin.checkOpcode(value)
            if opCode in self.R_type:  # r 타입일때

                rs = self.Registers[getRs(value)]
                rt = self.Registers[getRt(value)]
                rd = self.Registers[getRd(value)]

                if getFunct(value) == 8: #jr
                    self.ProgramCounter = self.Registers[31]
                    return 0
                    #continue
                elif getFunct(value) == 32: #if add
                    control = 0x8
                    self.Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
                elif getFunct(value) == 33: #addu
                    control = 0x8
                    self.Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
                elif getFunct(value) == 34: #sub
                    control = 0x9
                    self.Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
                elif getFunct(value) == 36: #and
                    control = 0xC
                    self.Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
                elif getFunct(value) == 37: #or
                    control = 0xD
                    self.Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
                elif getFunct(value) == 38: #xor
                    control = 0xE
                    self.Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
                elif getFunct(value) == 39: #nor
                    control = 0xF
                    self.Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
                elif getFunct(value) == 42: #slt
                    control = 8
                    self.Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
                elif getFunct(value) == 0: #sll
                    control = 0x1
                    shift_amt = getShamt(value)
                    self.Registers[getRd(value)] = alu.ALU_main(shift_amt, rt, control, z)
                elif getFunct(value) == 2: #srl
                    control = 0x2
                    shift_amt = getShamt(value)
                    self.Registers[getRd(value)] = alu.ALU_main(shift_amt, rt, control, z)
                elif getFunct(value) == 3: #sra
                    control = 0x3
                    shift_amt = getShamt(value)
                    self.Registers[getRd(value)] = alu.ALU_main(shift_amt, rt, control, z)
                elif getFunct(value) == 12: #syscall
                    if self.Registers[2] == 10:
                        print("end")
                        #break



            else:
                if opCode == "j":
                    if isAssembly==1:
                        address = getAddress(value)
                        self.ProgramCounter = (self.ProgramCounter & 0xF0000000) | ((address) << 2)
                        return 0
                    else:
                        address = getAddress(value)
                        self.ProgramCounter = (self.ProgramCounter & 0xF0000000) | ((address+9) << 2)
                        return 0

                    #continue
                #
                elif opCode == "jal":
                    address = getAddress(value)
                    self.Registers[31] = self.ProgramCounter + 4
                    if value == 0x0c100009 or isAssembly == 1:
                        self.ProgramCounter = (self.ProgramCounter & 0xF0000000) | ((address) << 2)
                    else:
                        self.ProgramCounter = (self.ProgramCounter & 0xF0000000) | ((address + 9) << 2)
                    return 0

                    #continue
                elif opCode == "beq":
                    rs = self.Registers[getRs(value)]
                    rt = self.Registers[getRt(value)]
                    offset = getOffset(value)
                    control =  0x9 #sub
                    if alu.ALU_main(rs, rt, control, z) == 0: #if same
                        self.ProgramCounter = self.ProgramCounter + (offset << 2)
                    elif alu.ALU_main(rs, rt, control, z) != 0:
                        self.ProgramCounter += 4
                    return 0
                    #continue
                elif opCode == "bne" :
                    rs = self.Registers[getRs(value)]
                    rt = self.Registers[getRt(value)]
                    offset = getOffset(value)
                    control = 0x9 # sub
                    if alu.ALU_main(rs, rt, control, z) != 0:  # if not same
                        self.ProgramCounter = self.ProgramCounter + (offset << 2)
                    elif alu.ALU_main(rs, rt, control, z) == 0:
                        self.ProgramCounter += 4
                    return 0
                    #continue

                elif opCode == "lw":

                    rs = self.Registers[getRs(value)]
                    offset = getOffset(value)
                    control = 0x8 # add
                    val = 0
                    self.Registers[getRt(value)] = self.Mem.MEM(alu.ALU_main(rs, offset, control, z), val, 0, 2)


                elif opCode == "sw":
                    rs = self.Registers[getRs(value)]
                    rt = self.Registers[getRt(value)]
                    offset = getOffset(value)
                    control = 0x8 #add
                    self.Mem.MEM(alu.ALU_main(rs, offset, control, z), rt, 1, 2)

                elif opCode == "addiu" :
                    control = 0x8 # add
                    rs = self.Registers[getRs(value)]
                    offset = getOffset(value)
                    self.Registers[getRt(value)] = rs + offset

                elif opCode == "ori" :
                    control = 0xD
                    rs = self.Registers[getRs(value)]
                    offset = getOffset(value)
                    self.Registers[getRt(value)] = alu.ALU_main(rs, offset, control, z)

                elif opCode == "xori" :
                    control = 0xE
                    rs = self.Registers[getRs(value)]
                    offset = getOffset(value)
                    self.Registers[getRt(value)] = alu.ALU_main(rs, offset, control, z)

                elif opCode == "lui" :
                    control = 0x1
                    offset = getOffset(value)
                    self.Registers[getRt(value)] = alu.ALU_main(16, offset, control, z)

            self.ProgramCounter += 4
            #time.sleep(0.5)
            #continue
    def decodeInstr(self, isAssembly = None):
        Memstart = 0x00400000

        if isAssembly == None:
            length = len(self.readBin.codeList) + 9
        elif isAssembly == 1:
            length = len(self.instList) + 9

        decodedList = []
        for i in range(length):
            instr_hex = self.Mem.MEM(Memstart, "", 0, 2)
            decodedLine = self.readBin.checkOpcode(instr_hex)
            if decodedLine in self.R_type:
                if decodedLine == "syscall":
                    decodedLine = decodedLine

                elif decodedLine == "jr":
                    decodedLine += " $" + str(getRs(instr_hex))

                elif decodedLine in ['sll', 'sra', 'srl']:
                    decodedLine += "$" + str(getRd(instr_hex)) + ","
                    decodedLine += "$" + str(getRt(instr_hex)) + ","
                    decodedLine +=  str(getShamt(instr_hex))

                else:
                    decodedLine += " $" + str(getRd(instr_hex)) + ", "
                    decodedLine += "$" + str(getRs(instr_hex)) + ", "
                    decodedLine += "$" + str(getRt(instr_hex))

            elif decodedLine == "jal" or decodedLine == "j":
                if isAssembly==1:
                    address = getAddress(instr_hex) * 4
                else:
                    address = getAddress(instr_hex) * 4
                    if (not address == 0x00400024):
                        address = getAddress(instr_hex)*4 + 0x24
                adrs = "0x%08X" % (address)
                decodedLine +=  " " + str(adrs)


            elif decodedLine == "lw" or decodedLine == "sw":
                offset = getOffset(instr_hex)
                if offset > 0x7fff:
                    offset -= 0x10000
                    #offset = (-offset) + (-offset)
                decodedLine += " $" + str(getRt(instr_hex)) +", "
                decodedLine +=  str(offset)
                decodedLine += "($" + str(getRs(instr_hex))+ ")"

            else:
                offset = getOffset(instr_hex)
                if offset >= 0x7fff:
                    offset -= 0x10000
                    #offset = (-offset) + (-offset)
                decodedLine += " $" + str(getRt(instr_hex)) + ", "
                decodedLine += "$" + str(getRs(instr_hex)) + ", "
                decodedLine +=str(offset)

            decodedList.append(decodedLine)
            Memstart += 0x4

        return decodedList
####for test#####
