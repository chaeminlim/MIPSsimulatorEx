		.data

		.text
        .globl main
main:	addi $a0, $0, 6
		jal fibo
		add $t0, $v0, $0
		li $v0, 1
		move $a0, $t0
		syscall 
		j next
fibo:   add $sp, $sp, -12
		sw $ra, 8($sp)
		sw $s0, 4($sp)
		sw $a0, 0($sp)
		bgt $a0, 0, test
		add $v0, $0, 0
		j rtrn
test:	addi $t0, $0, 1  
		bne $t0, $a0, calc
		addi $v0, $0, 1
		j rtrn
calc:	addi $a0, $a0, -1
		jal fibo
		addi $s0, $v0, 0
		addi $a0, $a0, -1
		jal fibo
		add $v0, $v0, $s0
rtrn:	lw $a0, 0($sp)
		lw $s0, 4($sp)
		lw $ra, 8($sp)
		addi $sp, $sp, 12 
		jr $ra
next:	
		
		
		