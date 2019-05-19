class decodeAssembly:

    def __init__(self):
        print("hello")
    def fopen(self, directory):
        self.f = open(directory, 'r')


da = decodeAssembly()
da.fopen("C:\\Users\Chaemin Lim\\Desktop\\컴퓨터구조과제\\qtspim_example\\as_ex01_arith.s")
print(da.f)
lines = da.f.readlines()
print(lines)

a = lines.count('\n')

for i in range(a):
    lines.remove("\n")

b = 0
while True:
    try:
        lines[b] = lines[b].replace("\n", '')
        b += 1
    except:
        break
b = 0

while True:
    try:
        print(lines[b])
        b += 1
    except:
        break



