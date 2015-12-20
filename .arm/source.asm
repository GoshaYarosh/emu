	mov r1, 5
	mov r2, 0
	mov r3, 25

cycle:
	add r2, r2, r1
	cmp r2, r3
	bhi cycle