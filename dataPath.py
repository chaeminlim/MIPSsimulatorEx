from ALU import ALU
from readbinary import readbinary
from memoryAccess import MemoryAccess
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
    def __init__(self, inst_number):
        self.Registers = [0 for _ in range(32)]
        self.Registers[29] = 0x7ffff1f8
        self.ProgramCounter = 0x00400000
        self.inst_log = []
        self.Registers_log = []

        if inst_number == 2:
            self.file_name = "binaries/as_ex02_logic.bin"
        elif inst_number == 3:
            self.file_name = "binaries/as_ex03_ifelse.bin"
        elif inst_number == 4:
            self.file_name = "binaries/as_ex04_fct.bin"

    def run(self):

        R_type = ['add', 'sub', 'and', 'jr', 'sll', 'sra', 'srl', 'syscall', 'or',
                  'nor', 'xor', 'addu']
        # 메모리 객체 생성
        Mem = MemoryAccess()
        Mem.stackMEM[0xff1f8] = 0x2
        # 파일 읽어오기
        readBin = readbinary()
        readBin.changeEndian(readBin.openreadfile(self.file_name))
        # 4바이트 씩 나누어 리스트에 저장됨

        value = 0
        self.F_ProgramCounter = 0x00400000

        for i in range(0, 9):
            sys_list = [
                0x8fa40000, 0x27a50004,
                0x24a60004, 0x00041080,
                0x00c23021, 0x0c100009,
                0x00000000, 0x3402000a,
                0x0000000c]
            Mem.MEM(self.F_ProgramCounter,sys_list[i], 1 ,2)
            self.F_ProgramCounter += 4

        for i in range(2, len(readBin.codeList), 1):
            Mem.MEM(self.ProgramCounter+0x24, readBin.codeList[i], 1, 2) #24부터 저장
            self.ProgramCounter += 4

        # 저장 후 프로그램 카운터 초기화
        self.ProgramCounter = 0x00400000
        #디코딩
        while True:
            z = 1
            #alu 객체 생성
            alu = ALU()
            # 명령어 하나씩 읽어오기
            value = Mem.MEM(self.ProgramCounter, value, 0, 2)
            #log appending
            self.inst_log.append(value)
            list1 = []
            list1 = self.Registers[0:31]
            self.Registers_log.append(list1)

            # opCode를 해석
            opCode = readBin.checkOpcode(value)
            if opCode in R_type:  # r 타입일때

                rs = self.Registers[getRs(value)]
                rt = self.Registers[getRt(value)]
                rd = self.Registers[getRd(value)]

                if getFunct(value) == 8: #jr
                    self.ProgramCounter = self.Registers[31]
                    continue
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
                        break



            else:
                if opCode == "j":
                    address = getAddress(value)
                    self.ProgramCounter = (self.ProgramCounter & 0xF0000000) | ((address + 9) << 2)
                    continue
                #
                elif opCode == "jal":
                    address = getAddress(value)
                    self.Registers[31] = self.ProgramCounter + 4
                    if value == 0x0c100009:
                        self.ProgramCounter = (self.ProgramCounter & 0xF0000000) | ((address) << 2)
                    else:
                        self.ProgramCounter = (self.ProgramCounter & 0xF0000000) | ((address + 9) << 2)
                    continue
                elif opCode == "beq":
                    rs = self.Registers[getRs(value)]
                    rt = self.Registers[getRt(value)]
                    offset = getOffset(value)
                    control =  0x9 #sub
                    if alu.ALU_main(rs, rt, control, z) == 0: #if same
                        self.ProgramCounter = self.ProgramCounter + (offset << 2)
                    elif alu.ALU_main(rs, rt, control, z) != 0:
                        self.ProgramCounter += 4
                    continue
                elif opCode == "bne" :
                    rs = self.Registers[getRs(value)]
                    rt = self.Registers[getRt(value)]
                    offset = getOffset(value)
                    control = 0x9 # sub
                    if alu.ALU_main(rs, rt, control, z) != 0:  # if not same
                        self.ProgramCounter = self.ProgramCounter + (offset << 2)
                    elif alu.ALU_main(rs, rt, control, z) == 0:
                        self.ProgramCounter += 4
                    continue

                elif opCode == "lw":

                    rs = self.Registers[getRs(value)]
                    offset = getOffset(value)
                    control = 0x8 # add
                    val = 0

                    self.Registers[getRt(value)] = Mem.MEM(alu.ALU_main(rs, offset, control, z), val, 0, 2)

                elif opCode == "sw":
                    rs = self.Registers[getRs(value)]
                    rt = self.Registers[getRt(value)]
                    offset = getOffset(value)
                    control = 0x8 #add
                    Mem.MEM(alu.ALU_main(rs, offset, control, z), rt, 1, 2)

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

                elif opCode == "lui" :
                    control = 0x1
                    offset = getOffset(value)
                    self.Registers[getRt(value)] = alu.ALU_main(offset, 16, control, z)


                rs = self.Registers[getRs(value)]
                rt = self.Registers[getRt(value)]
                offset = getOffset(value)

            self.ProgramCounter += 4
            ###time.sleep(0.1)
            continue





