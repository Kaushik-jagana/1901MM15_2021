def isdigit(num_array):
    invalid_inp=[]
    for num in num_array:
        if type(num)!=int:
          invalid_inp.append(num)
    return invalid_inp    
def get_memory_score(num_array):
    memory = []
    score = 0
    for num in num_array:
        if num in memory:
            score += 1
            continue
        if len(memory) == 5:
            memory.pop(0)
        memory.append(num)
    return score
inp=[3,4,1,6,3,3,9,0,0,0]
if len(isdigit(inp))==0:
   print("Score:", get_memory_score(inp))
else:
   print( "Invalid Input",isdigit(inp))
   