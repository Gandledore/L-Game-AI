



# x x  and x x
# x          x
# x          x


dir = ['E']

L1Dict = {}
for i in range(3):
    for j in range(2):
        if (i+1, j+1) not in L1Dict:
            L1Dict[(i+1, j+1)] = set()  
        for d in dir:
            L1Dict[(i+1, j+1)].add(d)
for item in L1Dict:
    print(item, L1Dict[item])

dir = ['W']

L1Dict = {}
for i in range(3):
    for j in range(2):
        if (i+2, j+1) not in L1Dict:
            L1Dict[(i+2, j+1)] = set()  
        for d in dir:
            L1Dict[(i+2, j+1)].add(d)
for item in L1Dict:
    print(item, L1Dict[item])

         
# x x x and     x
#     x     x x x

dir = ['S']

L1Dict = {}
for i in range(2):
    for j in range(3):
        if (i+3, j+1) not in L1Dict:
            L1Dict[(i+3, j+1)] = set()  
        for d in dir:
            L1Dict[(i+3, j+1)].add(d)
for item in L1Dict:
    print(item, L1Dict[item])


dir = ['N']

L1Dict = {}
for i in range(2):
    for j in range(3):
        if (i+3, j+2) not in L1Dict:
            L1Dict[(i+3, j+2)] = set()  
        for d in dir:
            L1Dict[(i+3, j+2)].add(d)
for item in L1Dict:
    print(item, L1Dict[item])

   #E      #W
# x    and   x
# x          x
# x x      x x


dir = ['E']

L1Dict = {}
for i in range(3):
    for j in range(2):
        if (i+1, j+3) not in L1Dict:
            L1Dict[(i+1, j+3)] = set()  
        for d in dir:
            L1Dict[(i+1, j+3)].add(d)
for item in L1Dict:
    print(item, L1Dict[item])


dir = ['W']

L1Dict = {}
for i in range(3):
    for j in range(2):
        if (i+2, j+3) not in L1Dict:
            L1Dict[(i+2, j+3)] = set()  
        for d in dir:
            L1Dict[(i+2, j+3)].add(d)
for item in L1Dict:
    print(item, L1Dict[item])


         
# x x x and x    
# x         x x x

dir = ['S']

L1Dict = {}
for i in range(2):
    for j in range(3):
        if (i+1, j+1) not in L1Dict:
            L1Dict[(i+1, j+1)] = set()  
        for d in dir:
            L1Dict[(i+1, j+1)].add(d)
for item in L1Dict:
    print(item, L1Dict[item])


dir = ['N']

L1Dict = {}
for i in range(2):
    for j in range(3):
        if (i+1, j+2) not in L1Dict:
            L1Dict[(i+1, j+2)] = set()  
        for d in dir:
            L1Dict[(i+1, j+2)].add(d)
for item in L1Dict:
    print(item, L1Dict[item])
