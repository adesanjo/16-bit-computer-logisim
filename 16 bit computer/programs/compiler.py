import sys

"""
give code name with .16b extension
"""

file=open(sys.argv[1])
code=file.read()
file.close()

def hexadec(n):
    if n>=2**15 or n<-2**15:
        raise Exception(str(n)+"is not a valid number")
    return hex(n if n>=0 else 2**16+n)

regs=("ax","bx","cx","dx","bp","sp")
regnums={"ax":"0","bx":"1","cx":"2","dx":"3","bp":"4","sp":"5"}
jumps={"jmp":0,"ja":1,"jnbe":1,"jna":2,"jbe":2,"je":3,"jne":4,"jb":5,"jnae":5,"jnb":6,
"jae":6,"jg":7,"jnle":7,"jng":8,"jle":8,"jl":9,"jnge":9,"jnl":10,"jge":10,"jz":11,"jnz":12}

# variables are defined by a *
var={}
# labels are difined by a :
labels={}

code=code.splitlines()
code=[line.strip().split() for line in code if len(line.strip())>0 and line.strip()[0]!="#"]

wordsList=[4]

for i,line in enumerate(code):
    words=0
    if line[0][0]=="*":
        var[line[0]]=(i,len(line)-1)
    elif line[0][0]==":":
        labels[line[0]]=hexadec(wordsList[-1])[2:]
    elif line[0] in ("mov","add","sub","mul","div","cmp","shl","shr","sar","rol","ror","and","or","xor"):
        words+=1
        if (line[1] not in regs and line[1][1:-1] not in regs) or (line[2] not in regs and line[2][1:-1] not in regs):
            words+=1
        if (line[1] not in regs and line[1][1:-1] not in regs) and (line[2] not in regs and line[2][1:-1] not in regs):
            words+=1
    elif line[0] in ("out","inc","dec","push","pop","not","neg"):
        words+=1
        if line[1] not in regs and line[1][1:-1] not in regs:
            words+=1
    elif line[0] in ("halt","nop","enter","leave","ret"):
        words+=1
    elif line[0] in jumps or line[0]=="call":
        words+=2
    wordsList.append(wordsList[-1]+words)

compiledCode=["0014","ffff","0015","ffff"]
compiledVar=[]
words=wordsList[-1]

i=0
for v in var.keys():
    vv=var[v]
    for j in range(vv[1]):
        compiledVar.append(hexadec(int(code[vv[0]][j+1],0))[2:])
    var[v]=hexadec(words+i)
    i+=vv[1]

for line in code:
    if line[0][0] in("*",":"):
        continue
    if line[0]=="nop":
        compiledCode.append("0")
    elif line[0] in ("mov","add","sub","mul","div","shl","shr","sar","rol","ror","and","or","xor"):
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
            elif line[0]=="shl":
                compiledCode.append("11"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="shr":
                compiledCode.append("12"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="sar":
                compiledCode.append("13"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="rol":
                compiledCode.append("14"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="ror":
                compiledCode.append("15"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="and":
                compiledCode.append("16"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="or":
                compiledCode.append("17"+regnums[line[1]]+regnums[line[2]])
            elif line[0]=="xor":
                compiledCode.append("18"+regnums[line[1]]+regnums[line[2]])
        elif line[1] in regs and line[2][0]=="[" and line[2][1:-1] in regs:
            if line[0]=="mov":
                compiledCode.append("02"+regnums[line[1]]+regnums[line[2][1:-1]])
            elif line[0]=="add":
                compiledCode.append("05"+regnums[line[1]]+regnums[line[2][1:-1]])
            elif line[0]=="sub":
                compiledCode.append("08"+regnums[line[1]]+regnums[line[2][1:-1]])
            elif line[0]=="mul":
                compiledCode.append("0b"+regnums[line[1]]+regnums[line[2][1:-1]])
            elif line[0]=="div":
                compiledCode.append("0e"+regnums[line[1]]+regnums[line[2][1:-1]])
        elif line[1][0]=="[" and line[1][1:-1] in regs and line[2] in regs:
            if line[0]=="mov":
                compiledCode.append("03"+regnums[line[1][1:-1]]+regnums[line[2]])
            elif line[0]=="add":
                compiledCode.append("06"+regnums[line[1][1:-1]]+regnums[line[2]])
            elif line[0]=="sub":
                compiledCode.append("09"+regnums[line[1][1:-1]]+regnums[line[2]])
            elif line[0]=="mul":
                compiledCode.append("0c"+regnums[line[1][1:-1]]+regnums[line[2]])
            elif line[0]=="div":
                compiledCode.append("0f"+regnums[line[1][1:-1]]+regnums[line[2]])
        elif line[1] in regs and line[2] not in regs and (line[2][0] not in ("[","*") or line[2][:2]=="**"):
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
            elif line[0]=="shl":
                compiledCode.append("116"+regnums[line[1]])
            elif line[0]=="shr":
                compiledCode.append("126"+regnums[line[1]])
            elif line[0]=="sar":
                compiledCode.append("136"+regnums[line[1]])
            elif line[0]=="rol":
                compiledCode.append("146"+regnums[line[1]])
            elif line[0]=="ror":
                compiledCode.append("156"+regnums[line[1]])
            elif line[0]=="and":
                compiledCode.append("166"+regnums[line[1]])
            elif line[0]=="or":
                compiledCode.append("176"+regnums[line[1]])
            elif line[0]=="xor":
                compiledCode.append("186"+regnums[line[1]])
            compiledCode.append(hexadec(int(var[line[2][1:]] if line[2][:2]=="**" else line[2],0))[2:])
        elif line[1] in regs and line[2][0] in ("[","*"):
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
            elif line[0]=="shl":
                compiledCode.append("117"+regnums[line[1]])
            elif line[0]=="shr":
                compiledCode.append("127"+regnums[line[1]])
            elif line[0]=="sar":
                compiledCode.append("137"+regnums[line[1]])
            elif line[0]=="rol":
                compiledCode.append("147"+regnums[line[1]])
            elif line[0]=="ror":
                compiledCode.append("157"+regnums[line[1]])
            elif line[0]=="and":
                compiledCode.append("167"+regnums[line[1]])
            elif line[0]=="or":
                compiledCode.append("177"+regnums[line[1]])
            elif line[0]=="xor":
                compiledCode.append("187"+regnums[line[1]])
            compiledCode.append(hexadec(int(line[2][1:-1] if line[2][0]=="[" else var[line[2]],0))[2:])
        elif line[2] in regs and line[1][0] in ("[","*"):
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
            elif line[0]=="shl":
                compiledCode.append("118"+regnums[line[1]])
            elif line[0]=="shr":
                compiledCode.append("128"+regnums[line[1]])
            elif line[0]=="sar":
                compiledCode.append("138"+regnums[line[1]])
            elif line[0]=="rol":
                compiledCode.append("148"+regnums[line[1]])
            elif line[0]=="ror":
                compiledCode.append("158"+regnums[line[1]])
            elif line[0]=="and":
                compiledCode.append("168"+regnums[line[1]])
            elif line[0]=="or":
                compiledCode.append("178"+regnums[line[1]])
            elif line[0]=="xor":
                compiledCode.append("188"+regnums[line[1]])
            compiledCode.append(hexadec(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
        elif line[1][0] in ("[","*") and line[2] not in regs and (line[2][0] not in ("[","*") or line[2][:2]=="**"):
            if line[0]=="mov":
                compiledCode.append("0016")
            elif line[0]=="add":
                compiledCode.append("0046")
            elif line[0]=="sub":
                compiledCode.append("0076")
            elif line[0]=="mul":
                compiledCode.append("00a6")
            elif line[0]=="div":
                compiledCode.append("00d6")
            elif line[0]=="shl":
                compiledCode.append("1186")
            elif line[0]=="shr":
                compiledCode.append("1286")
            elif line[0]=="sar":
                compiledCode.append("1386")
            elif line[0]=="rol":
                compiledCode.append("1486")
            elif line[0]=="ror":
                compiledCode.append("1586")
            elif line[0]=="and":
                compiledCode.append("1686")
            elif line[0]=="or":
                compiledCode.append("1786")
            elif line[0]=="xor":
                compiledCode.append("1886")
            compiledCode.append(hexadec(int(var[line[2][1:]] if line[2][:2]=="**" else line[2],0))[2:])
            compiledCode.append(hexadec(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
        elif line[1][0] in ("[","*") and line[2][0] in ("[","*"):
            if line[0]=="mov":
                compiledCode.append("0018")
            elif line[0]=="add":
                compiledCode.append("0048")
            elif line[0]=="sub":
                compiledCode.append("0078")
            elif line[0]=="mul":
                compiledCode.append("00a8")
            elif line[0]=="div":
                compiledCode.append("00d8")
            elif line[0]=="shl":
                compiledCode.append("1187")
            elif line[0]=="shr":
                compiledCode.append("1287")
            elif line[0]=="sar":
                compiledCode.append("1387")
            elif line[0]=="rol":
                compiledCode.append("1487")
            elif line[0]=="ror":
                compiledCode.append("1587")
            elif line[0]=="and":
                compiledCode.append("1687")
            elif line[0]=="or":
                compiledCode.append("1787")
            elif line[0]=="xor":
                compiledCode.append("1887")
            compiledCode.append(hexadec(int(line[2][1:-1] if line[2][0]=="[" else var[line[2]],0))[2:])
            compiledCode.append(hexadec(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
    elif line[0] in ("not","neg"):
        if line[1] in regs:
            compiledCode.append(("196" if line[0]=="not" else "1a6")+regnums[line[1]])
        elif line[1][0] in ("[","*") and line[1][1:-1] in regs:
            compiledCode.append(("197" if line[0]=="not" else "1a7")+regnums[line[1][1:-1]])
        elif line[1][0] in ("[","*"):
            compiledCode.append("1976" if line[0]=="not" else "1a76")
            compiledCode.append(hexadec(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
    elif line[0] in ("inc","dec"):
        if line[1] in regs:
            compiledCode.append(("046" if line[0]=="inc" else "076")+regnums[line[1]])
        elif line[1][0] in ("[","*"):
            compiledCode.append("0047" if line[0]=="inc" else "0077")
            compiledCode.append(hexadec(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
    elif line[0]=="out":
        if line[1] in regs:
            compiledCode.append(("fff")+regnums[line[1]])
        elif line[1][0] in ("[","*"):
            compiledCode.append("fff6")
            compiledCode.append(hexadec(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
        elif  line[1] not in regs and line[1][0] not in ("[","*"):
            compiledCode.append("fff7")
            compiledCode.append(hexadec(int(line[1],0))[2:])
    elif line[0]=="halt":
        compiledCode.append("ffff")
    elif line[0]=="cmp":
        if line[1] in regs and line[2] in regs:
            compiledCode.append("10"+regnums[line[1]]+regnums[line[2]])
        elif line[1] in regs and line[2] not in regs and (line[2][0] not in ("[","*") or line[2][:2]=="**"):
            compiledCode.append("106"+regnums[line[1]])
            compiledCode.append(hexadec(int(var[line[2][1:]] if line[2][:2]=="**" else line[2],0))[2:])
        elif line[1] in regs and line[2][0] in ("[","*"):
            compiledCode.append("107"+regnums[line[1]])
            compiledCode.append(hexadec(int(line[2][1:-1] if line[2][0]=="[" else var[line[2]],0))[2:])
        elif line[1][0] in ("[","*") and line[2] not in regs and (line[2][0] not in ("[","*") or line[2][:2]=="**"):
            compiledCode.append("1076")
            compiledCode.append(hexadec(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
            compiledCode.append(hexadec(int(var[line[2][1:]] if line[2][:2]=="**" else line[2],0))[2:])
        elif line[1][0] in ("[","*") and line[2][0] in ("[","*"):
            compiledCode.append("1077")
            compiledCode.append(hexadec(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
            compiledCode.append(hexadec(int(line[2][1:-1] if line[2][0]=="[" else var[line[2]],0))[2:])
    elif line[0] in jumps:
        compiledCode.append("108"+hexadec(jumps[line[0]])[2:])
        compiledCode.append(labels[line[1]])
    elif line[0] in ("push","pop"):
        if line[1] in regs:
            compiledCode.append(("066" if line[0]=="push" else "077")+regnums[line[1]])
        elif line[1][0] in (":","*"):
            compiledCode.append("0666" if line[0]=="push" else "0776")
            compiledCode.append(hexadec(int(line[1][1:-1] if line[1][0]=="[" else var[line[1]],0))[2:])
        elif line[0]=="push" and line[1] not in regs and line[1][0] not in (":","*"):
            compiledCode.append("0667")
            compiledCode.append(hexadec(int(line[1],0))[2:])
    elif line[0]=="call":
        compiledCode.append("0668")
        compiledCode.append(labels[line[1]])
    elif line[0] in ("enter","leave","ret"):
        compiledCode.append("0669" if line[0]=="enter" else "0778" if line[0]=="ret" else "0779")

file=open(sys.argv[1].replace(".16b",".c16b"),"w")
file.write("v2.0 raw\n"+" ".join(compiledCode+compiledVar))
file.close()

print("done")
