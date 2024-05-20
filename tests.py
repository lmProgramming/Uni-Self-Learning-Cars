import random

def min_steps_to_unique(array):
    from collections import Counter
    
    n = len(array)
    count = Counter(array)
    
    duplicates = []
    missing = []
    
    for num in range(1, n + 1):
        if count[num] == 0:
            missing.append(num)
        elif count[num] > 1:
            duplicates.extend([num] * (count[num] - 1))
    
    duplicates.sort()
    missing.sort()
    
    steps = 0
    
    for dup, miss in zip(duplicates, missing):
        steps += abs(dup - miss)
    
    return steps

def min_steps_to_unique_mine(array):    
    sorted_a = sorted(array)
    
    steps = 0
    
    for index, i in enumerate(sorted_a):
        steps += abs(i - index - 1)
        
    return steps

def min_steps_to_unique_mine_2(A):
    N = len(A)

    numbers = [False for i in range(0, N + 1)]

    moves = 0
    for num in A:
        if numbers[num]:
            offset = 1
            while True:
                moves += 1
                if num - offset >= 1 and not numbers[num - offset]:
                    numbers[num - offset] = True
                    break
                elif num + offset <= N and not numbers[num + offset]:
                    numbers[num + offset] = True
                    break
                offset += 1      
        else:
            numbers[num] = True
        if moves > 1000000000:
            return -1
    return moves

N = 10000000
array = [random.randrange(1, N) for _ in range(N + 1)]
print(min_steps_to_unique(array)) 
print(min_steps_to_unique_mine(array))  
print(min_steps_to_unique_mine_2(array))