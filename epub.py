import os

after_sec = 0
tit_no = 8
 
with open('ch03-git-branching.xhtml') as read_f,open('.ch03-git-branching.xhtml.swap','w') as write_f:
    for line in read_f:
    	if line.find('section') > 0:
    		after_sec = 1
    		continue
    	if after_sec == 1 and line.find('id') > 0 and line.find('h2') > 0:
    		line = line.replace('">8', '">')
    		after_sec = 0
    	write_f.write(line)
    		
        # line=line.replace('SB','h2')
        # write_f.write(line)
 
os.remove('ch03-git-branching.xhtml')
os.rename('.ch03-git-branching.xhtml.swap','ch03-git-branching.xhtml')

