import os

def readConfig():

	if os.path.exists('config'):
		config_dict = {}
		f = open('config','r')
		ls =f.readlines()
		for l in ls:
			temp = l.strip().split(':')
			config_dict[temp[0]] = temp[1]
		return config_dict
	else:
		exit('Can not find config file , please download from github:......')




if __name__ == '__main__':
	main()