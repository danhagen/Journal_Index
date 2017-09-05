import pickle
import numpy as np
from termcolor import cprint,colored
import platform
import subprocess
import ipdb

class index_topic:

	def __init__(self,topic,volume,page):
		assert type(int(volume))==int, colored("Volume must be an integer.",'green',attrs=['bold'])
		assert np.array([type(int(el))==int for el in page]).all(), colored("Page must be an integer.",'green',attrs=['bold'])
		self.topic = topic
		self.volume = volume
		if len(page)!=2:
			self.page = page
			self.index = {str(volume):[page]}
		else:
			self.page = list(range(page[0],page[1]))
			self.index = {str(volume):list(range(page[0],page[1]+1))}

	def add_pages_to_volume(self, volume, page):
		if str(volume) not in self.index.keys():
			if len(page)!=2:
				self.index[str(volume)] = [page]
			else:
				self.index[str(volume)] = list(range(page[0],page[1]+1))
		else:
			if len(page)!=2:
				self.index[str(volume)].append(page)
			else:
				[self.index[str(volume)].append(p) for p in list(range(page[0],page[1]+1))]
	def print_topic(self,volume=None):
		if volume == None:
			keys = np.sort([int(key) for key in self.index.keys()])
		else:
			assert type(volume)==int,"Volume must be an integer."
			if str(volume) not in self.index.keys():
				keys = []
			else:
				keys = [volume]
		output = "&\\text{" + self.topic +"} \\hspace*{6em}"
		for j in range(len(keys)):
			pages = list(set(self.index[str(keys[j])]))
			pages = np.sort(pages)
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
								if discontinuity_indicator[i-1] != 0:
									pages_string += ", " + str(pages[i+1])
								else:
									pages_string += "-" + str(pages[i]) + ", " + str(pages[i+1])
					else:
						for i in range(2,len(discontinuity_indicator-1)):
							if discontinuity_indicator[i] != 0:
								if discontinuity_indicator[i-1] != 0:
									pages_string += ", " + str(pages[i+1])
								else:
									pages_string += "-" + str(pages[i]) + ", " + str(pages[i+1])
						pages_string += "-" + str(pages[-1])
				else:
					if discontinuity_indicator[-1] != 0:
						for i in range(1,len(discontinuity_indicator)):
							if discontinuity_indicator[i] != 0:
								if discontinuity_indicator[i-1] != 0:
									pages_string += ", " + str(pages[i+1])
								else:
									pages_string += "-" + str(pages[i]) + ", " + str(pages[i+1])
					else:
						for i in range(1,len(discontinuity_indicator-1)):
							if discontinuity_indicator[i] != 0:
								if discontinuity_indicator[i-1] != 0:
									pages_string += ", " + str(pages[i+1])
								else:
									pages_string += "-" + str(pages[i]) + ", " + str(pages[i+1])
						pages_string += "-" + str(pages[-1])
			if j == 0:
				if volume != None:
					output +=  "&&" + pages_string + "\\\\" + "\n"
				else:
					output +=  "&& vol. " + str(keys[j]) + ": " + pages_string + "\\\\" + "\n"
			else:
				output += "& && vol. " + str(keys[j]) + ": " + pages_string + "\\\\" + "\n"
		return(output)
