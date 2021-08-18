inp_arr = input().split(" ")
total_meraki_numbers = 0


def is_meraki_number(num_str):
    for i in range(0, len(num_str) - 1):
        current = int(num_str[i])
        next = int(num_str[i+1])
        if current + 1 == next or current - 1 == next:   
            continue
        else:
            print("No - {} is not a meraki number".format(num_str))   
            return False
    print("Yes - {} is a meraki number".format(num_str))       
    return True


for i in inp_arr:
    if(is_meraki_number(i)):
        total_meraki_numbers += 1
        

print( "The input list contains {} meraki numbers and {} non meraki numbers.".format( total_meraki_numbers, len(inp_arr) - total_meraki_numbers))