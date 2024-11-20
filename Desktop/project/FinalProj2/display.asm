# display.asm - Display functionality
.data
    boardLine:      .asciiz "+----+----+----+----+\n"
    hiddenCard:     .asciiz "  ? "
    newline:        .asciiz "\n"
    space:          .asciiz " "
    remaining:      .asciiz "Pairs remaining: "
    timeLabel:      .asciiz "Time: "
    winMessage:     .asciiz "Well Done! You finished in "

.text
displayGame:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, ($sp)
    
    # Display status
    jal displayStatus
    
    # Display board header
    li $v0, 4
    la $a0, boardLine
    syscall
    
    li $t1, 0           # Row counter
    li $t2, 0           # Position counter
    
displayLoop:
    # Print vertical bar
    li $v0, 11
    li $a0, 124         # ASCII for |
    syscall
    
    # Check if card is revealed
    move $a0, $t2
    jal isRevealed
    beqz $v0, showHidden
    
    # Show card value
    move $a0, $t2
    jal getCardValue
    move $t3, $v0
    
    li $v0, 1
    move $a0, $t3
    syscall
    
    # Pad with spaces
    li $v0, 11
    li $a0, 32          # Space
    syscall
    bgt $t3, 9, skipExtra
    syscall             # Extra space for single digit
skipExtra:
    j continueDisplay
    
showHidden:
    li $v0, 4
    la $a0, hiddenCard
    syscall
    
continueDisplay:
    addi $t2, $t2, 1
    
    # Check if row is complete
    rem $t3, $t2, 4
    bnez $t3, displayLoop
    
    # End of row
    li $v0, 11
    li $a0, 124         # ASCII for |
    syscall
    li $v0, 4
    la $a0, newline
    syscall
    la $a0, boardLine
    syscall
    
    addi $t1, $t1, 1
    blt $t1, 4, displayLoop
    
    # Restore return address
    lw $ra, ($sp)
    addi $sp, $sp, 4
    jr $ra

displayStatus:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, ($sp)
    
    # Display remaining pairs
    li $v0, 4
    la $a0, remaining
    syscall
    
    li $v0, 1
    lw $a0, matches
    syscall
    
    # Display time
    li $v0, 4
    la $a0, space
    syscall
    la $a0, timeLabel
    syscall
    
    jal displayTime
    
    li $v0, 4
    la $a0, newline
    syscall
    
    # Restore return address
    lw $ra, ($sp)
    addi $sp, $sp, 4
    jr $ra

displayWin:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, ($sp)
    
    # Display win message with time
    li $v0, 4
    la $a0, winMessage
    syscall
    
    jal displayTime
    
    li $v0, 4
    la $a0, newline
    syscall
    
    # Restore return address
    lw $ra, ($sp)
    addi $sp, $sp, 4
    jr $ra