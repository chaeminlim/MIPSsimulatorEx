class ALU:

    def ALU_main(self, x, y, c, z):

        c32 = (c >> 2) & 0x3
        c10 = c & 0x3
        if c32 == 0:
            ret = self.shiftOperation(x, y, c10)

        elif c32 == 1:
            ret = self.checkSetless(x, y)

        elif c32 == 2:
            ret = self.addSubstract(x, y, c10)
            S = ret
            Z = self.checkZero(S)

        elif c32 == 3:
            ret = self.logicOperation(x, y, c10)

        return ret

    def EndFunc(self):
        print("end")

    def logicOperation(self, x, y, c10):
        if c10 < 0 or c10 > 3:
            self.EndFunc()

        if c10 == 0:
            return x & y
        elif c10 == 1:
            return x | y
        elif c10 == 2:
            return x ^ y
        elif c10 == 3:
            return ~(x | y)

    def shiftOperation(self, v, y, c):

        v = v & 0x001F # 5bit
        if c < 0 or c > 3:
            self.EndFunc()
        if c == 0:
            ret = y
        elif c == 1:
            y = y << v
            ret = y
        elif c == 2:
            y = y >> v
            ret = y
        elif c == 3:
            msb = y
            msb = msb >> 31
            if msb == 1:
                y = y >> v
                y = y | (0xFFFFFFFF << (32 - v))
                ret = y
                return ret
            if msb == 0:
                y = y >> v
                ret = y
                return ret
        return ret

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