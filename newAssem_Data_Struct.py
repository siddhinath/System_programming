from Opcode_table1 import *
from Header_File import *

#All Data Structures Defined here
symbol_table={}
#{"line_no":line[0],"value":"","name":sym,"size":0,"status":"U","section":".text","convert_value":"","type":"global","line_address":""}

literal_table={}	# key as line number Format-"line_no":{"line_no":0,"literal":"","type":"","bits":0,"converted":,"nopadzero":}

registers={"al":8,"bl":8,"cl":8,"dl":8,"ax":16,"bx":16,"cx":16,"dx":16,"eax":32,"ebx":32,"ecx":32,"edx":32,"esp":32,"ebp":32,"esi":32,"edi":32}

address_table={}#key line number ans address with instruction and converted values and opcodes #final output here available
#line_no={"opcodes":,"size":,"line_no"}
global Original_file
Original_file={}#key line no and line

global File_data
File_data={".data":[],".bss":[],".text":[]} #Data keys are three section .data .bss .text 

sym_finder=["loop","main","main:","jmp","jl","je",":","jz","dw","dq","extern"]

mod_bit_register_opcodes=Mod_bit_registers_code()	#Get register mod byte and code 000 001 010 100 etc

instructions=["mov","add","repnz","xor","std","lodsb","cld","stosb","loop","jmp","sub","mul","div","cmp","jl","jq","je"]

#Macro Data Structure 
macro_def={}#{"mdt:{"unique_macro_name":{"start":,"end":},"macr_name2":{"start":,"end"},"mdt":{//nested macro//}}
Macro_data={}

def make_Empty():
	global File_data
	File_data={".data":[],".bss":[],".text":[]} #Data keys are three section .data .bss .text 

