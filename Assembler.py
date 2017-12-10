import sys
from Opcode_table1 import *
from newAssem_Data_Struct import *
from MacroExpansion import *
class Process_file:
	def Process_line(self,data,section):
		if len(data)==0:
			return ""
		if section==1:
			data=data.split(" ")
			data=[data[0],data[1],"".join(data[2:]).split(",")]
		elif section==2 or section==3:
			data=data.split(" ")
			if len(data)>1:
				data[-1]=data[-1].split(",")
		return data

	def read_Input_File(self,filename):
		f=open(filename,"r")
		Data=f.read().split("\n")
		Data=list(map((lambda v: v.replace("\t","")),Data))
		line_no,section,key=0,0,""
		for data in Data:
			line_no+=1
			if ".data" in data:
				section,key=1,".data"
				Original_file[line_no]={"line":data}				
			elif ".bss" in data:
				section,key=2,".bss"
				Original_file[line_no]={"line":data}
			elif ".text" in data:
				Original_file[line_no]={"line":data}
				section,key=3,".text"
			elif key!="":
				line=[line_no]+[self.Process_line(data,section)]
				File_data[key].append(line)
				Original_file[line_no]={"line":data}
			else:
				Macro_data[line_no]=data
		#After read data from .asm file it will ormatted in File_data dict
		
class Sym_tab:
	def Convert_value(self,value,type_):
		#print(value)
		if type_=="dd":
			value=list(map((lambda v: (hex(int(v)).rstrip("L").lstrip("0x") or "0") ),value))
			value=''.join(list(map((lambda v: ''.join([str(v).upper()]+["0" for i in range(8-len(v))])),value)))
			#print(value)
			return value					
		elif type_=="db":
			value[0]=list(value[0])
			value[0]=''.join(list(map((lambda v: (hex(ord(v)).rstrip("L").lstrip("0x") or "0").upper() ),value[0])))
			temp=''.join(list(map((lambda v: (hex(int(v)).rstrip("L").lstrip("0x") or "0").upper() ),value[1:])))
			value=str(value[0])+str(temp)
			return value
		elif type_=="resd" or type_=="resb":
			return (hex(int(value[0])).rstrip("L").lstrip("0x") or "0").upper()

	def Calculate_size(self,value,type_):
		if type_=="dd":
			return len(value)*4
		elif type_=="db":
			value[0]=value[0].lstrip("\"").rstrip("\"")
			return len(value[0])+len(value[1:])
		elif type_=="resd":
			return int(value[0])*4
		elif type_=="resb":
			return int(value[0])

	def Find_symbols(self,Data_symbols,section):
		Address_line_by_line=0
		for symbol in Data_symbols:
			if len(symbol[1])>1:
				if Checker_key_available(symbol[1][0],symbol_table)!="Error":
					print("Symbol redeclaretion."+str(symbol[0]),symbol_table,symbol[1][0])
					sys.exit()
				line_no=symbol[0]
				name=symbol[1][0]
				type_=symbol[1][1]
				value=symbol[1][2]
				if type_!="equ":
					size=self.Calculate_size(value,type_)
					if type_=="resd":
						value[0]=str(int(value[0])*4)
						convert_value=self.Convert_value(value,type_)
					else:
						convert_value=self.Convert_value(value,type_)
					address=hex(Address_line_by_line).rstrip("L").lstrip("0x") or "0"
					address="".join(["0" for i in range(8-len(address))]+[str(address).upper()])
					Address_line_by_line+=size
				symbol_table[name]={"line_no":symbol[0],"value":value,"name":symbol[1][0],"size":size,"status":"D","section":section,"convert_value":convert_value,"type":symbol[1][1],"line_address":address}
				#print(symbol_table[name])
#Check symbol in operands of instructions
#return symbol name and size of that symbol
	def split_Dword_operand(self,operand):
		st=operand.index("[")
		end=operand[st:].index("]")
		return operand[st+1:st+end]
		
	def Defined_symbols(self,operand):
		if len(operand)>=1:
			if "dword" in str(operand[1]):
				op1=self.split_Dword_operand(operand[1])
				if Checker_key_available(op1,registers)=="Error":
					return op1
				else:
					return ""
			elif "dword" in str(operand[0]):
				op1=self.split_Dword_operand(operand[0])
				if Checker_key_available(op1,registers)=="Error":
					return op1
				else:
					return ""
			elif Checker_key_available(operand[0],registers)=="Error":
				return operand[0]
			elif Checker_key_available(operand[1],registers)=="Error":
				return operand[1]
			else:
				return ""
		else:
			return ""

#Disc-	parse whole line check in line symbol present or not 
	def isSymbol_Present(self,symbols):
		if len(symbols)>0:
			for symbol_checker in sym_finder:
				if symbols[0]==symbol_checker:
					return True,symbol_checker
				elif len(symbols[1])>=1 and symbols[1][0]==symbol_checker:
					return True,symbol_checker
				elif len(symbols[1])==2 and symbols[1][1][0]==symbol_checker:
					return True,symbol_checker
				elif ":" in str(symbols):
					return True,symbol_checker
		if len(symbols[1])==2 and len(symbols[1][1])==2:
			sym=self.Defined_symbols(symbols[1][1])
			if len(sym)>0:
				return True,sym
		return False,""
	def global_extern_symbols(self,line):
		if "global" in str(line):
			for sym in line[1][1]:
				symbol_table[sym]={"line_no":line[0],"value":"","name":sym,"size":'',"status":"U","section":".text","convert_value":"","type":"global","line_address":""}
		elif "extern" in str(line):
			for sym in line[1][1]:
				symbol_table[sym]={"line_no":line[0],"value":"","name":sym,"size":'',"status":"D","section":".text","convert_value":"","type":"extern","line_address":""}
	#check symbol as literal or not
	#o/p- bool true or false and type in that literal and bits
	def Check_literal(self,symbol):
		bool_,bits,converted=isConvertible(symbol)
		if bool_:
			return True,"int",bits,converted
		bool_,bits,converted=isChar(symbol)
		if bool_:
			return True,"char",bits,converted
		bool_,bits,converted=isHex(symbol)
		if bool_:
			return True,"hex",bits,converted
		else:
			return False,"",0,""

	def add_Literal_table(self,type_,bits,symbol,line_no,converted):
		temp=''.join(["0" for i in range(2-len(converted))]+[converted.upper()])
		converted=''.join([str(converted).upper()]+["0" for i in range(8-len(converted))])
		literal_table[line_no]={"line_no":line_no,"type":type_,"literal":symbol,"bits":bits,"converted":converted,"nopadzero":temp}

	def check_Symbol_Define(self,symbol):
		if Checker_key_available(symbol,symbol_table)=="Error":
			return False
		return True # check symbol defien or not

#I/P-	Text section data only
#Disc-	Collect all symbols from text section and check they defines in data sect or not if define "D" if not then "U" at last show "U" to error
#O/P-	Find all symbols and write in symbol table "symbol_table" Data struct
	def Find_symbols_text_section(self,Data_symbols):
		for symbols in Data_symbols:
			if len(symbols)>0:
				bool_,symbol=self.isSymbol_Present(symbols)#Add symbol Details in table and also add address of that symbols
				if bool_:
					#Here parse symbols check present of not in symbol table and if not "U"
					if "global" in str(symbols) or "global" in str(symbols):
						self.global_extern_symbols(symbols)
					elif len(symbols[1])==1:#label ete xyz or pqr:
						if self.check_Symbol_Define(symbols[1][0]):
							print(" Error. Symbol redefine. line no",symbols[0])
							sys.exit()
						symbol_table[symbols[1][0]]={"line_no":symbols[0],"value":"","name":symbols[1][0],"size":'',"status":"D","section":".text","convert_value":"","type":"label","line_address":""}
					elif len(symbols[1][1])==2:#means two parameter instruction
						#Check symbol Literal or not
						bool_,type_,bits,converted=self.Check_literal(symbol)
						if bool_:
							#Add literal into literal_table function call
							self.add_Literal_table(type_,bits,symbol,symbols[0],converted)
						else:
							bool_=self.check_Symbol_Define(symbol)
							if bool_:
								pass#Define and fetch symbol here
							else:
								print("Error symbol not define.Line no-",symbols[0])

	def Collect_symbols(self):
		Data_symbols=File_data[".data"]
		self.Find_symbols(Data_symbols,".data")
		Data_symbols=File_data[".bss"]
		self.Find_symbols(Data_symbols,".bss")
		Data_symbols=File_data[".text"]
		self.Find_symbols_text_section(Data_symbols)
		
class Opcode_table:
	#Find the oprand type line r,imm,m,other 
	def find_operand_type(self,operand,sym_tab_obj,line_no):
		if Checker_key_available(operand,registers)!="Error":
			return "r"+str(registers[operand]),operand
		#if Check it is literal or not
		elif Checker_key_available(line_no,literal_table)!="Error":
			return "imm"+str(literal_table[line_no]["bits"]),operand
		elif "dword" in operand:
			op1=sym_tab_obj.split_Dword_operand(operand)

			if Checker_key_available(str(op1),registers)!="Error":
				return "r"+str(registers[op1]),op1
			elif Checker_key_available(op1,symbol_table)!="Error":
				#print(symbol["type"])
				return "m32",op1
			else:
				print("Error invalid instruction, line no-",line_no)
				sys.exit()
		elif Checker_key_available(operand,symbol_table)!="Error":
			return "m32",operand
		else:
			print("Operand field not define yes sorry. Contact owner.")
			sys.exit()

	def store_Address_table(self,concat,size,text_inst):
		address_table[text_inst[0]]={"opcodes":concat,"size":size,"line_no":text_inst[0]}

	def get_Symbol_Address(self,symbol,sym_tab_obj):
		if sym_tab_obj.check_Symbol_Define(symbol):
			return "["+symbol_table[symbol]["line_address"]+"]"
		else:
			print("Error Symbol not define ",symbol)

	def fetch_Literal_value(self,ln,val):
		return literal_table[ln][val]

	def find_operands_types(self,operands,sym_tab_obj,line_no):
		op1,original_op1=self.find_operand_type(operands[0],sym_tab_obj,line_no)#print(operands)
		op2,original_op2=self.find_operand_type(operands[1],sym_tab_obj,line_no)#print(operands)
		return op1,op2,original_op1,original_op2

	def process_mov_inst(self,text_inst,sym_tab_obj,size=0,concat=""):
		op1,op2,original_op1,original_op2=self.find_operands_types(text_inst[1][1],sym_tab_obj,text_inst[0])#third para for line number
		if op1=="r32" and op2=="imm8":
			op2="imm32"
		opcode_mnumonic_opcode_table=get_opcode_instruction("mov",op1+op2)
		if "r" in op1 and "r" in op2:
			registers_mnumonic_registersmod_table=Find_reg_opcode(original_op1,original_op2,mod_bit_register_opcodes)
			size,concat=2,opcode_mnumonic_opcode_table+registers_mnumonic_registersmod_table
		elif "r" in op1 and "imm" in op2:
			#registers_mnumonic_registersmod_table=Find_reg_opcode(original_op1,"eax",mod_bit_register_opcodes)
			literal_in_hex=self.fetch_Literal_value(text_inst[0],"converted")
			size,concat=2,opcode_mnumonic_opcode_table+literal_in_hex
		elif "r" in op1 and "m" in op2:
			symbol_address=self.get_Symbol_Address(original_op2,sym_tab_obj)
			size,concat=2,opcode_mnumonic_opcode_table+symbol_address
		else:
			print("Invalid Combination",text_inst[0])
		self.store_Address_table(concat,size,text_inst)

	def process_add_inst(self,text_inst,sym_tab_obj,size=0,concat=""):
		op1,op2,original_op1,original_op2=self.find_operands_types(text_inst[1][1],sym_tab_obj,text_inst[0])#third para for line number
		opcode_mnumonic_opcode_table=get_opcode_instruction("add",op1+op2)
		if "r" in op1 and "imm" in op2:
			registers_mnumonic_registersmod_table=Find_reg_opcode(original_op1,"eax",mod_bit_register_opcodes)
			literal_in_hex=self.fetch_Literal_value(text_inst[0],"nopadzero")
			size,concat=3,opcode_mnumonic_opcode_table+registers_mnumonic_registersmod_table+literal_in_hex
		elif "r" in op1 and "m" in op2:
			symbol_address=self.get_Symbol_Address(original_op2,sym_tab_obj)
			size,concat=2,opcode_mnumonic_opcode_table+symbol_address			
		elif "r" in op1 and "r" in op2:
			registers_mnumonic_registersmod_table=Find_reg_opcode(original_op1,original_op2,mod_bit_register_opcodes)
			size,concat=2,opcode_mnumonic_opcode_table+registers_mnumonic_registersmod_table
		self.store_Address_table(concat,size,text_inst)
	def process_xor_inst(self,text_inst,sym_tab_obj):
		op1,op2,original_op1,original_op2=self.find_operands_types(text_inst[1][1],sym_tab_obj,text_inst[0])#third para for line number
		opcode_mnumonic_opcode_table=get_opcode_instruction(text_inst[1][0],op1+op2)
		registers_mnumonic_registersmod_table=Find_reg_opcode(original_op1,original_op2,mod_bit_register_opcodes)

		size,concat=2,opcode_mnumonic_opcode_table+registers_mnumonic_registersmod_table
		self.store_Address_table(concat,size,text_inst)
		
	def process_single_inst(self,text_inst,sym_tab_obj):
		opcode_mnumonic_opcode_table=get_opcode_instruction(text_inst[1][0],text_inst[1][0]+text_inst[1][0])
		size,concat=1,opcode_mnumonic_opcode_table
		self.store_Address_table(concat,size,text_inst)
		
	def Process_instruction(self,sym_tab_obj):
		text_section_data=File_data[".text"]
		data_section_data=File_data[".data"]
		bss_section_data=File_data[".bss"]
		for text_inst in text_section_data:
			if len(text_inst[1])>0:
				if text_inst[1][0] in instructions:
					ins=text_inst[1][0]
					if text_inst[1][0]=="mov":
						self.process_mov_inst(text_inst,sym_tab_obj)
					elif text_inst[1][0]=="add":
						self.process_add_inst(text_inst,sym_tab_obj)
					elif text_inst[1][0]=="xor" or ins=="sub":
						self.process_xor_inst(text_inst,sym_tab_obj)
					elif ins=="repnz" or ins=="std" or ins=="cld" or ins=="stosb" or ins=="lodsb":
						self.process_single_inst(text_inst,sym_tab_obj)


class LST_file:
	def write_lst_contents(self,filename):
		fp=open(filename,"w+")
		size_address,opcodes,size,size_address_s=0,"",0,""
		fp.write("16220 create by siddhinath kharade\n")
		for k,v in sorted(Original_file.items()):
			size_address_s="".join(["0" for i in range(8-len(str(size_address)))]+[str(size_address).upper()])

			fp.write(str(k)+"\t")
			flag=0
			if Checker_key_available(k,address_table)!="Error":
				flag=1
				size,opcodes=address_table[k]["size"],address_table[k]["opcodes"]
				fp.write(size_address_s+"\t"+opcodes+"\t\t"+Original_file[k]["line"]+"\n")
				size_address+=size
			for kk,v in symbol_table.items():
				if str(v["line_no"])==str(k):
					flag=1
					size,conversion=symbol_table[kk]["size"],symbol_table[kk]["convert_value"]
					fp.write(symbol_table[kk]["line_address"]+"\t"+conversion+"\t\t"+Original_file[k]["line"]+"\n")
					break
			if flag==0:
				fp.write("\t\t\t"+Original_file[k]["line"]+"\n")

def Show_Header_lst():
	fp3=open("a.lst","r")
	firstline=fp3.readline()
	print(firstline)
	
def check_Macro_define():
	fp=open(sys.argv[1],"r")
	if "%endmacro" in fp.read():
		return True
	else:
		return False

def Start_point_second(limit):
	if(len(sys.argv)<2):
		print("Provide assembly file...")
		sys.exit()
	filename=sys.argv[1]
	obj_process=Process_file()
	flag=0
	if check_Macro_define():
		flag=1
	if flag==1:
		obj_process.read_Input_File(filename)
		flag=Expand_macro("macroexp@1@"+sys.argv[1],sys.argv[1])
		global File_data
		File_data={".data":[],".bss":[],".text":[]} #Data keys are three section .data .bss .text 
		global Original_file
		Original_file={}
		filename="macroexp@1@"+sys.argv[1]#new file name If macro present return TRUE else FALSE
		if(limit==1):
			Display_Macro_Expansion(filename)
			return 
		obj_process.read_Input_File(filename)
	

	obj_symbol=Sym_tab()
	obj_symbol.Collect_symbols()
	obj_opcode_table=Opcode_table()
	obj_opcode_table.Process_instruction(obj_symbol)
	lst_file=LST_file()
	lst_file.write_lst_contents("a.lst")
	if len(sys.argv)==3:
		if sys.argv[2]=="-H" or sys.argv[2]=="-h":
			Show_Header_lst()
	print("Check a.lst")


def main():
	if len(sys.argv)==1:
		print("Error. Please provide .asm file name to assembler.")
		sys.exit()
	if len(sys.argv)>2 and (sys.argv[2]=="-e" or sys.argv[2]=="-E"):
		Start_point_second(1)
	else:
		Start_point_second(0)#For -E Expansion 	show purpose	
main()
