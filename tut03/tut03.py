
import os
def output_by_subject():
    file = open('regtable_old.csv', 'r')
    Lines = file.readlines()
    l = 1
    while l<len(Lines):
	    record = Lines[l].split(',')
	    l+=1
	    roll = record[0]
	    register_sem = record[1]
	    sub_no = record[3]
	    sub_type = record[-1]
	    folder = "output_by_subject"
	    if not os.path.exists(folder):
		    os.mkdir(folder)
	    file_name = "{}/{}.csv".format(folder,sub_no)
	    with open(file_name, "a") as f:
		    if os.path.getsize(file_name) == 0:
			      f.write("rollno,register_sem,subno,sub_type")
		    f.write("{},{},{},{}".format(roll,register_sem,sub_no,sub_type))
    



def output_by_rollno():
    file = open('regtable_old.csv', 'r')
    Lines = file.readlines()
    l = 1
    while l<len(Lines):
	    record = Lines[l].split(',')
	    l+=1
	    roll = record[0]
	    register_sem = record[1]
	    sub_no = record[3]
	    sub_type = record[-1]
	    folder = "output_individual_roll"
	    if not os.path.exists(folder):
		     os.mkdir(folder)
	    file_name = "{}/{}.csv".format(folder,roll)
	    with open(file_name, "a") as f:
		    if os.path.getsize(file_name) == 0:
			     f.write("rollno,register_sem,subno,sub_type")
		    f.write("{},{},{},{}".format(roll,register_sem,sub_no,sub_type))

output_by_rollno()
output_by_subject()    














    

   