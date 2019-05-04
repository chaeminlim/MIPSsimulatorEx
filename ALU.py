class ALU:

    def ALU_main(self, x, y, c, z):

        c32 = (c >> 2) & 0x3
        c10 = c & 0x3
        if c32 == 0:
            print("shiftoperation 수행")
            ret = self.shiftOperation(x, y, c10)

        elif c32 == 1:
            print("checkSetless 수행")
            ret = self.checkSetless(x, y)

        elif c32 == 2:
            print("addsubstract 수행")
            ret = self.addSubstract(x, y, c10)
            S = ret
            Z = self.checkZero(S)

        elif c32 == 3:
            print("logicOperation 수행")
            ret = self.logicOperation(x, y, c10)

        return ret

    def EndFunc(self):
        print("end")

    def logicOperation(self, x, y, c10):
        if c10 < 0 or c10 > 3:
            print("오류")
            self.EndFunc()

        if c10 == 0:
            print("AND")
            return x & y
        elif c10 == 1:
            print("OR")
            return x | y
        elif c10 == 2:
            print("XOR")
            return x ^ y
        elif c10 == 3:
            print("NOR")
            return ~(x | y)

    def shiftOperation(self, v, y, c):

        v = v & 0x001F # 5bit
        if c < 0 or c > 3:
            print("error int shift operation")
            self.EndFunc()
        if c == 0:
            print("no shift")
            ret = y
        elif c == 1:
            print("sll")
            y = y << v
            ret = y
        elif c == 2:
            print("srl")
            y = y >> v
            ret = y
        elif c == 3:
            print("sra")
            msb = y
            msb = msb >> 31
            if msb == 1:
                y = y >> v
                y = y | (0xFFFFFFFF << (32 - v))
                return y
            if msb == 0:
                y = y >> v
                return y
        return y

    def addSubstract(self, x, y, c10):
        if c10 < 0x0 or c10 > 0x3:
            print("error")
            self.EndFunc()
        elif c10 == 0x0 or c10 == 0x2:
            ret = x + y
        elif c10 == 0x1 or c10 == 0x3:
            ret = x - y

        return ret

    def checkZero(self, s):
        if s == 0:
            return 1
        else:
            return 0

    def checkSetless(self, x, y):
        if x < y:
            return 1
        else:
            return 0