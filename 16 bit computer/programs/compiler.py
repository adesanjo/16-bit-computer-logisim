import sys

"""
give code name with .16b extension
"""

file=open(sys.argv[1])
code=file.read()
file.close()

regs=("ax","bx","cx","dx","bp","sp")
regnums={"ax":"0","bx":"1","cx":"2","dx":"3","bp":"4","sp":"5"}
jumps=["jmp","ja","jna","je","jne","jb","jnb","jg","jng","jl","jnl"]

# variables are defined by a -
var={}
# labels are difined by a :
labels={}

code=code.splitlines()
code=[line.strip().split() for line in code if len(line.strip())>0]

wordsList=[0]

for i,line in enumerate(code):
    words=0
    if line[0][0]=="-":
        var[line[0]]=i
    elif line[0][0]==":":
        labels[line[0]]=hex(wordsList[-1])[2:]
    elif line[0] in ("mov","add","sub","mul","div","cmp"):
        words+=1
        if line[1] not in regs or line[2] not in regs:
            words+=1
        if line[1] not in regs and line[2] not in regs:
            words+=1
    elif line[0] in ("out","halt","nop"):
        words+=1
    elif line[0] in jumps:
        words+=2
    wordsList.append(wordsList[-1]+words)

compiledCode=[]
compiledVar=[]
words=wordsList[-1]

for i,v in enumerate(var.keys()):
    compiledVar.append(hex(int(code[var[v]][1],0))[2:])
    var[v]=hex(words+i)

for line in code:
    if line[0][0] in("-",":"):
        continue
    if line[0]=="nop":
        compiledCode.append("0")
    elif line[0] in ("mov","add","sub","mul","div"):
        if line[1] in regs and line[2] in regs:
            if line[0]=="mov":
                compiledCode.append("01"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="add":
                compiledCode.append("04"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="sub":
                compiledCode.append("07"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="mul":
                compiledCode.append("0a"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="div":
                compiledCode.append("0d"+regnums[line[1]]+regnums[line[2]])
        elif line[1] in regs and line[2][0]=="[" and line[2][1:-1] in regs:
            if line[0]=="mov":
                compiledCode.append("02"+regnums[line[1][1:-1]]+regnums[line[2]])
            elif line[0]=="add":
                compiledCode.append("05"+regnums[line[1][1:-1]]+regnums[line[2]])
            elif line[0]=="sub":
                compiledCode.append("08"+regnums[line[1][1:-1]]+regnums[line[2]])
            elif line[0]=="mul":
                compiledCode.append("0b"+regnums[line[1][1:-1]]+regnums[line[2]])
            elif line[0]=="div":
                compiledCode.append("0e"+regnums[line[1][1:-1]]+regnums[line[2]])
        elif line[1][0]=="[" and line[1][1:-1] in regs and line[2] in regs:
            if line[0]=="mov":
                compiledCode.append("03"+regnums[line[1]]+regnums[line[2][1:-1]])
            elif line[0]=="add":
                compiledCode.append("06"+regnums[line[1]]+regnums[line[2][1:-1]])
            elif line[0]=="sub":
                compiledCode.append("09"+regnums[line[1]]+regnums[line[2][1:-1]])
            elif line[0]=="mul":
                compiledCode.append("0c"+regnums[line[1]]+regnums[line[2][1:-1]])
            elif line[0]=="div":
                compiledCode.append("0f"+regnums[line[1]]+regnums[line[2][1:-1]])
        elif line[1] in regs and line[2] not in regs and line[2][0] not in ("[","-"):
            if line[0]=="mov":
                compiledCode.append("001"+regnums[line[1]])
            elif line[0]=="add":
                compiledCode.append("004"+regnums[line[1]])
            elif line[0]=="sub":
                compiledCode.append("007"+regnums[line[1]])
            elif line[0]=="mul":
                compiledCode.append("00a"+regnums[line[1]])
            elif line[0]=="div":
                compiledCode.append("00d"+regnums[line[1]])
            compiledCode.append(hex(int(line[2],0))[2:])
        elif line[1] in regs and line[2][0] in ("[","-"):
            if line[0]=="mov":
                compiledCode.append("002"+regnums[line[1]])
            elif line[0]=="add":
                compiledCode.append("005"+regnums[line[1]])
            elif line[0]=="sub":
                compiledCode.append("008"+regnums[line[1]])
            elif line[0]=="mul":
                compiledCode.append("00b"+regnums[line[1]])
            elif line[0]=="div":
                compiledCode.append("00e"+regnums[line[1]])
            compiledCode.append(hex(int(line[2][1:-1] if line[2][0]=="[" else var[line[2]],0))[2:])
        elif line[2] in regs and line[1][0] in ("[","-"):
            if line[0]=="mov":
                compiledCode.append("003"+regnums[line[2]])
            elif line[0]=="add":
                compiledCode.append("006"+regnums[line[2]])
            elif line[0]=="sub":
                compiledCode.append("009"+regnums[line[2]])
            elif line[0]=="mul":
                compiledCode.append("00c"+regnums[line[2]])
            elif line[0]=="div":
                compiledCode.append("00f"+regnums[line[1]])
            compiledCode.append(hex(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
    elif line[0]=="out":
        compiledCode.append("fff"+regnums[line[1]])
    elif line[0]=="halt":
        compiledCode.append("ffff")
    elif line[0]=="cmp":
        if line[1] in regs and line[2] in regs:
            compiledCode.append("10"+regnums[line[1]]+regnums[line[2]])
        elif line[1] in regs and line[2] not in regs and line[2][0] not in ("[","-"):
            compiledCode.append("106"+regnums[line[1]])
            compiledCode.append(hex(int(line[2],0))[2:])
        elif line[1] in regs and line[2][0] in ("[","-"):
            compiledCode.append("107"+regnums[line[1]])
            compiledCode.append(hex(int(line[2][1:-1] if line[2][0]=="[" else var[line[2]],0))[2:])
        elif line[1][0] in ("[","-") and line[2] not in regs and line[2][0] not in ("[","-"):
            compiledCode.append("1076")
            compiledCode.append(hex(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
            compiledCode.append(hex(int(line[2],0))[2:])
        elif line[1][0] in ("[","-") and line[2][0] in ("[","-"):
            compiledCode.append("1077")
            compiledCode.append(hex(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
            compiledCode.append(hex(int(line[2][1:-1] if line[2][0]=="[" else var[line[2]],0))[2:])
    elif line[0] in jumps:
        compiledCode.append("108"+hex(jumps.index(line[0]))[2:])
        compiledCode.append(labels[line[1]])

file=open(sys.argv[1].replace(".16b",".c16b"),"w")
file.write("v2.0 raw\n"+" ".join(compiledCode+compiledVar))
file.close()

print("done")
