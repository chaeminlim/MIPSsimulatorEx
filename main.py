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
if __name__ == "__main__":
    ProgramCounter = 0x00400000
    Registers = [0 for _ in range(32)]
    Registers[29] = 0x7ffff1f8
    R_type = ['add', 'sub', 'and', 'jr', 'sll', 'sra', 'srl', 'syscall', 'or',
              'nor', 'xor', 'addu']
    # 메모리 객체 생성
    Mem = MemoryAccess()
    Mem.stackMEM[0xff1f8] = 0x2
    # 파일 읽어오기
    readBin = readbinary()
    readBin.changeEndian(readBin.openreadfile())
    # 4바이트 씩 나누어 리스트에 저장됨

    value = 0
    F_ProgramCounter = 0x00400000

    for i in range(0, 9):
        sys_list = [
            0x8fa40000, 0x27a50004,
            0x24a60004, 0x00041080,
            0x00c23021, 0x0c100009,
            0x00000000, 0x3402000a,
            0x0000000c]
        Mem.MEM(F_ProgramCounter,sys_list[i], 1 ,2)
        F_ProgramCounter += 4

    for i in range(2, len(readBin.codeList), 1):
        Mem.MEM(ProgramCounter+0x24, readBin.codeList[i], 1, 2) #24부터 저장
        ProgramCounter += 4

    # 저장 후 프로그램 카운터 초기화
    ProgramCounter = 0x00400000
    #디코딩
    while True:
        print("starting fetch#######################################3")
        print(Registers)

        z = 1
        #alu 객체 생성
        alu = ALU()
        # 명령어 하나씩 읽어오기
        value = Mem.MEM(ProgramCounter, value, 0, 2)
        print("instruction value: %x" % value)

        # opCode를 해석
        opCode = readBin.checkOpcode(value)
        if opCode in R_type:  # r 타입일때

            rs = Registers[getRs(value)]
            rt = Registers[getRt(value)]
            rd = Registers[getRd(value)]

            if getFunct(value) == 8: #jr
                ProgramCounter = Registers[31]
                continue
            elif getFunct(value) == 32: #if add
                control = 0x8
                Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
            elif getFunct(value) == 33: #addu
                control = 0x8
                Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
            elif getFunct(value) == 34: #sub
                control = 0x9
                Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
            elif getFunct(value) == 36: #and
                control = 0xC
                Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
            elif getFunct(value) == 37: #or
                control = 0xD
                Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
            elif getFunct(value) == 38: #xor
                control = 0xE
                Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
            elif getFunct(value) == 39: #nor
                control = 0xF
                Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
            elif getFunct(value) == 42: #slt
                control = 8
                Registers[getRd(value)] = alu.ALU_main(rs, rt, control, z)
            elif getFunct(value) == 0: #sll
                control = 0x1
                shift_amt = getShamt(value)
                Registers[getRd(value)] = alu.ALU_main(shift_amt, rt, control, z)
            elif getFunct(value) == 2: #srl
                control = 0x2
                shift_amt = getShamt(value)
                Registers[getRd(value)] = alu.ALU_main(shift_amt, rt, control, z)
            elif getFunct(value) == 3: #sra
                control = 0x3
                shift_amt = getShamt(value)
                Registers[getRd(value)] = alu.ALU_main(shift_amt, rt, control, z)
            elif getFunct(value) == 12: #syscall
                if Registers[2] == 10:
                    sys.exit()



        else:
            print(opCode)
            if opCode == "j":
                address = getAddress(value)
                ProgramCounter = (ProgramCounter & 0xF0000000) | ((address + 9) << 2)
                print("점프 프로그램카운터의 값은? %x" % ProgramCounter)
                continue
            #
            elif opCode == "jal":
                address = getAddress(value)
                Registers[31] = ProgramCounter + 4
                if value == 0x0c100009:
                    ProgramCounter = (ProgramCounter & 0xF0000000) | ((address) << 2)
                else:
                    ProgramCounter = (ProgramCounter & 0xF0000000) | ((address + 9) << 2)
                print("점프앤 링크 프로그램카운터의 값은? %x" % ProgramCounter)
                continue
            elif opCode == "beq":
                rs = Registers[getRs(value)]
                rt = Registers[getRt(value)]
                offset = getOffset(value)
                control =  0x9 #sub
                if alu.ALU_main(rs, rt, control, z) == 0: #if same
                    print("분기합니다")
                    ProgramCounter = ProgramCounter + (offset << 2)
                    print("bne 프로그램카운터의 값은? %x" % ProgramCounter)
                elif alu.ALU_main(rs, rt, control, z) != 0:
                    print("진행합니다")
                    ProgramCounter += 4
                continue
            elif opCode == "bne" :
                rs = Registers[getRs(value)]
                rt = Registers[getRt(value)]
                offset = getOffset(value)
                control = 0x9 # sub
                if alu.ALU_main(rs, rt, control, z) != 0:  # if not same
                    print("분기합니다")
                    ProgramCounter = ProgramCounter + (offset << 2)
                    print("bne 프로그램카운터의 값은? %x" % ProgramCounter)
                elif alu.ALU_main(rs, rt, control, z) == 0:
                    print("진행합니다")
                    ProgramCounter += 4
                continue

            elif opCode == "lw":
                
                rs = Registers[getRs(value)]
                offset = getOffset(value)    
                control = 0x8 # add
                val = 0

                Registers[getRt(value)] = Mem.MEM(alu.ALU_main(rs, offset, control, z), val, 0, 2)
                
            elif opCode == "sw":
                rs = Registers[getRs(value)]
                rt = Registers[getRt(value)]
                offset = getOffset(value) 
                control = 0x8 #add
                Mem.MEM(alu.ALU_main(rs, offset, control, z), rt, 1, 2)

            elif opCode == "addiu" :
                control = 0x8 # add
                rs = Registers[getRs(value)]
                offset = getOffset(value)
                Registers[getRt(value)] = rs + offset

            elif opCode == "ori" :
                control = 0xD
                rs = Registers[getRs(value)]
                offset = getOffset(value)
                Registers[getRt(value)] = alu.ALU_main(rs, offset, control, z)

            elif opCode == "lui" :
                control = 0x1
                offset = getOffset(value)
                Registers[getRt(value)] = alu.ALU_main(offset, 16, control, z)


            rs = Registers[getRs(value)]
            rt = Registers[getRt(value)]
            offset = getOffset(value)

        ProgramCounter += 4
        print("INSTRUCTION END##################################")
        time.sleep(0.1)
        continue






