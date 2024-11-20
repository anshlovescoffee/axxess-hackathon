# game_logic.asm - Game mechanics and rules
.data
    inputPrompt:    .asciiz "Enter position (1-16): "
    invalidMsg:     .asciiz "Invalid position. Try again.\n"
    revealedMsg:    .asciiz "Card already revealed. Try again.\n"

.text
.include "globals.asm"

initBoard:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, ($sp)

    # Initialize board with values
    la $t0, board
    li $t1, 1
    li $t2, 1
initLoop:
    mul $t3, $t1, $t2
    sw $t3, ($t0)
    addi $t0, $t0, 4
    addi $t1, $t1, 1
    blt $t1, 5, initContinue
    li $t1, 1
    addi $t2, $t2, 1
initContinue:
    blt $t2, 5, initLoop

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
initGame:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, ($sp)
    
    # Initialize board and timer
    jal initBoard
    jal initTimer
    
    # Restore return address
    lw $ra, ($sp)
    addi $sp, $sp, 4
    jr $ra

processMove:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, ($sp)
    
getInput:
    # Get card position
    li $v0, 4
    la $a0, inputPrompt
    syscall
    
    li $v0, 5
    syscall
    addi $t0, $v0, -1    # Convert to 0-based index
    
    # Validate input
    bltz $t0, invalidInput
    bge $t0, 16, invalidInput
    
    # Check if already revealed
    move $a0, $t0
    jal isRevealed
    bnez $v0, revealedCard
    
    # Valid move - reveal card
    move $a0, $t0
    jal revealCard
    
    # Check if this is first or second card
    lw $t1, firstChoice
    bgez $t1, secondChoice
    
    # First choice
    sw $t0, firstChoice
    j moveEnd
    
secondChoice:
    # Store second choice
    sw $t0, secondChoice
    
    # Display board to show both cards
    jal displayGame
    
    # Check for match
    jal checkMatch
    
    # Reset choices
    jal resetChoices
    
    j moveEnd
    
invalidInput:
    li $v0, 4
    la $a0, invalidMsg
    syscall
    j getInput
    
revealedCard:
    li $v0, 4
    la $a0, revealedMsg
    syscall
    j getInput
    
moveEnd:
    # Check for win
    jal isGameWon
    
    # Restore return address
    lw $ra, ($sp)
    addi $sp, $sp, 4
    jr $ra

checkMatch:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, ($sp)
    
    # Get values of both cards
    lw $a0, firstChoice
    jal getCardValue
    move $t0, $v0
    
    lw $a0, secondChoice
    jal getCardValue
    
    # Compare values
    beq $t0, $v0, matchFound
    
    # No match - delay then hide cards
    li $v0, 32
    li $a0, 1000        # 1 second delay
    syscall
    
    lw $a0, firstChoice
    jal hideCard
    lw $a0, secondChoice
    jal hideCard
    j matchEnd
    
matchFound:
    # Decrement remaining matches
    lw $t0, matches
    addi $t0, $t0, -1
    sw $t0, matches
    
matchEnd:
    # Restore return address
    lw $ra, ($sp)
    addi $sp, $sp, 4
    jr $ra

isGameWon:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, ($sp)
    
    # Check if matches is 0
    lw $t0, matches
    bnez $t0, notWon
    
    # Game is won - display win message
    jal displayWin
    
    # Delay before returning
    li $v0, 32
    li $a0, 3000        # 3 second delay
    syscall
    
notWon:
    # Restore return address
    lw $ra, ($sp)
    addi $sp, $sp, 4
    jr $ra