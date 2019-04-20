import os

def add_tit_no (filename, cpt_no):
	after_sec = 0
	sec_no = 1
	with open(filename) as read_f,open('temp.swap','w') as write_f:
		for line in read_f:
			if line.find('section') > 0:
				after_sec = 1
				continue
			if after_sec == 1 and line.find('id') > 0 and line.find('h2') > 0:
				line = line.replace('">', '">' + str(cpt_no) + '.' + str(sec_no) + ' ')
				sec_no += 1
				after_sec = 0
			write_f.write(line)

	os.remove(filename)
	os.rename('temp.swap', filename)

add_tit_no('ch03-git-branching.xhtml',3)

