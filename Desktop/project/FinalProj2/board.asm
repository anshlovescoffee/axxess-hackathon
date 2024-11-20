# board.asm - Board state management
.data
    board:          .word 0:16        # 4x4 board
    revealed:       .word 0:16        # Revealed card tracking
    firstChoice:    .word -1          # Index of first choice
    secondChoice:   .word -1          # Index of second choice
    matches:        .word 8           # Number of remaining pairs

.text
initBoard:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, ($sp)
    
    la $t0, board
    li $t1, 0            # Counter
    li $t2, 1            # First multiplier
    li $t3, 1            # Second multiplier
    
initLoop:
    mul $t4, $t2, $t3    # Calculate product
    sw $t4, ($t0)        # Store in board
    
    addi $t0, $t0, 4     # Next position
    addi $t1, $t1, 1     # Increment counter
    
    # Update multipliers
    addi $t3, $t3, 1
    blt $t3, 5, initContinue
    li $t3, 1
    addi $t2, $t2, 1
    
initContinue:
    blt $t1, 16, initLoop
    
    # Reset revealed array
    la $t0, revealed
    li $t1, 0
clearLoop:
    sw $zero, ($t0)
    addi $t0, $t0, 4
    addi $t1, $t1, 1
    blt $t1, 16, clearLoop
    
    # Reset choices and matches
    li $t0, -1
    sw $t0, firstChoice
    sw $t0, secondChoice
    li $t0, 8
    sw $t0, matches
    
    # Restore return address
    lw $ra, ($sp)
    addi $sp, $sp, 4
    jr $ra

isRevealed:
    la $t0, revealed
    sll $t1, $a0, 2
    add $t0, $t0, $t1
    lw $v0, ($t0)
    jr $ra

revealCard:
    la $t0, revealed
    sll $t1, $a0, 2
    add $t0, $t0, $t1
    li $t2, 1
    sw $t2, ($t0)
    jr $ra

hideCard:
    la $t0, revealed
    sll $t1, $a0, 2
    add $t0, $t0, $t1
    sw $zero, ($t0)
    jr $ra

getCardValue:
    la $t0, board
    sll $t1, $a0, 2
    add $t0, $t0, $t1
    lw $v0, ($t0)
    jr $ra

resetChoices:
    li $t0, -1
    sw $t0, firstChoice
    sw $t0, secondChoice
    jr $ra