file=open("../sheets/Instructions.txt")
text=file.read()
file.close()
lines=[line.strip() for line in text.splitlines()]
lines=lines[lines.index("Micro Code:")+2:]
lines=[line for line in lines if len(line)>0]
hexadec="0123456789abcdef"
microInstructions={"pc out":0x00000001,
                   "mar in":0x00000002,
                  "ram out":0x00000004,
                     "i in":0x00000008,
                   "pc inc":0x00000010,
                   "pc set":0x00000020,
                   "ram in":0x00000040,
            "reset counter":0x00000080,
                     "a in":0x00000100,
                     "b in":0x00000200,
                  "alu out":0x00000400,
                    "ax in":0x00000800,
                    "bx in":0x00001000,
                    "cx in":0x00002000,
                    "dx in":0x00004000,
                   "ax out":0x00008000,
                   "bx out":0x00010000,
                   "cx out":0x00020000,
                   "dx out":0x00040000,
                     "halt":0x00080000,
                   "bp out":0x00100000,
                    "bp in":0x00200000,
                   "sp out":0x00400000,
                    "sp in":0x00800000,
                   "si out":0x01000000,
                    "si in":0x02000000,
                   "di out":0x04000000,
                    "di in":0x08000000,
                       "ja":0x10000000,
                      "jna":0x20000000,
                       "je":0x30000000,
                      "jne":0x40000000,
                       "jb":0x50000000,
                      "jnb":0x60000000,
                       "jg":0x70000000,
                      "jng":0x80000000,
                       "jl":0x90000000,
                      "jnl":0xa0000000}
opcode=""
instructions={}
for line in lines:
    if len(line)>4 and line[0] in hexadec and line[1] in hexadec and line[2] in hexadec and line[3] in hexadec:
        opcode=int(line[:4],16)
        instructions[opcode]=[]
    else:
        instructions[opcode].append(line.split(", "))
encodedList=["v2.0 raw"]
for i in range(2**16):
    if i not in instructions:
        encodedList.append(" ".join(["0"]*16))
    else:
        line=["0"]
        for mCode in instructions[i]:
            mCodeEncoded=0
            for mInstruction in mCode:
                mCodeEncoded+=microInstructions[mInstruction]
            line.append(hex(mCodeEncoded)[2:])
        while len(line)<16:
            line.append("0")
        encodedList.append(" ".join(line))
file=open("Micro Instructions","w")
file.write("\n".join(encodedList))
file.close()
print("done")
