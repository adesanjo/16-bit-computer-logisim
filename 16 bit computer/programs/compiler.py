import sys

"""
give code name with .16b extension
"""

file=open(sys.argv[1])
code=file.read()
file.close()

code=code.splitlines()

file=open(sys.argv[1].replace(".16b",".bin"),"w")
file.write("v2.0 raw")
file.close()
