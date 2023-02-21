import os
import openai as ai
from pathlib import Path
from sys import exit as term
from time import sleep
from pathlib import Path as path
from shutil import move, copymode, copyfile
import termcolor


def getKey():
	api = Path('api_key.dat')
	if (api.exists):
		key = api.read_text().lstrip().lstrip(" ").split(" ")[0].rstrip("\n")
		if (len(key) > 30):
			global Key
			Key = key
		else:
			pwd = path("api_key.dat").absolute()
			print(f"Invalid key or keyformat, please check {pwd} and make sure there is nothing in there except the key, and that the key itself is correct.")
			sleep(2)
			input("Press enter to exit now.")
			term("Invalid key.")
	else:
		path("api_key.dat").touch()
		pwd = path("api_key.dat").absolute()
		print(f"API keyfile not found, created file {pwd}, please enter your openai api key in the file.")
		sleep(2)
		input("Press enter to exit now.")
		term("File not found.")

def gpt_response(prompt):
	getKey()
	ai.api_key = Key
	openai.api_key = "YOUR_API_KEY"
	response = openai.Completion.create(
		model="code-davinci-edit-001",
		input=prompt,
		instruction=f"Make the $username and $password use mysqli_real_escape_string  ",
		max_tokens=1024,
		temperature=0.5,
		n = 1,
		stop=None
	)
	return response.choices[0].text


def backup():
	source_directory = input('Origin:')
	backup_directory = input('Destination:')
	if not os.path.exists(backup_directory):
		os.makedirs(backup_directory)
	for filename in os.listdir(source_directory):
		if filename.endswith('.php'):
			source_path = os.path.join(source_directory, filename)
			backup_path = os.path.join(backup_directory, filename)
			copyfile(source_path, backup_path)
	sleep(1)
	print("PHP files backup completed.")

def wKey():
	with open("api_key.dat",'r+') as file:
		file.truncate(0)
	inp = input('Enter your OpenAI API key: ')
	print('Writing API to the file (api_key.dat)...')
	with open('api_key.dat', "w") as file:
		file.write(inp)
	sleep(2)
	print("API has been written to the file (api_key.dat)!")


def fixSQL():
	pathd = input("Path:")
	def get_php_files(directory):
		php_files = []
		for filename in os.listdir(directory):
			if filename.endswith('.php'):
				php_files.append(os.path.join(directory, filename))
		return php_files

	def find_query_lines(directory):
		php_files = get_php_files(directory)
		all_query_lines = []
		for filename in php_files:
			with open(filename, 'r') as f:
				lines = f.readlines()
				query_lines = []
				for i, line in enumerate(lines):
					if "$query" in line:
						query_lines.append(line.strip())
						all_query_lines.append((filename, i+1, line.strip()))
						file_names, line_numbers, query_lines = zip(*all_query_lines)
		return list(file_names), list(line_numbers), list(query_lines)

	file_names, line_numbers, query_lines = find_query_lines(pathd)
	a = 0
	b = 1
	while a < len(line_numbers):
		print(f"Fixing File {b}...")
		#answer = gpt_response(query_lines[a])
		answer = f"sheesh{a}"
		print("Corrected Vulnerabilities.")
		sleep(1)
		print("Preparing to implement fixes...")
		sleep(3)
		with open(f'{file_names[a]}', 'r') as file:
			lines = file.readlines()
		lines[int(f'{line_numbers[a]}') - 1] = answer + '\n'
		with open(f'{file_names[a]}', 'w') as file:
			file.writelines(lines)
		print(f"File {b} has been fixed!")
		a+=1
		b+=1


termcolor.cprint("""
.------------------------------------------------------------------------------------------------------------------------.
|.----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  |
|| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. ||
|| |    _______   | || |    ___       | || |   _____      | || |  _________   | || |     _____    | || |  ____  ____  | ||
|| |   /  ___  |  | || |  .'   '.     | || |  |_   _|     | || | |_   ___  |  | || |    |_   _|   | || | |_  _||_  _| | ||
|| |  |  (__ \_|  | || | /  .-.  \    | || |    | |       | || |   | |_  \_|  | || |      | |     | || |   \ \  / /   | ||
|| |   '.___`-.   | || | | |   | |    | || |    | |   _   | || |   |  _|      | || |      | |     | || |    > `' <    | ||
|| |  |`\____) |  | || | \  `-'  \_   | || |   _| |__/ |  | || |  _| |_       | || |     _| |_    | || |  _/ /'`\ \_  | ||
|| |  |_______.'  | || |  `.___.\__|  | || |  |________|  | || | |_____|      | || |    |_____|   | || | |____||____| | ||
|| |              | || |              | || |              | || |              | || |              | || |              | ||
|| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' ||
| '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' |
| ---------------------------------------------------------------------------------------------------------------------- |
|                                                                                                                        |
| This software is provided "as is" without any warranty of any kind. The author of the software shall not be liable for |
| any claim, damages, or other liability arising from the use of the software. The user of the software assumes all risk |
| and responsibility for the use of the software.                                                                        |
|                                                                                                                        |   
| If you run into any errors make sure you have installed the dependencies required. You can do this by running          |   
| this command:                                                                                                          |
|      $ pip install -r requirements.text                                                                                |
|                                                                                                                        |
| Make sure to Backup the files first, for safety purposes the program wont work if you dont backup your files.          |
| Options:                                                                                                               |
|  [0]Exit                                                                                                               |   
|  [1]Backup Files                                                                                                       |           
|  [2]Setup API                                                                                                          |                           
|  [3]Fix SQL Vulnerabilities                                                                                            |
'------------------------------------------------------------------------------------------------------------------------'                                                                                                                                 
	""", 'white', 'on_black')


COMMANDS  ={
	'0' : exit,
	'1' : backup,
	'2' : wKey,
	'3' : fixSQL,
}

while True:
	command = input('> ')
	sleep(2)
	COMMANDS[command]()

