from newAssem_Data_Struct import *
from Header_File import *
import sys
def makeKey_macroname(data):
	value=data[1].split(" ")
	if len(value)<3:
		print("Error please pass name of macro with parameter,Line no-",data[0])
		sys.exit()
	value=value[1]+"@"+value[2]
	return value
#Code retrive all definitions of macro start= and end= retrive 
def Macro_retrive(index,data,macro_retrive,new):
	if len(data)==index:
		return macro_retrive,index
	if new!=0:
		macro_retrive["start"]=index+1
	if "%macro" in data[index][1]:
		key=makeKey_macroname(data[index])
		if Checker_key_available(key,macro_retrive)=="Error":
			macro_retrive[key]={}
			macro_retrive[key],re_index=Macro_retrive(index+1,data,{},1)
			macro_retrive,index=Macro_retrive(re_index+1,data,macro_retrive,0)
			return macro_retrive,index
		else:
			print("Macro redefine. Line no-",data[index][0])
			sys.exit()
	elif "endmacro" in data[index][1]:
		macro_retrive["end"]=index
		return macro_retrive,index
	else:
		return Macro_retrive(index+1,data,macro_retrive,0)

def checkLabel_Instruction(line):
	line=line[1].split(" ")
	if line[0] in instructions or ":" in line[0]:
		return True
	else:	return False

def checkLabel(line):
	if ":" in line[1] or "jmp" in line[1] or "jl" in line[1] or "je" in line[1]:
		return True
	else:	return False
def rename_Label(line,key):
	lable=line[1]
	if "%" in lable and ":" in lable:
		lable=lable.strip()
		lable=lable.replace(":","")
		lable=lable+key+":"
		line[1]=lable
		return line
	else:
		lable=lable.strip()+key
		line[1]=lable
		return line

def create_Key(line,line_no):
	line=line.split(" ")
	if len(line)==1:
		print("Instruction expected. Error line no-",line_no)
		sys.exit()
	line[1]=line[1].split(",")
	return line[0]+"@"+str(len(line[1])),line[1]


def Macro_Expansion_recur(macro_retrive,expand_data,skip,macro_file,index,start,end,key):
	if index+start>end:
		return expand_data,macro_retrive
	elif "%macro" in macro_file[index+start][1]:
		return Macro_Expansion_recur(macro_retrive,expand_data,skip+1,macro_file,index+1,start,end,key)
	elif "%endmacro" in macro_file[index+start]:
		return Macro_Expansion_recur(macro_retrive,expand_data,skip-1,macro_file,index+1,start,end,key)	
	elif checkLabel_Instruction(macro_file[index+start])==True and skip==0:
		if checkLabel(macro_file[index+start])==True and skip==0:
			line=rename_Label(macro_file[index+start],key)
			expand_data.append(line)
			return Macro_Expansion_recur(macro_retrive,expand_data,skip,macro_file,index+1,start,end,key)
		elif skip==0:
			line=macro_file[index+start]
			if "%" in macro_file[index+start][1]:
				line=replace_Parameter(macro_file[index+start],macro_retrive["param"])
			#print("Line",line)
			expand_data.append(line)
			return Macro_Expansion_recur(macro_retrive,expand_data,skip,macro_file,index+1,start,end,key)
	elif len(macro_file[start+index][1])>0 and skip==0:#check macro call
		temp_key,param=create_Key(macro_file[index+start][1],macro_file[index+start][0])
		if Checker_key_available(temp_key,macro_retrive)!="Error":#recursion for macro call
			macro_retrive[temp_key]["param"]=param
			expand_data,macro_retrive[temp_key]=Macro_Expansion_recur(macro_retrive[temp_key],expand_data,0,macro_file,0,macro_retrive[temp_key]["start"],macro_retrive[temp_key]["end"],temp_key)
			return Macro_Expansion_recur(macro_retrive,expand_data,0,macro_file,index+1,start,end,key)
		else:
			print("Here Instruction Expected. line no-",macro_file[start+index][0])
			sys.exit()
	else:
		return Macro_Expansion_recur(macro_retrive,expand_data,skip,macro_file,index+1,start,end,key)
			
#Macro Expansion by call by macro
def Macro_Expansion(macro_retrived,original_file,filename,macro_file):
	expand_data,flag,index=[],0,0
	for line in original_file:
		if flag==1:
			if len(line[1])>0 and checkLabel_Instruction(line)==False:
				key,param=create_Key(line[1],line[0])
				#print(key,param)
				if Checker_key_available(key,macro_retrived)!="Error":
					macro_retrived[key]["param"]=param
					expand_data,macro_retrive=Macro_Expansion_recur(macro_retrived[key],expand_data,0,[""]+macro_file,0,macro_retrived[key]["start"],macro_retrived[key]["end"],key)#0 for skip-0 unskip-1
				else:
					print("Inctruction Expected. line no-",line[0])
					sys.exit()
			else:
				expand_data.append(line)
		else:
			expand_data.append(line)
		
		if "global main" in line[1]:
			flag=1
		index+=1
	return expand_data
#macro expansion write
def write_New_Data_newfile(filename,expand_data):
	fp=open(filename,"w+")
	for line in expand_data:
		fp.write(line[1]+"\n")
#start Function to retrive and expand macro //called by assembler file function
def Expand_macro(newfilename,oldfilename):
	flag,temp=0,[]
	for k,v in sorted(Macro_data.items()):
		if "%macro" in v:
			flag=1 #For macro contains flag
		temp.append([k,v])
	if flag==0:
		return False
	original_file=[]
	
	for k,v in sorted(Original_file.items()):
		original_file.append([k,v["line"]])
	macro_retrive,index=Macro_retrive(0,temp,macro_def,0)
	#print("Macro retrived",macro_retrive)
	expand_data=Macro_Expansion(macro_retrive,original_file,newfilename,temp)

	#print("Expanded Data",expand_data)
	write_New_Data_newfile(newfilename,expand_data)
	return True
