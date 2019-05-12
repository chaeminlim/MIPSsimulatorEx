import struct


class readbinary:

    def __init__(self):
        self.codeList = []

    def openreadfile(self, inst_name):
        f = open(inst_name, 'rb')
        return f

    def closefile(self, f):
        f.close()

    def changeEndian(self, f):
        while True:
            s = f.read(4)
            if s == b"":
                break
            s = struct.unpack('!I', s)
            self.codeList.append(s[0])

    def checkOpcode(self, instr):
        if (instr >> 26) == 0:
            return{
                0: "sll",
                2: "srl",
                3: "sra",
                6: "srlv",
                8 + 0: "jr",
                8 + 4: "syscall",
                16 + 0: "mfhi",
                16 + 2: "mflo",
                24 + 0: "mul",
                32 + 0: "add",
                32 + 1: "addu",
                32 + 2: "sub",
                32 + 4: "and",
                32 + 5: "or",
                32 + 6: "xor",
                32 + 7: "nor",
                40 + 2: "slt"
            }.get(instr & 0x3F, "없음")

        return{
                0: "Rtype",
                1: "bltz",
                2: 'j',
                3: "jal",
                4: "beq",
                5: "bne",
                8 + 0: "addi",
                8 + 1: "addiu",
                8 + 2: "slti",
                8 + 4: "andi",
                8 + 5: "ori",
                8 + 6: "xori",
                8 + 7: "lui",
                32 + 0: "lb",
                32 + 3: "lw",
                32 + 4: "lbu",
                40 + 0: "sb",
                40 + 3: "sw"
            }.get(instr >> 26, '없음')


