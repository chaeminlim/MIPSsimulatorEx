
def func(z):
    z = 2
    return z

global z
z = 1
func(z)
print(z)