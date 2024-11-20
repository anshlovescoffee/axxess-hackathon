# main.asm - Main program entry point
.data
    menuPrompt:     .asciiz "\n1. Make a move\n2. Start new game\n3. Exit\nChoice: "
    errMsg:         .asciiz "\nInvalid choice. Please try again.\n"

.text
.include "globals.asm"

main:
    # Initialize game
    jal initGame
    
gameLoop:
    # Display current game state
    jal displayGame
    
    # Show menu and get choice
    li $v0, 4
    la $a0, menuPrompt
    syscall
    
    li $v0, 5
    syscall
    move $t0, $v0
    
    # Menu handling
    beq $t0, 1, handleMove
    beq $t0, 2, handleNewGame
    beq $t0, 3, handleExit
    
    # Invalid choice
    li $v0, 4
    la $a0, errMsg
    syscall
    j gameLoop

handleMove:
    jal processMove
    j gameLoop

handleNewGame:
    jal initGame
    j gameLoop
    
handleExit:
    li $v0, 10
    syscall