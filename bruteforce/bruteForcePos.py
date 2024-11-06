



L1List = []

# x x  and x x
# x          x
# x          x


dir = ['E']

for i in range(3):
    for j in range(2):
        for d in dir:
            L1List.append(((i+1, j+1), d))


dir = ['W']


for i in range(3):
    for j in range(2): 
        for d in dir:
            L1List.append(((i+2, j+1), d))

         
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

with open('Lpos.txt', 'w') as file:
    for i in L1List:
        file.write(f"{i}\n")  
# print(len(L1List))

# print("========L2========")
# L2List = L1List

# for i in L2List:
#     print(i)
# print(len(L2List))


# L1Set = set(L1List)
# L2Set = set(L2List)

# ValidL = L1Set - L2Set

# print(L1Set - L2Set)

# for v in ValidL:
#     print(v)



#token moves

TList = []

for i in range(4):
    for j in range(4):
        TList.append((i+1, j+1))

with open('Tpos.txt', 'w') as file:
    for i in TList:
        file.write(f"{i}\n")  


