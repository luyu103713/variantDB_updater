import optparse

def test_parse():
	usage = 'Usage: %prog [options] arg1 arg2 ...'
	parser = optparse.OptionParser(usage,version='%prog 1.0')
	parser.add_option('-f','--file',action='store',dest='filename',metavar='FILE',help='write output to FILE')
	(options,args)=parser.parse_args()
	print(parser.filename)


def main():
	test_parse()

if __name__ == '__main__':
	main()