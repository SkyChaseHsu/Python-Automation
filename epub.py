import os

def add_tit_no (filename, cpt_no):

	# Mark if the <h2> is below a <section>
	# - Beause every chapter title dose
	after_sec = 0

	# No in 2nd level, e.g. 3.1
	sec_no = 1
	with open(filename) as read_f,open('temp.swap','w') as write_f:
		for line in read_f:

			# Find the section, mark it
			if line.find('section') > 0:
				after_sec = 1
				continue

			# find the h2 and checkout if there is a section right above
			if after_sec == 1 and line.find('id') > 0 and line.find('h2') > 0:
				line = line.replace('">', '">' + str(cpt_no) + '.' + str(sec_no) + ' ')
				sec_no += 1
				after_sec = 0
			write_f.write(line)

	os.remove(filename)
	os.rename('temp.swap', filename)

add_tit_no('A.xhtml', 'A1')
add_tit_no('B.xhtml', 'A2')
add_tit_no('C.xhtml', 'A3')

