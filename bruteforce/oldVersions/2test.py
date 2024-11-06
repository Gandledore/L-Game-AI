



L1List = []

# x x  and x x
# x          x
# x          x


dir = ['E']

for i in range(3):
    for j in range(2):
        for d in dir:
            L1List.append(((i+1, j+1), d))

print("=========================")
for item in L1List:
    print(item)
print("=========================")

dir = ['W']


for i in range(3):
    for j in range(2): 
        for d in dir:
            L1List.append(((i+2, j+1), d))

print("=========================")
for item in L1List:
    print(item)
print("=========================")
         
# x x x and     x
#     x     x x x

dir = ['S']


for i in range(2):
    for j in range(3):
        for d in dir:
            L1List.append(((i+3, j+1), d))



dir = ['N']


for i in range(2):
    for j in range(3): 
        for d in dir:
            L1List.append(((i+3, j+2), d))


   #E      #W
# x    and   x
# x          x
# x x      x x


dir = ['E']


for i in range(3):
    for j in range(2):
        for d in dir:
            L1List.append(((i+1, j+3), d))



dir = ['W']


for i in range(3):
    for j in range(2):
        for d in dir:
            L1List.append(((i+2, j+3), d))



         
# x x x and x    
# x         x x x

dir = ['S']


for i in range(2):
    for j in range(3): 
        for d in dir:
            L1List.append(((i+1, j+1), d))



dir = ['N']


for i in range(2):
    for j in range(3):
        for d in dir:
            L1List.append(((i+1, j+2), d))


for i in L1List:
    print(i)
print(len(L1List))