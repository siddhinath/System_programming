%macro xyz 2
	mov eax,%1
	mov ebx,%2
	add eax,ebx
	%macro sid 2
		sub ecx,edx
		%macro kharade 2
			add eax,ebx
			%macro nested 3
				mov ecx,edx
			%endmacro
			%macro nested 2
				sub esi,edi
				mov ecx,edx
			%endmacro
			sub ecx,edx
		%endmacro
		mul esi,edi
		%macro kharade 3
			mov esi,edi
		%endmacro
	%endmacro
	sid 1,2
	%%lp: 
		add eax,ebx
		sub edx,ecx
	jmp %%lp
	sub eax,ebx

%endmacro
%macro pqr 3
	mov eax,%1
	mov ebx,%2
	add eax,ebx
	add eax,ebx
	sub edx,ecx
	jmp %%lp
	sub eax,ebx
%endmacro
section .data
	str1 db "%d",0
section .text
	extern printf
	global main
main:
	xor ecx,ecx
	xyz 11,22
	std
	lodsb	
