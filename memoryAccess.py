class MemoryAccess:

    def __init__(self):
        self.ProgramMEM = [0] * 0x100000
        self.dataMEM = [0] * 0x100000
        self.stackMEM = [0] * 0x100000

    def MEM(self, A, V, nRW, S):

        pM = []
        sel = A >> 20
        offset = A & 0xfffff
        if sel == 0x004:
            pM = self.ProgramMEM
        elif sel == 0x100:
            print("access data memory")
            pM = self.dataMEM
        elif sel == 0x7ff:
            print("access stack memory")
            pM = self.stackMEM
        else:
            print("no such memory")

        if S==0: #byte
            if nRW == 0: #read
                V = pM[offset]
                return V

            elif nRW == 1: #write
                pM[offset] = V & 0xff
                return V

        elif S == 1:
            if nRW == 0:
                V = (pM[offset]) | (pM[offset + 1] << 8)
                return V
            elif nRW == 1:
                pM[offset] = V & 0x00ff
                pM[offset + 1] = (V & 0xff00) >> 8
                return V

        elif S == 2: #fullword
            if nRW == 0:
                V = pM[offset] | (pM[offset + 1] << 8) | (pM[offset + 2] << 16) | (pM[offset + 3] << 24)
                return V
            elif nRW == 1:
                pM[offset] = V & 0x000000ff
                pM[offset + 1] = (V & 0x0000ff00) >> 8
                pM[offset + 2] = (V & 0x00ff0000) >> 16
                pM[offset + 3] = (V & 0xff000000) >> 24
                return V

        else:
            print("memeory access size error")
            return