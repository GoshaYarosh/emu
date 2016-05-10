	mov r1, 1
	mov r2, 1
	mov r7, 5

cycle:
	add r3, r1, r2
	mov r1, r2
	mov r2, r3

	mov r4, 1
	sub r7, r7, r4

	mov r4, 0
	cmp r4, r7
	bhi cycle
