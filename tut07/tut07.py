import pandas as pd
import numpy as np

def feedback_not_submitted():

	
	ltp_mapping_feedback_type = {1: 'lecture', 2: 'tutorial', 3:'practical'}
	output_file_name = "course_feedback_remaining.xlsx" 

	studentinfo = pd.read_csv("studentinfo.csv")
	course_feedback = pd.read_csv("course_feedback_submitted_by_students.csv")
	ltp_value = pd.read_csv("course_master_dont_open_in_excel.csv")
	course_registered = pd.read_csv("course_registered_by_all_students.csv")

	rollnos =  course_registered['rollno'].unique()

	df = pd.read_excel("course_feedback_remaining.xlsx")

	for i in rollnos:

		subs = np.array(course_registered[course_registered['rollno']==i]['subno'])
		
        
		for j in subs:
			ltp = ltp_value[ltp_value['subno']==j]['ltp'].iloc[0]
			ltp = [int(i) for i in ltp.split('-')]
			bit_count = np.count_nonzero(ltp)

			feedback_count = course_feedback[(course_feedback['stud_roll']==i) & (course_feedback['course_code']==j)].shape[0]

			if(bit_count!=feedback_count and bit_count>feedback_count):
				df1 = course_registered[(course_registered['rollno']==i) & (course_registered['subno']==j)].iloc[:,[0,1,2,3]]
				df2 = studentinfo[studentinfo['Roll No']==i].iloc[:,[0,1,8,9,10]]
				df2.columns = ['Name', 'rollno', 'email', 'aemail', 'contact']
				df3 = df1.merge(df2)
				df = df.append(df3,ignore_index=True)

	df = df.drop_duplicates(keep='first', ignore_index=True)
                                  
	df.to_excel("course_feedback_remaining.xlsx",index=False)


    
    

feedback_not_submitted()
                                   
   