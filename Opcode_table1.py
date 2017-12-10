instructions=["mov","add","repnz","xor","std","lodsb","cld","stosb","loop","sub"]
OPCODES={}	# opcodes dictionaryww
def Read_opcode_table_inst():
    fp = open("opcode_table_inst.txt","r")
    data=fp.read()
    data=data.split("\n")
    key=""
    for i in data:
        if i is not '':
            newData=i.split(" ")
            if newData[0] in instructions:
                key=newData[0]
                OPCODES[key]={}
            else:
                key2=newData[1]+newData[2]
                OPCODES[key][key2]=newData[0]#[newData[1],newData[2],newData[0]]
def get_opcode_instruction(inst,op1op2):
    try:
        code=OPCODES[inst][op1op2]
        return code
    except Exception:
        return ''
def getNumber(reg,code):
    for i in code:
        if reg in i:
            return i[0],i[1]
    return '',''
def Find_reg_opcode(reg1,reg2,code):
    no1,binary=getNumber(reg1,code[0])
    no2,binary=getNumber(reg2,code[0])
    no1=int(no1)
    no2=int(no2)
    exactCodes=code[1]
    return exactCodes[no2][no1]

#Read 32 bit register mod bit and registers codes 000 001 010 100

def Mod_bit_registers_code():#register opcodes
    #code=[]     #get code form 0compare 1codes
    compares,code,opcode=[],[],[]
    #opcode=[]
    fp=open("opcodes.txt","r")
    for i in range(1,9):
        data=fp.readline()
        data=data.replace("\n","")
        temp=data.split(" ")
        compares.append(temp)
    for i in range(0,1):
        mod=fp.readline()
        mod=mod.replace("\n","")
        for i in range(0,8):
            data=fp.readline()
            data=data.replace("\n","")
            temp=data.split(",")
            opcode.append(temp)
    code=[compares,opcode]
    #print(code)
    return code #Find(reg1,reg2,code)  #function call

#Read_file("eax","ebx")
Read_opcode_table_inst()
#s=get_opcode_instruction("mov","r8","m8")
