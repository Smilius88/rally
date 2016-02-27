
# Rally Programming Puzzle
# Sean Young, Friday, Feb 26, 2016
#
# To run type python omc2.py -f [FILENAME]
# To see all options, type python omc2.py --help

from sys import argv, stdin, stderr, exit
import argparse, re

def omc(ifile, subs, pretty):

	f = ifile.read().split('\n')
	ifile.close()
	
	projEmployees, projectCount  = dict(), dict()

	for i, line in enumerate(f):
		line = subs(line)
		l = line.split("\t")
		try:
			project, name = l[0], l[1]
			project = int(project)
		except:
			# print stderr.write("Line %d improperly formatted :\"%s\"\n" % (i, line))
			continue

		if name not in projectCount:
			projectCount[name] = set()
		projectCount[name].add(project)

		if project not in projEmployees:
			projEmployees[project] = set()
		projEmployees[project].add(name)


	ans = []
	for project in projEmployees:
		num = set()
		for name in projEmployees[project]:
			num |= projectCount[name]
		ans.append((project, len(num)-1))

	if pretty:
		print "Mission ID".ljust(12), "# of other missions".ljust(25)
	else:
		print "Mission ID\t# of other missions"

	for t in sorted(ans):
		if pretty:
			print repr(t[0]).ljust(12), repr(t[1]).ljust(25)
		else:
			print "%d\t%d" % t




def liberal_sub(string):
		return re.sub('\s+', '\t', string)

def conservative_sub(string):
		return re.sub(' {2,}', '\t', string)

def make_parser():
	parser = argparse.ArgumentParser(description='Print how many other projects the employees of a given  project are working on')
	parser.add_argument('--file', '-f', type=argparse.FileType('r'), nargs='?', default = stdin, help='file containing which employees work on which projects. Input may also be received by input redirection')
	parser.add_argument('-p', action='store_true', help='Print output in fixed width columns. Otherwise output columns will be separated by tabs.')
	parser.add_argument('-l', dest='lwr', action='store_const', help='Treat all whitespace as separating colummns. By default, whitespace of 2 or more spaces, or one or more tabs, will be counted as a separator', const=liberal_sub, default=conservative_sub)
	return parser

if __name__ == "__main__":
	parser = make_parser()
	args = parser.parse_args()
	omc(args.file, args.lwr, args.p)	

