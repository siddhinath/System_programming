Name - 		Siddhinath Kharade
Roll No-	16220
Program Version-	3.0

Updated Version-
Date-	14-11-2017
	What is update.

		1.	Header in lst file it will print if option "-H" provide command line after filename.
			EXAMPLE-	python3 Assembler.py newMacro.asm -H		#print header of lst
		2.  makefile add
			With dependency option solve commands
			examples is in mymake.txt

	How to Run-
		1.	python3 makefile.py mymake.txt 
		2.  python3 makefile.py mymake.txt 1 OR
		3.  python3 makefile.py mymake.txt 2 OR
	etc

Program Run-
			If "lst" Generate-
								python3 Assembler.py input_file.asm
			If macro expansion-
								python3 Assembler.py input_file.asm -E 		OR
								python3 Assembler.py input_file.asm -e
			OUTPUT-
					a.lst

Updated version-
	Macro Expansion
				-Pass zero complete done
				-Nested macro also expansion
				-Lable rename if "%%lable-name" gives
				-Valid error show 
				
Already Done-
	Up to "a.lst" file complete
	
	With instructions-
						mov,add,sub,lodsb,stosb,std,cld.
		
	Validations-
				1.Symbol redeclaration Error show
				2.Syntax Error
				3.Undefined symbol Error

Tips-
	1. Validation types inherited form nasm assembler
	2. Opcodes inherited by INTEL MANUAL
	3. Macro Expansion Done using DICTIONARY data structure with nested

	
Program Details-
	Assembler.py
			Main file to create lst file
	newAssem_Data_Struct.py
			Contains all data structure 
	Opcode_table1.py
			Get Opcodes of every instruction
	Macro_Expansion.py
			Macro expansion done in this file

Thank You
