import sys
from itertools import islice


searchfile = open("./HM_Date_2012070100.html", "r")
for line in searchfile:
    if ('Obstype     ') in line: 
        #the following line will store the next two lines in a list
        #the first element will be the line ------
        next_two=list(islice(searchfile, 2))
        obstype = line.split()[1]
        if 'Codetype' in next_two[1]:
            #print(line)
            #print(next_two[1])
            #print(next_two[1].split())
            codetype=next_two[1].split()[1]
            print("Obstype: %s Codetype: %s"%(obstype,codetype))
        #print(list(islice(searchfile, 2))[1])
        #print(list(islice(searchfile, 4))[-1])
        #sys.exit()
        #for _ in range(2):
        #    print(searchfile.readline())
searchfile.close()
