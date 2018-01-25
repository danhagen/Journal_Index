import pickle
import numpy as np
from termcolor import cprint,colored
import platform
import subprocess
import ipdb
import re
import string

platform_name = platform.system()
if platform_name == 'Windows':
	subprocess.call("git pull --quiet origin master", shell = True)
else:
	subprocess.call(args=["git pull --quiet origin master"], shell = True)
import class_def
from class_def import index_topic

def print_reference(topic_string,index):
	keys = np.sort([int(key) for key in index[topic_string].index.keys()])
	if len(topic_string)%2==1:
		left_adjustment,right_adjustment = int((len(topic_string)-1)/2),int((len(topic_string)+1)/2)
	else:
		left_adjustment,right_adjustment = int(len(topic_string)/2),int(len(topic_string)/2)
	output = "\n" + " "*10 + colored(' '*(20-left_adjustment) + topic_string + ' '*(20-right_adjustment),'white',attrs=['bold','underline']) + " "*10
	for j in range(len(keys)):
		pages = np.sort(index[topic_string].index[str(keys[j])])
		discontinuity_indicator = (np.diff(pages)!=1)*np.arange(1,len(pages),1)
		if len(pages)==1:
			pages_string = "p. " + str(pages[0])
		else:
			pages_string = "pp. " + str(pages[0])
			if discontinuity_indicator[0] != 0:
				pages_string += ", " + str(pages[1])
				if discontinuity_indicator[-1] != 0:
					for i in range(2,len(discontinuity_indicator)):
						if discontinuity_indicator[i] != 0:
							pages_string += "-" + str(pages[i]) + ", " + str(pages[i+1])
				else:
					for i in range(2,len(discontinuity_indicator-1)):
						if discontinuity_indicator[i] != 0:
							pages_string += "-" + str(pages[i]) + ", " + str(pages[i+1])
					pages_string += "-" + str(pages[-1])
			else:
				if discontinuity_indicator[-1] != 0:
					for i in range(1,len(discontinuity_indicator)):
						if discontinuity_indicator[i] != 0:
							pages_string += "-" + str(pages[i]) + ", " + str(pages[i+1])
				else:
					for i in range(1,len(discontinuity_indicator-1)):
						if discontinuity_indicator[i] != 0:
							pages_string += "-" + str(pages[i]) + ", " + str(pages[i+1])
					pages_string += "-" + str(pages[-1])
		if j == 0:
			if (5+len(str(keys[j]))+2+len(pages_string))%2==1:
				left_adjustment,right_adjustment = int(((5+len(str(keys[j]))+2+len(pages_string))-1)/2),int(((5+len(str(keys[j]))+2+len(pages_string))+1)/2)
			else:
				left_adjustment,right_adjustment = int((5+len(str(keys[j]))+2+len(pages_string))/2),int((5+len(str(keys[j]))+2+len(pages_string))/2)
			output +=  colored("\n" + " "*(30-left_adjustment) + "vol. " + str(keys[j]) \
								+ ": " + pages_string + " "*(30-right_adjustment) \
								+ "\n",
								'white')
		else:
			if (5+len(str(keys[j]))+2+len(pages_string))%2==1:
				left_adjustment,right_adjustment = int(((5+len(str(keys[j]))+2+len(pages_string))-1)/2),int(((5+len(str(keys[j]))+2+len(pages_string))+1)/2)
			else:
				left_adjustment,right_adjustment = int((5+len(str(keys[j]))+2+len(pages_string))/2),int((5+len(str(keys[j]))+2+len(pages_string))/2)

			output += colored(" "*(30-left_adjustment) + "vol. " + str(keys[j]) \
								+ ": " + pages_string + " "*(30-right_adjustment)\
								+ "\n", \
								'white')
	cprint(output)
def list_references(index):
	cprint('-'*60,'white',attrs=['bold'])
	cprint('Reference List\n','white',attrs=['bold','underline'])
	[cprint('- ' + key,'white') for key in sorted(index.keys())]
	print('')
def print_single_reference(index):
	another_reference = True
	while another_reference == True:
		cprint('-'*60,'white',attrs=['bold'])
		cprint('Print Reference','blue',attrs = ['bold','underline'])
		valid_response_1 = False
		while valid_response_1 == False:
			topic = input(colored('Topic: ','red', attrs = ['bold']))
			topic = " ".join(string.capwords(w) for w in re.split('-| ',topic))
			for letter in string.ascii_lowercase:
				topic = topic.replace("("+letter,"("+letter.capitalize())
			for article in [" A "," The ", " An ", " At ", " From ", " Of ", " W.r.t. "]:
				topic = topic.replace(article,article.lower())
			if topic in index.keys():
				print_reference(topic,index)
				valid_response_1 = True
			elif topic == 'Exit' or topic == 'Cancel':
				break
			else:
				if len(topic)>=4:
					topic = topic[:4]
				potential_keys = []
				for key in index.keys():
					if key[:len(topic)] == topic:
						potential_keys.append(key)
				if len(potential_keys)==0:
					cprint("No references matched your search.", 'blue', attrs = ['bold'])
					valid_response_1 == False
				else:
					cprint('-'*60,'white',attrs=['bold'])
					cprint('Search Results','blue',attrs = ['bold','underline'])
					[cprint(str(i+1) + " - " + potential_keys[i], 'white') for i in range(len(potential_keys))]
					exit_search_results = False
					while exit_search_results == False:
						cprint('-'*60,'white',attrs=['bold'])
						valid_response_2 = input(colored("Select Reference Number: ", 'red', attrs = ['bold']))
						if valid_response_2.capitalize() == "Exit" or valid_response_2.capitalize() == "Cancel":
							valid_response_1 = True
							break
						else:
							try:
								if int(valid_response_2)-1 not in range(len(potential_keys)):
									cprint('-'*60,'white',attrs=['bold'])
									cprint('Number option not listed.', 'blue', attrs = ['bold'])
									exit_search_results = False
								else:
									topic = potential_keys[int(valid_response_2)-1]
									print_reference(topic,index)
									valid_response_1 = True
									exit_search_results = True
							except ValueError:
								cprint('Invalid Response.', 'blue', attrs =['bold'])
								exit_search_results = False
		valid_response_3 = False
		while valid_response_3 == False:
			cprint('-'*60,'white',attrs=['bold'])
			next_action = input(colored("Print Another Reference? ([y],n): ",'red',attrs=['bold'])).capitalize()
			if next_action in ['Y', '']:
				another_reference = True
				valid_response_3 = True
			elif next_action == 'N':
				another_reference = False
				valid_response_3 = True
			else:
				cprint('Invalid Response.', 'blue', attrs =['bold'])
				valid_response_3 = False
def delete_topic(index):
	delete_another_topic = True
	while delete_another_topic == True:
		cprint('-'*60,'white',attrs=['bold'])
		cprint('Delete Reference','blue',attrs = ['bold','underline'])
		topic_to_be_deleted = input(colored('Topic: ','red',attrs = ['bold'])).capitalize()
		topic_to_be_deleted = " ".join(string.capwords(w) for w in re.split('-| ',topic_to_be_deleted))
		for letter in string.ascii_lowercase:
			topic_to_be_deleted = topic_to_be_deleted.replace("("+letter,"("+letter.capitalize())
		for article in [" A "," The ", " An ", " At ", " From ", " Of ", " W.r.t. "]:
			topic_to_be_deleted = topic_to_be_deleted.replace(article,article.lower())

		if topic_to_be_deleted == "Exit":
			return
		else:
			potential_keys = []
			for key in index.keys():
				if key[:len(topic_to_be_deleted)] == topic_to_be_deleted:
					potential_keys.append(key)
			if len(potential_keys)==0:
				cprint("No references matched your search.", 'blue', attrs = ['bold'])
			else:
				cprint('-'*60,'white',attrs=['bold'])
				cprint('Search Results','blue',attrs = ['bold','underline'])
				[cprint(str(i+1) + " - " + potential_keys[i], 'white') for i in range(len(potential_keys))]
				exit_search_results = False
				while exit_search_results == False:
					cprint('-'*60,'white',attrs=['bold'])
					response_3 = input(colored("Select Reference Number: ", 'red', attrs = ['bold']))
					if response_3.capitalize() == "Exit":
						return
					else:
						try:
							if int(response_3)-1 not in range(len(potential_keys)):
								cprint('-'*60,'white',attrs=['bold'])
								cprint('Number option not listed.', 'blue', attrs = ['bold'])
								exit_search_results = False
							else:
								topic_to_be_deleted = potential_keys[int(response_3)-1]
								valid_response_2 = False
								while valid_response_2 == False:
									safety_check = input(colored("Are you sure you want to delete '" \
														+ topic_to_be_deleted + "' in Index? ([y],n): ",\
														'red',attrs = ['bold'])).capitalize()
									if safety_check in ['Y', '']:
										del index[topic_to_be_deleted]
										valid_response_2 = True
									elif safety_check == 'N':
										valid_response_2 = True
									else:
										cprint('Invalid Response.', 'blue', attrs =['bold'])
										valid_response_2 = False
								exit_search_results = True
						except ValueError:
							cprint('Invalid Response.', 'blue', attrs =['bold'])
							exit_search_results = False
		invalid_response = True
		while invalid_response == True:
			cprint('-'*60,'white',attrs=['bold'])
			next_action = input(colored("Delete Another Reference? ([y],n): ",'red',attrs=['bold'])).capitalize()
			if next_action in ['Y', '']:
				delete_another_topic = True
				invalid_response = False
			elif next_action == 'N':
				delete_another_topic = False
				invalid_response = False
			else:
				cprint('Invalid Response.', 'blue', attrs =['bold'])
				invalid_response = True
def delete_volume(index):
	remove_another_volume_reference = True
	while remove_another_volume_reference == True:
		cprint('-'*60,'white',attrs=['bold'])
		cprint('Remove Volume Reference','blue',attrs = ['bold','underline'])
		valid_response_1 = False
		while valid_response_1 == False:
			topic_string = input(colored('Topic: ','red',attrs = ['bold']))
			topic_string = " ".join(string.capwords(w) for w in re.split('-| ',topic_string))
			for letter in string.ascii_lowercase:
				topic_string = topic_string.replace("("+letter,"("+letter.capitalize())
			for article in [" A "," The ", " An ", " At ", " From ", " Of ", " W.r.t. "]:
				topic_string = topic_string.replace(article,article.lower())

			if topic_string in index.keys():
				if len(index[topic_string].index.keys())==1:
					cprint("Topic '" + topic_string + "' has only one volume reference. \nSwitch to Delete Topic.",\
							'blue', attrs = ['bold'])
					valid_response_1 = True
				else:
					valid_response_2 = False
					while valid_response_2 == False:
						volume_to_be_deleted = input(colored('Volume: ','red',attrs = ['bold']))
						if volume_to_be_deleted in index[topic_string].index.keys():
							valid_response_3 = False
							while valid_response_3 == False:
								safety_check = input(colored("Are you sure you want to delete vol. " + volume_to_be_deleted + \
													" from topic '" + topic_string + " in Index? ([y],n): ",\
													'red',attrs = ['bold'])).capitalize()
								if safety_check in ['Y', '']:
									del index[topic_string].index[volume_to_be_deleted]
									valid_response_3 = True
								elif safety_check == 'N':
									valid_response_3 = True
								else:
									cprint('Invalid Response.', 'blue', attrs =['bold'])
									valid_response_3 = False
							valid_response_2 = True
						else:
							cprint("Topic '" + topic_string + "' is not in vol. " + volume_to_be_deleted + '.','blue',attrs=['bold'])
							valid_response_2 = False
					valid_response_1 = True
			elif topic_string == 'Exit':
				break
			else:
				cprint('Topic ' + topic_string + ' not in Index.','blue',attrs=['bold'])
				valid_response_1 = False
		valid_response_3 = False
		while valid_response_3 == False:
			cprint('-'*60,'white',attrs=['bold'])
			next_action = input(colored("Remove Another Volume Reference? ([y],n): ",'red',attrs=['bold'])).capitalize()
			if next_action in ['Y', '']:
				remove_another_volume_reference = True
				valid_response_3 = True
			elif next_action == 'N':
				remove_another_volume_reference = False
				valid_response_3 = True
			else:
				cprint('Invalid Response.', 'blue', attrs =['bold'])
				valid_response_3 = False
def delete_page(index):
	remove_another_page_reference = True
	while remove_another_page_reference == True:
		cprint('-'*60,'white',attrs=['bold'])
		cprint('Remove Page Reference','blue',attrs = ['bold','underline'])
		valid_response_1 = False
		while valid_response_1 == False:
			topic_string = input(colored('Topic: ','red',attrs = ['bold']))
			topic_string = " ".join(string.capwords(w) for w in re.split('-| ',topic_string))
			for letter in string.ascii_lowercase:
				topic_string = topic_string.replace("("+letter,"("+letter.capitalize())
			for article in [" A "," The ", " An ", " At ", " From ", " Of ", " W.r.t. "]:
				topic_string = topic_string.replace(article,article.lower())

			if topic_string in index.keys():
				valid_response_2 = False
				while valid_response_2 == False:
					volume_string = input(colored('Volume: ','red', attrs = ['bold']))
					if volume_string in index[topic_string].index.keys():
						if len(index[topic_string].index[volume_string])==1:
							cprint("Topic '" + topic_string + "' in vol. " + volume_string + \
									" has only 1 reference. \nSwitch to either Delete Topic or " + \
									"Remove Volume Reference.",\
									'blue',attrs=['bold'])
						else:
							valid_response_3 = False
							while valid_response_3 == False:
								page_to_delete = int(input(colored('Page: ','red',attrs=['bold'])))
								if page_to_delete in index[topic_string].index[volume_string]:
									valid_response_4 = False
									while valid_response_4 == False:
										safety_check = input(colored("Are you sure you want to remove the index of '" + topic_string +\
																		"' in vol. " + volume_string + ", p. " \
																		+ str(page_to_delete) + "? ([y],n): ",\
																		'red', attrs = ['bold'])).capitalize()
										if safety_check in ['Y', '']:
											index_of_page = index[topic_string].index[volume_string].index(page_to_delete)
											del index[topic_string].index[volume_string][index_of_page]
											valid_response_4 = True
										elif safety_check == 'N':
											valid_response_4 = True
										else:
											cprint('Invalid Response.', 'blue', attrs =['bold'])
											valid_response_4 = False
									valid_response_3 = True
								else:
									cprint("Page " + str(page_to_delete) + " in vol. " + volume_string \
												+ " does not include topic '" + topic_string + "'.", 'blue', attrs = ['bold'])
									valid_response_3 = False
						valid_response_2 = True
					else:
						cprint("Topic '" + topic_string + "' is not in vol. " + volume_string + '.','blue',attrs=['bold'])
						valid_response_2 = False
				valid_response_1 = True
			else:
				cprint("Topic '" + topic_string + "' not in Index.",'blue',attrs=['bold'])
				valid_response_1 = False
		valid_response_5 = False
		while valid_response_5 == False:
			cprint('-'*60,'white',attrs=['bold'])
			next_action = input(colored("Remove Another Page Reference? ([y],n): ",'red',attrs=['bold'])).capitalize()
			if next_action in ['Y', '']:
				remove_another_page_reference = True
				valid_response_5 = True
			elif next_action == 'N':
				remove_another_page_reference = False
				valid_response_5 = True
			else:
				cprint('Invalid Response.', 'blue', attrs =['bold'])
				valid_response_5 = False
def generate_latex_file(index):
	generate_another_latex_file = True
	while generate_another_latex_file == True:
		cprint('-'*60,'white',attrs=['bold'])
		cprint('Generate Index for Volume Number','blue',attrs = ['bold','underline'])
		valid_response_1 = False
		while valid_response_1 == False:
			volume_number = input(colored('Volume: ','red',attrs = ['bold'])).capitalize()
			if volume_number == "Cancel":
				valid_response_1 = True
				generate_another_latex_file = False
			else:
				if volume_number.capitalize() == 'All':
					volume_number = None
					filename = "CompleteIndex.tex"
				else:
					volume_number = int(volume_number)
					filename = "Volume" + str(volume_number) + "Index.tex"
				print_index(filename,volume=volume_number)
				valid_response_1 = True
				generate_another_latex_file = False
				platform_name = platform.system()
				if platform_name == 'Windows':
					pdflatex_cmd = "pdflatex " + filename + " >nul 2>nul"
					if volume_number == None:
						commit_message = 'git commit --quiet -m "Building Complete Index!"'
					else:
						commit_message = 'git commit --quiet -m "Adding to Volume ' +volume_number+ ' Index!"'
					subprocess.call(pdflatex_cmd,shell=True)
					subprocess.call("git add .", shell = True)
					subprocess.call(commit_message, shell = True)
					subprocess.call("git push --quiet origin master", shell = True)
				else:
					pdflatex_cmd = "pdflatex " + filename + " &> /dev/null"
					if volume_number == None:
						commit_message = "git commit --quiet -m 'Building Complete Index!'"
					else:
						commit_message = "git commit --quiet -m 'Adding to  Volume " + str(volume_number) + " Index!'"
					subprocess.call(args=[pdflatex_cmd],shell=True)
					subprocess.call(args=["git add ."], shell = True)
					subprocess.call(args=[commit_message], shell = True)
					subprocess.call(args=["git push --quiet origin master"], shell = True)
def options(index):
	exit_options = False
	while exit_options == False:
		cprint('-'*60,'white',attrs=['bold'])
		cprint('Options','blue',attrs=['bold','underline'])
		cprint('\n- List All References          (1)'+\
			   '\n- Print Reference              (2)'+\
			   '\n- Delete Reference             (3)'+\
			   '\n- Delete Volume Reference      (4)'+\
			   '\n- Delete Page Reference        (5)'+\
			   '\n- Print Volume Index (Latex)   (6)'+\
			   '\n- [Exit]\n','blue',\
			   attrs=['bold'])
		cprint('-'*60,'white',attrs=['bold'])
		action_string = colored('Desired Action: ','red',attrs = ['bold'])
		action = input(action_string).capitalize()
		if action in ['Exit', '']:
			exit_options = True
		elif action == '1':
			list_references(index)
			exit_options = True
		elif action == '2':
			print_single_reference(index)
			exit_options = True
		elif action == '3':
			delete_topic(index)
			exit_options = True
		elif action == '4':
			delete_volume(index)
			exit_options = True
		elif action == '5':
			delete_page(index)
			exit_options = True
		elif action == '6':
			generate_latex_file(index)
			exit_options = True
		else:
			cprint('Invalid Response.','blue',attrs=['bold'])
			exit_options = False
def index_from_letter(latexfile,letters,index,volume,keys):
	for letter in letters:
		latexfile.write("\\textit{"+letter+"\\hspace{0.5em}} \\\\")
		for key in sorted(keys):
			if key[0] == letter: latexfile.write(index[key].print_topic(volume =volume))
def print_index(filename,volume=None):
	alphabet = []
	keys = []
	if __name__=='__main__':
		with open('journalindeces.pkl', 'rb') as f:
		    index = pickle.load(f)
	if volume == None:
		keys = index.keys()
		for key in keys:
			alphabet.append(key[0])
	else:
		for key in index.keys():
			if str(volume) in index[key].index.keys():
				keys.append(key)
				alphabet.append(key[0])
	# for key in index.keys():
	# 	if volume == None:
	# 		alphabet.append(key[0])
	# 	else:
	# 		if str(volume) in index[key].index.keys():
	# 			alphabet.append(key[0])
	alphabet = sorted(list(set(alphabet)))

	latexfile = open(filename,"w")
	latexfile.write("\\documentclass[a4paper]{article} \n" + \
						"\\usepackage[english]{babel} \n" + \
						"\\usepackage[utf8x]{inputenc} \n" + \
						"\\usepackage[T1]{fontenc} \n" + \
						"\\usepackage{ragged2e} \n" + \
						"\\usepackage{amsmath} \n" + \
						"\\usepackage[a4paper,top=3cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry} \n" + \
						"\\begin{document} \n" + \
						"\\section*{Index} \n" + \
						"\\allowdisplaybreaks \n" + \
						"\\begin{flalign*} \n")
	for key in sorted(keys):
		if key[0] not in alphabet:
			latexfile.write(index[key].print_topic(volume=volume))
	index_from_letter(latexfile,alphabet,index,volume,keys)
	latexfile.write("\\end{flalign*} \n")
	latexfile.write("\\end{document}")
	latexfile.close()
def clean_up(index):
	all_topics = index.keys()
	for topic in all_topics:
		volumes = index[topic].index.keys()
		for volume in volumes:
			index[topic].index[volume] = list(set(index[topic].index[volume]))
def print_documentation():
	cprint('-'*60,'white',attrs=['bold'])
	cprint('Program Documentation','blue',attrs = ['bold','underline'])
	def margins(string):
		if string == None:
			string = "Lorem ipsum dolor sit amet, ipsum nonumy diceret pri ad. Quod doming labitur mei ea. Meis vidit te nam. Id fuisset senserit eum, esse contentiones voluptatibus per in. Pri libris mucius suscipiantur in, id detracto constituam pri. Est cibo lucilius id, quo no debitis atomorum conclusionemque. Cu dicam dicunt eos, agam dicam te vix. Vero fabellas ea pri. Posse dolor sed an. Zril facete dictas te mea, quot vivendo cum at. Usu ut phaedrum aliquando, postea delenit ea pri. Ex iisque tibique eam. Meis utinam primis eos ex, porro vituperata complectitur has ad. Mea ad quot tantas tamquam. Ne eam amet vidisse percipit, sint aliquip eu vis. Ex vis utinam animal urbanitas."
		if len(string) < 60:
			return(string)
		else:
			import math
			nlines = math.ceil(len(string)/60)
			breakpoint = 60
			i = 1
			while i < nlines-1:
				if ' ' not in string[breakpoint:] and \
						list(reversed(string[:breakpoint])).index(' ')>=3 and \
							len(string[breakpoint:])>=3:
					string = string[:breakpoint] + '-\n   ' + string[breakpoint:]
					nlines = (i+1) + math.ceil(len(string[(breakpoint+2):])/60)
					breakpoint += 60 + 2 + 3
					i += 1
				elif ' ' not in string[breakpoint:]:
					nearest_space = list(reversed(string[:breakpoint])).index(' ')
					breakpoint = breakpoint-nearest_space
					string = string[:breakpoint] + '\n   ' + \
					 			string[breakpoint:]
					nlines = (i+1) + math.ceil(len(string[(breakpoint+1):])/60)
					breakpoint += 60 + 1 + 3
					i += 1
				elif string[breakpoint:].index(' ')==1:
					nearest_space = list(reversed(string[:breakpoint])).index(' ')
					breakpoint = breakpoint-nearest_space
					string = string[:breakpoint] + '\n   ' + \
					 			string[breakpoint:]
					nlines = (i+1) + math.ceil(len(string[(breakpoint+1):])/60)
					breakpoint += 60 + 1 + 3
					i += 1
				elif list(reversed(string[:breakpoint])).index(' ')>=3 and \
						string[breakpoint:].index(' ')>=3:
					string = string[:breakpoint] + '-\n   ' + string[breakpoint:]
					nlines = (i+1) + math.ceil(len(string[(breakpoint+2):])/60)
					breakpoint += 60 + 2 + 3
					i += 1
				else:
					nearest_space = list(reversed(string[:breakpoint])).index(' ')
					breakpoint = breakpoint-nearest_space
					string = string[:breakpoint] + '\n   ' + \
					 			string[breakpoint:]
					nlines = (i+1) + math.ceil(len(string[(breakpoint+1):])/60)
					breakpoint += 60 + 1 + 3
					i += 1
			string = '\n' + string + '\n'
			return(string)
	documentation = \
	margins(" - This program is designed to index all of the notes taken in numbers notebooks for easier intra- and inter-volume searching.") + \
	"\n" + \
	'~'*60 + \
	"\n" + \
	"Shortcuts:\n" + \
	'~'*60 + \
	"\n" + \
	margins(" - Options Menu: Typing 'options' in the add topic/vol/page environment or the additional pages environment will bring up the options menu.") + \
	margins(" - Searching: Using '>' before any topic can be used to search for an existing topic. This search is automatically done while printing or deleting topics in the options menu.") + \
	margins(" - Quick Volume Ammend: Using the format (vol)page can quickly ammend any journal entry in any volume (even in new volumes if desired).") + \
	margins(" - Current Volume Inquiry: In the add topic/vol/page enviroment, the command 'current volume?' will bring up the current volume number.") + \
	margins(" - Changing Current Volume: Likewise, typing in 'change volume' will result in a prompt to change the current volume. This can be used to back ammend volumes or to add new volumes.") + \
	margins(" - Clean up: Typing in 'clean up' will initiate a subprogram that will make sure that there are no duplicate entries in the dictionary.") + \
	margins(" - Cancelling: Typing in 'cancel' at any point during this program will cancel the current operation and return the user to the additional entries query.") + \
	margins(" - Exiting: Additionally, typing in 'exit' will exit the program all together and initiate the saving and committing of the new files.")
	cprint(documentation,'white')

if __name__=='__main__':
	with open('journalindeces.pkl', 'rb') as f:
	    index = pickle.load(f)
current_volume = max([max([int(el) for el in list(index[key].index.keys())]) for key in index.keys()])
additional_entry = True
while additional_entry == True:
	exit_prompt = False
	cprint('-'*60,'white',attrs=['bold'])
	topic_string = colored('Topic: ', 'red', attrs = ['bold'])
	topic_response = input(topic_string)
	topic_response = " ".join(string.capwords(w) for w in re.split('-| ',topic_response))
	for letter in string.ascii_lowercase:
		topic_response = topic_response.replace("("+letter,"("+letter.capitalize())
	for article in [" A "," The ", " An ", " At ", " From ", " Of ", " W.r.t. "]:
		topic_response = topic_response.replace(article,article.lower())
	if topic_response != '\x1b[a': topic = topic_response
	if topic == "Exit":
		cprint('-'*60,'white',attrs=['bold'])
		break
	elif topic == "Options":
		options(index)
	elif topic == "Volume?":
		cprint("Current Volume: " + str(current_volume),'blue')
	elif topic == "Change Volume":
		current_volume = input(colored("Change from Volume " + str(current_volume) + " to Volume: " ,'red',attrs = ['bold']))
	elif topic == "Clean Up":
		clean_up(index)
	elif topic == 'Help':
		print_documentation()
	else:
		if topic[0] == ">":
			topic = topic[1:]
			topic = " ".join(string.capwords(w) for w in re.split('-| ',topic))
			for letter in string.ascii_lowercase:
				topic = topic.replace("("+letter,"("+letter.capitalize())
			for article in [" A "," The ", " An ", " At ", " From ", " Of ", " W.r.t. "]:
				topic = topic.replace(article,article.lower())
			potential_keys = []
			for key in index.keys():
				if key[:len(topic)] == topic:
					potential_keys.append(key)
			if len(potential_keys)==0:
				cprint("No references matched your search.", 'blue', attrs = ['bold'])
			else:
				cprint('-'*60,'white',attrs=['bold'])
				cprint('Search Results','blue',attrs = ['bold','underline'])
				[cprint(str(i+1) + " - " + potential_keys[i], 'white') for i in range(len(potential_keys))]
				exit_search_results = False
				while exit_search_results == False:
					cprint('-'*60,'white',attrs=['bold'])
					response_3 = input(colored("Select Reference Number: ", 'red', attrs = ['bold']))
					if response_3.capitalize() == "Exit":
						cprint('-'*60,'white',attrs=['bold'])
						additional_entry = False
						exit_prompt = True
						break
					elif response_3.capitalize() == "Cancel":
						exit_prompt = False
						break
					else:
						try:
							if int(response_3)-1 not in range(len(potential_keys)):
								cprint('-'*60,'white',attrs=['bold'])
								cprint('Number option not listed.', 'blue', attrs = ['bold'])
								exit_search_results = False
							else:
								topic = potential_keys[int(response_3)-1]
								new_page = False
								while new_page == False:
									page_string = colored('Page: ', 'red', attrs = ['bold'])
									page = input(page_string).capitalize()
									if page == "Exit":
										cprint('-'*60,'white',attrs=['bold'])
										exit_search_results = True
										additional_entry = False
										exit_prompt = True
										break
									elif page == "Cancel":
										exit_search_results = True
										exit_prompt = False
										break
									else:
										if page[0] == '(':
											volume = int(page[1:page.index(')')])
											page = [int(page[page.index(')')+1:])]
										elif '-' in page:
											page = [int(page[:page.index('-')]),\
														int(page[page.index('-')+1:])]
											volume = current_volume
										else:
											page = [int(page)]
											volume = current_volume
										if topic in index.keys():
											if str(volume) not in index[topic].index.keys():
												new_page = True
											elif len(page)==2:
												if np.array([p in index[topic].index[str(volume)]\
														for p in range(page[0],page[1])]).any():
													overlapping_pages=list(filter(lambda x: x in index[topic].index[str(volume)], range(page[0],page[1]+1)))
													if len(overlapping_pages)==1:
														overlapping_pages_string = str(overlapping_pages[0])
													else:
														overlapping_pages_string = str(overlapping_pages[0])
														for i in range(1,len(overlapping_pages)):
															overlapping_pages_string += ", "*(len(overlapping_pages)!=2) + " & "*(len(overlapping_pages)==2) + "& "*(i == len(overlapping_pages)-1) +  str(overlapping_pages[i])

													cprint("Page(s) " + overlapping_pages_string + " already referenced in vol. " + str(volume) \
															+ " for topic '" + topic + "'.", 'blue', attrs = ['bold'])
													new_page = False
												else:
													new_page = True
											elif page in index[topic].index[str(volume)]:
												cprint("Page " + str(page) + " in vol. " + str(volume) \
														+ " is already indexed for topic '" + topic + "'.", 'blue', attrs = ['bold'])
												new_page = False
											else:
												new_page = True
										else:
											new_page = True
								if page not in ["Cancel","Exit"]:
									if topic not in index.keys():
										index[topic] = index_topic(topic,volume,page)
									else:
										index[topic].add_pages_to_volume(volume,page)
								exit_search_results = True
						except ValueError:
							cprint('Invalid Response.', 'blue', attrs =['bold'])
							exit_search_results = False
		else:
			new_page = False
			while new_page == False:
				page_string = colored('Page: ', 'red', attrs = ['bold'])
				page = input(page_string).capitalize()
				if page == "Exit":
					cprint('-'*60,'white',attrs=['bold'])
					additional_entry = False
					exit_prompt = True
					break
				elif page == "Cancel":
					exit_prompt = False
					break
				else:
					if page[0] == '(':
						volume = int(page[1:page.index(')')])
						page = [int(page[page.index(')')+1:])]
					elif '-' in page:
						page = [int(page[:page.index('-')]),\
									int(page[page.index('-')+1:])]
						volume = current_volume
					else:
						page = [int(page)]
						volume = current_volume
					if topic in index.keys():
						if str(volume) not in index[topic].index.keys():
							new_page = True
						elif len(page)==2:
							if np.array([p in index[topic].index[str(volume)]\
									for p in range(page[0],page[1])]).any():
								overlapping_pages=list(filter(lambda x: x in index[topic].index[str(volume)], range(page[0],page[1]+1)))
								if len(overlapping_pages)==1:
									overlapping_pages_string = str(overlapping_pages[0])
								else:
									overlapping_pages_string = str(overlapping_pages[0])
									for i in range(1,len(overlapping_pages)):
										overlapping_pages_string += ", "*(len(overlapping_pages)!=2) + " & "*(len(overlapping_pages)==2) + "& "*(i == len(overlapping_pages)-1) +  str(overlapping_pages[i])

								cprint("Page(s) " + overlapping_pages_string + " already referenced in vol. " + str(volume) \
										+ " for topic '" + topic + "'.", 'blue', attrs = ['bold'])
								new_page = False
							else:
								new_page = True
						elif page in index[topic].index[str(volume)]:
							cprint("Page " + str(page) + " in vol. " + str(volume) \
									+ " is already indexed for topic '" + topic + "'.", 'blue', attrs = ['bold'])
							new_page = False
						else:
							new_page = True
					else:
						new_page = True
			if page not in ["Cancel","Exit"]:
				if topic not in index.keys():
					index[topic] = index_topic(topic,volume,page)
				else:
					index[topic].add_pages_to_volume(volume,page)

	while exit_prompt == False:
		cprint('-'*60,'white',attrs=['bold'])
		response_string = colored("Additional Entries? ([y]/n): ",'red',attrs=['bold'])
		response = input(response_string).capitalize()
		if response not in ['Y','','N','Options']:
			cprint('Invalid Response. ','blue',attrs = ['bold'])
			exit_prompt=False
		elif response in ['Y','']:
			additional_entry=True
			exit_prompt=True
		elif response == 'Options':
			options(index)
			exit_prompt = False
		else:
			cprint('-'*60,'white',attrs=['bold'])
			additional_entry=False
			exit_prompt=True

alphabet = []
for key in index.keys():
	alphabet.append(key[0])
alphabet = sorted(list(set(alphabet)))

pickle.dump(index,open('journalindeces.pkl','wb'),pickle.HIGHEST_PROTOCOL)

print_index("CompleteIndex.tex")
