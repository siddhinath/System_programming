import sys
import os

def isInteger(i):
	try:
		i=i.strip().split(" ")
		i=int(i[0])
		return True
	except Exception:
		return False

def checkTab_Present_Command(command):
	command=command.split("\t")
	#print(command)
	if command[0]=='':
		return True
	else:
		return False

#fun check syntax of make file
#i\p-make file data
#o\p-formatted data and status syntax correct or not
def checkSyntax_makefile(input_data):
	input_data=input_data.split("\n")
	#print(input_data)
	if len(input_data)<1:
		return "",False
	else:
#set commands as ans interative 
		command=[[] for i in range(10)]
		pos,depend=[],[]
		for i in input_data:
			if isInteger(i):
				pos=list(map(int,i.strip().split(" ")))
			else:
				if len(i)>1:
					if checkTab_Present_Command(i):
						if len(pos)>1:
							depend=pos
						i=i.split("\t")
						command[pos[0]].append(i[1])
					else:
						print("Error. makefile syntax error. please provide correct tab indent in makefile")
						sys.exit()

## DEPENDENCY SOLVER
		temp=[]
		for i in range(len(depend)-1,0,-1):
			#print(depend[i])
			temp.append(command[depend[i]][0])
		#print(temp)
		temp1=[]
		for i in command[depend[0]]:
			temp.append(i)
		command[depend[0]]=[]
		for i in temp:
			command[depend[0]].append(i)
		for i in temp1:
			command[depend[0]].append(i)
		return command,True

def execute_Commands(commands_data):
	#print("Execute Commands",commands_data)
	start_point=0
	if len(sys.argv)>=2:
		if isInteger(sys.argv[2]):
			start_point=int(sys.argv[2])
		else:
			print("Error. Commands line error you provide wrong integer which is not present in makefile")
	else:
		start_point=0 #default start point makefile
	for command in commands_data[start_point]:
		os.system(command)

def main():
#check makefile.txt present or not
	if len(sys.argv)<2:
		print("Error. makefile name not provided please provide filename as command line argument")
		sys.exit()
	filename=sys.argv[1]
	fp=open(sys.argv[1],"r")
	if fp==None:
		print("makefile.txt not present current directory")
	else:
#Check Syntax of file
		data=fp.read()
		commands_data,check_status=checkSyntax_makefile(data)
		if check_status==False:
			print("Error. Entered wrong syntax in makefile. Please correct it.")
		else:
#Go further execution
			execute_Commands(commands_data)

main()
