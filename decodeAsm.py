from memoryAccess import MemoryAccess

class decodeAssembly:

    def __init__(self):
        self.iTypeInst = ['lw', 'sw', 'addi']
        self.rTypeInst = ['add', 'sub', 'bne', 'or', 'xor', 'nor', 'and']
        self.jTypeInst = ['j', 'jr', 'jal']
        self.pseudoInst = ['la', 'li', 'move', 'syscall']
        self.shiftInst =['sll', 'srl', 'sra']
        self.registerDict = {
            'zero': 0, 'at': 1, 'v0': 2, 'v1': 3,
            'a0': 4, 'a1': 5, 'a2': 6, 'a3': 7,
            't0': 8, 't1': 9, 't2': 10, 't3': 11, 't4': 12, 't5': 13, 't6': 14, 't7': 15,
            's0': 16, 's1': 17, 's2': 18, 's3': 19, 's4': 20, 's5': 21, 's6': 22, 's7': 23,
            't8': 24, 't9': 25, 'k0': 26, 'k1': 27, 'gp': 28, 'sp': 29, 'fp': 30, 'ra': 31
        }
        self.MemIdx = {}
    def fopen(self, directory):
        self.f = open(directory, 'r')

    def encode(self, MEM):
        lines = self.f.readlines()
        a = lines.count('\n')
        for i in range(a):
            lines.remove("\n")

        b = 0
        while True:
            try:
                lines[b] = lines[b].replace("\n", '')
                lines[b] = lines[b].replace(" ", '')
                lines[b] = lines[b].split('#')[0]
                lines[b] = lines[b].replace("\t", "")
                b += 1
            except:
                break

        a = lines.count('')
        for i in range(a):
            lines.remove("")

        decodedList = []
        dataList = []
        textList = []

        for i in range(len(lines)):
            if lines[i] == '.data':
                while True:
                    i += 1
                    if lines[i] == '.text': break
                    dataList.append(lines[i])
                continue
            if lines[i] == '.text':
                while True:
                    i += 1
                    textList.append(lines[i])
                    if i == len(lines) - 1: break
                continue

        validCnt = 0
        for i in range(len(textList)):

            line = textList[i].split('$')
            if line[0] in self.iTypeInst or line[0] in self.rTypeInst or line[0] in self.jTypeInst or line[0]  in self.pseudoInst or line[0][0]=='j' or line[0] in self.shiftInst:
                validCnt += 1

            if ':' in line[0]:
                for index in range(len(line[0])):
                    if line[0][index] == ':':
                        idxName = line[0][0:index]
                        line[0] = line[0].replace(idxName, '')
                        line[0] = line[0].replace(':', '')
                        idxName = idxName.replace(':', '')
                        self.MemIdx[idxName] = 0x00400000 + 0x4 * (validCnt)
                        if line[0] in self.iTypeInst or line[0] in self.rTypeInst or line[0] in self.jTypeInst or line[0] in self.pseudoInst or line[0] in self.shiftInst:
                            print("라인값",line[0])
                            validCnt += 1
                        break

        memCnt = 0

        for i in range(len(textList)):

            line = textList[i].split('$')
            if ':' in line[0]:
                for index in range(len(line[0])):
                    if line[0][index] == ':':
                        idxName = line[0][0:index+1]
                        line[0] = line[0].replace(idxName,'')
                      #  idxName = idxName.replace(':','')
                        idxName = idxName.replace(':', '')
                        #self.MemIdx[idxName] = 0x00400024 + 4 * (memCnt)

                        break
            if line[0] in self.shiftInst:

                rd = line[1].replace(',', '')
                rt = line[2].split(',')[0]
                shamt = int(line[2].split(',')[1])

                if line[0] == 'srl': #line0 srl line1 t1, line2 s2, 4
                    decoded = 0x2 + (shamt << 6) + (self.registerDict[rd] << 11) + (self.registerDict[rt] << 16)
                    decodedList.append(decoded)

                elif line[0] == 'sll':
                    decoded = 0x0 + (shamt << 6) + (self.registerDict[rd] << 11) + (self.registerDict[rt] << 16)
                    decodedList.append(decoded)

                elif line[0] == 'sra':
                    decoded = 0x3 + (shamt << 6) + (self.registerDict[rd] << 11) + (self.registerDict[rt] << 16)
                    decodedList.append(decoded)


                memCnt += 1

            if line[0] in self.iTypeInst:

                if line[0] == 'addi':
                    rt = line[1].replace(',','')
                    rs = line[2].split(',')[0]
                    imm = line[2].split(',')[1]
                    decoded = (0x8 << 26) + (self.registerDict[rs] << 21) + (self.registerDict[rt] << 16) + int(imm)
                    decodedList.append(decoded)

                if line[0] == 'lw':
                    decodeLine = textList[i].replace('lw$', '')
                    rd = decodeLine.split(',')[0]  # s0
                    rest = decodeLine.split(',')[1]  # 4($t2)
                    rest = rest.replace('(', '')
                    rest = rest.replace(')', '')
                    offset = rest.split('$')[0]
                    rs = rest.split('$')[1]
                    decoded = (self.registerDict[rd] << 16) + (0x23 << 26) + int(offset) + (self.registerDict[rs] << 21)
                    decodedList.append(decoded)

                if line[0] == 'sw':
                    decodeLine = textList[i].replace('sw$', '')
                    rd = decodeLine.split(',')[0]  # s0
                    rest = decodeLine.split(',')[1]  # 4($t2)
                    rest = rest.replace('(', '')
                    rest = rest.replace(')', '')
                    offset = rest.split('$')[0]
                    rs = rest.split('$')[1]
                    decoded = (self.registerDict[rd] << 16) + (0x2B << 26) + int(offset) + (self.registerDict[rs] << 21)
                    decodedList.append(decoded)

                memCnt += 1

            elif line[0] in self.rTypeInst:
                if line[0] == 'bne':
                    rs = line[1].replace(',', '')
                    rt = line[2].split(',')[0]
                    offset = line[2].split(',')[1]
                    decoded = ((self.MemIdx[offset]-(self.MemIdx['main'] + memCnt*4))>>2) + (self.registerDict[rs] << 21) + (self.registerDict[rt] << 16) +(0x5<<26)
                    decodedList.append(decoded)


                else:
                    line[2] = line[2].replace(',', '')
                    line[1] = line[1].replace(',', '')
                    decoded = (self.registerDict[line[1]] << 11) + (self.registerDict[line[2]] << 21) + (self.registerDict[line[3]] << 16)

                if line[0] == 'add':
                    decoded += 0x20
                    decodedList.append(decoded)

                if line[0] == 'sub':
                    decoded += 0x22
                    decodedList.append(decoded)

                if line[0] == 'or':
                    decoded += 0x25
                    decodedList.append(decoded)

                if line[0] == 'xor':
                    decoded += 0x26
                    decodedList.append(decoded)

                if line[0] == 'nor':
                    decoded += 0x27
                    decodedList.append(decoded)

                if line[0] == 'and':
                    decoded += 0x24
                    decodedList.append(decoded)

                memCnt += 1


            elif line[0] in self.pseudoInst:

                if line[0] == 'la':  # lui 4097
                    decoded = 4097 + (self.registerDict[line[1].split(',')[0]] << 16) + (0xf << 26)
                    decodedList.append(decoded)

                elif line[0] == 'li':

                    if '0x' in line[1].split(',')[1]:
                        if (int(line[1].split(',')[1], 0) >> 16) > 0:
                            decoded = (self.registerDict[line[1].split(',')[0]] << 16) + (int(line[1].split(',')[1],0)>>16) + (0xF << 26)
                        else:
                            decoded = (self.registerDict[line[1].split(',')[0]] << 16) + int(line[1].split(',')[1],0) + (0xD << 26)
                    else:
                        if (int(line[1].split(',')[1]) >> 16) > 0:
                            decoded = (self.registerDict[line[1].split(',')[0]] << 16) + (int(line[1].split(',')[1],0)>>16) + (0xF << 26)
                        else:
                            decoded = (self.registerDict[line[1].split(',')[0]] << 16) + int(line[1].split(',')[1]) + (0xD << 26)
                    decodedList.append(decoded)

                elif line[0] == 'move':
                    line[1] = line[1].replace(',', '')
                    decoded = (self.registerDict[line[1]] << 11) + (self.registerDict[line[2]] << 16) + 0x21
                    decodedList.append(decoded)

                elif line[0] == 'syscall':
                    decoded = 0xC
                    decodedList.append(decoded)

                memCnt += 1

            elif line[0] in self.jTypeInst:

                if line[0] == 'jr':
                    decoded = 0x8 + (self.registerDict[line[1]] << 21)
                    decodedList.append(decoded)

                    memCnt += 1

            else:
                if line[0] == "":
                    pass
                elif line[0][0] == 'j' and line[0][1] != 'a':
                    adName = line[0].split('j')[1]
                    Joffset = self.MemIdx[adName] + 0x24
                    decoded = (0x2 << 26) + (Joffset >> 2)
                    decodedList.append(decoded)
                    memCnt += 1

                elif line[0][0] == 'j' and line[0][1] == 'a' and line[0][2] == 'l':
                    adName = line[0].replace('jal','')
                    Joffset = self.MemIdx[adName] + 0x24
                    decoded = (0x3 << 26) + (Joffset >> 2)
                    decodedList.append(decoded)
                    memCnt += 1

        ###
        ###

        address = 0x10010000
        for i in range(len(dataList)):
            for stridx in range(len(dataList[i])):
                if dataList[i][stridx] == ':' :
                    dataList[i] = dataList[i][stridx+1: ]
                    break
            if '.word' in  dataList[i]:
                dataList[i] = dataList[i].replace('.word', '')
                MEM.MEM(address, int(dataList[i]), 1, 2)
                address += 0x4


        return decodedList, dataList, textList

    def printAll(self,decodedList, dataList):

        for i in range(len(dataList)):
            print(dataList[i])

        for i in range(len(decodedList)):
            print("%08X" % decodedList[i])




if __name__ == "__main__":
    da = decodeAssembly()
    da.fopen("C:\\Users\\Chaemin Lim\\Desktop\\컴퓨터구조과제\\qtspim_example\\as_ex04_fct.s")
    Mem = MemoryAccess()
    decodedList, dataList, textList = da.encode(Mem)
    da.printAll(decodedList, dataList)

    for i in range(len(textList)):
        print(textList[i])
