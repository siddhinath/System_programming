def Checker_key_available(key,data_struct):
	try:
		return data_struct[key]
	except Exception:
		return "Error"

def getBit(temp):#ip-string op-integer with no of bits
	temp=int(temp)
	if temp<256 and temp>(-256):
		return 8
	else:
		return 32
#check integer or not
def isConvertible(symbol):
	try:
		int(symbol)
		bits=getBit(symbol)
		return True,bits,hex(int(symbol)).lstrip("0x").rstrip("L") or "0"
	except ValueError:
		return False,0,""
def isHex(temp):
	try:
		int(temp,16)
		return True,8,hex(temp).lstrip("0x").rstrip("L") or "0"
	except ValueError:
		return False,0,""
def isChar(temp):
	if (ord(temp[0])==39) and (ord(temp[-1])==39) and len(temp)==3:
		return True,8,hex(ord(temp[1])).lstrip("0x").rstrip("L") or "0"
	else:
		return False,0,""

def replace_Parameter(line,param):
	val=line[1].split(" ")
	val[1]=val[1].split(",")
	for i in range(len(val[1])):
		if "%" in val[1][i]:
			j=val[1][i].replace("%","")
			j=int(j)
			new=str(param[j-1])
			val[1][i]=new
			break	
	val[1]=val[1][0]+","+val[1][1]
	val=val[0]+" "+val[1]
	line[1]=val
	return line

def Display_Macro_Expansion(filename):
	fp=open(filename,"r")
	for line in fp.readlines():
		print(line.replace("\n",""))
