section .data
str1 db "%d",0
section .text
extern printf
global main
main:
xor ecx,ecx
mov eax,11
mov ebx,22
add eax,ebx
sub ecx,edx
mul esi,edi
%%lpxyz@2:
add eax,ebx
sub edx,ecx
jmp %%lpxyz@2
sub eax,ebx
std
lodsb

