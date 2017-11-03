import sys

"""
give code name with .16b extension
"""

file=open(sys.argv[1])
code=file.read()
file.close()

# variables are defined by a -
vars={}
# labels are difined by a :
labels={}

code=code.splitlines()
code=[line.strip().split() for line in code if len(line.strip())>0]

for line in code:
    if line[0][0]=="-":
        vars[line[0]]=-1
    elif line[0][0]==":":
        labels[line[0]]=-1
    

file=open(sys.argv[1].replace(".16b",".bin"),"w")
file.write("v2.0 raw")
file.close()
