import re
import os
import shutil
from typing import Pattern
padding= 4
print("1. Breaking Bad")
print("2. Game of Thrones")
print("3. Lucifer")

webseries_num = int(input("Enter the number of the web series that you wish to rename. 1/2/3: "))
season_padding = int(input("Enter the Season Number Padding: "))
episode_padding = int(input("Enter the Episode Number Padding: "))

shutil.copytree(src='./wrong_srt',dst='./correct_srt')

def change_episode_syntax(match_pattern):
	global episode_padding
	season = match_pattern.group(1)
	episode = match_pattern.group(2)
		 
	return "Season " +  season + " Episode " + "".join(['0' for i in range( episode_padding - len(episode))]) + episode
def format_srt(match_pattern):
    video_name = match_pattern.group(1)
    file_format = match_pattern.group(2)
    return video_name + file_format


def regex_renamer():

	# Taking input from the user

	 
	 if webseries_num==1:
		 os.chdir("./correct_srt/Breaking Bad")
		 BB=os.listdir(os.getcwd())
		 for B in BB:
			 pattern=re.compile(r'.720p.BRip.Sujadir')
			 os.rename(B,pattern.sub('',B))
			 match_pattern1=re.compile(r"."+ "/d+" + "[a-zA-Z]"+'/d')
			 match_pattern2=re.compile(r'/d+')
			 season=re.findall(match_pattern1,B)
			 episode=re.findall(match_pattern2,B)
			 os.rename(B,match_pattern1.sub("Season " + "".join(['0' for i in range( season_padding - len(episode))]) + season + " Episode " + "".join(['0' for i in range( episode_padding - len(episode))]) + episode))
	 elif webseries_num==2:
		 os.chdir("./correct_srt/Game of Thrones")
		 files=os.listdir(os.getcwd())
		 for file in files:
			 show_name, episodes, srt_name = file.split(" - ")
			 print(episodes)
			 episodes = re.sub(r"(\d)[xe](\d+)",change_episode_syntax,episodes)
			 
			 srt_name = re.sub(r"^(.*?\.).*\.(\w*)$",format_srt,srt_name)
			 
			 os.rename(file," - ".join([show_name,episodes,srt_name]))
			 
		  
	 else:
		 os.chdir("./correct_srt/Lucifer")
		 LUf=os.listdir(os.getcwd())
		 for Lu in LUf:
			 show_name, episodes, srt_name = Lu.split(" - ")
			 episodes = re.sub(r"(\d)[xe](\d+)",change_episode_syntax,episodes)
			 srt_name = re.sub(r"^(.*?\.).*\.(\w*)$",format_srt,srt_name)
			 os.rename(Lu," - ".join([show_name,episodes,srt_name]))
			
			 



    	    

    

	  

regex_renamer()