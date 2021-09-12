import csv
import openpyxl 
import os
from os import listdir
import os.path
from os.path import isfile, join
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
    return

def output_individual_roll():
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
    return

output_individual_roll()
output_by_subject() 

def xlsx_output_by_rollno():
  files = [f for f in listdir('./output_individual_roll/') if isfile(join('./output_individual_roll/', f))]
  for file in files:
    if os.path.splitext(file)[1][1:] == 'csv':
      wb = openpyxl.Workbook()
      Xl = wb.active

      with open('./output_individual_roll/' + file) as f:
          reader = csv.reader(f, delimiter=',')
          for row in reader:
              Xl.append(row)
              wb.save('./output_individual_roll/' + file + '.xlsx')
      


def xlsx_output_by_subject():
  folder = [f for f in listdir('./output_by_subject/') if isfile(join('./output_by_subject/', f))]
  
  for file in folder:
    if os.path.splitext(file)[1][1:] == 'csv':
      wb = openpyxl.Workbook()
      Xl = wb.active

      with open('./output_by_subject/' + file) as f:
          reader = csv.reader(f, delimiter=',')
          for row in reader:
              Xl.append(row)
              wb.save('./output_by_subject/' +file + '.xlsx')
			  


      
      

xlsx_output_by_rollno()
xlsx_output_by_subject()
