def subreeks(n):
    s = 0
    for i in range(1, n):
        s = s + i
    return s

def calc(n):
    s = 0
    for i in range(1, n+1):
        s = s + subreeks(i)
    return s

print calc(6)
print calc(7)
print calc(8)
print calc(35)
print calc(150)