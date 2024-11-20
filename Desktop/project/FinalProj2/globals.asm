.data
    board:          .word 0:16        # 4x4 board
    revealed:       .word 0:16        # Revealed card tracking
    firstChoice:    .word -1          # Index of first choice
    secondChoice:   .word -1          # Index of second choice
    matches:        .word 8           # Number of remaining pairs
    startTime:      .word 0           # Start time in milliseconds

.text
    # initBoard: Initializes the board with values and resets revealed and choices
    initBoard:
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

        la $t0, revealed
        li $t1, 0
    clearLoop:
        sw $zero, ($t0)
        addi $t0, $t0, 4
        addi $t1, $t1, 1
        blt $t1, 16, clearLoop

        li $t0, -1
        sw $t0, firstChoice
        sw $t0, secondChoice
        li $t0, 8
        sw $t0, matches
        jr $ra

    # isRevealed: Checks if a card is revealed
    isRevealed:
        la $t0, revealed
        sll $t1, $a0, 2
        add $t0, $t0, $t1
        lw $v0, ($t0)
        jr $ra

    # revealCard: Reveals a card
    revealCard:
        la $t0, revealed
        sll $t1, $a0, 2
        add $t0, $t0, $t1
        li $t2, 1
        sw $t2, ($t0)
        jr $ra

    # hideCard: Hides a card
    hideCard:
        la $t0, revealed
        sll $t1, $a0, 2
        add $t0, $t0, $t1
        sw $zero, ($t0)
        jr $ra

    # getCardValue: Gets the value of a card
    getCardValue:
        la $t0, board
        sll $t1, $a0, 2
        add $t0, $t0, $t1
        lw $v0, ($t0)
        jr $ra

    # resetChoices: Resets first and second choices
    resetChoices:
        li $t0, -1
        sw $t0, firstChoice
        sw $t0, secondChoice
        jr $ra

    # displayGame: Displays the current game state
    displayGame:
        # ... (implementation in display.asm)

    # displayStatus: Displays the current game status
    displayStatus:
        # ... (implementation in display.asm)

    # displayWin: Displays the win message
    displayWin:
        # ... (implementation in display.asm)

    # processMove: Processes a player move
    processMove:
        # ... (implementation in game_logic.asm)

    # checkMatch: Checks if two cards match
    checkMatch:
        # ... (implementation in game_logic.asm)

    # isGameWon: Checks if the game is won
    isGameWon:
        # ... (implementation in game_logic.asm)

    # initGame: Initializes the game
    initGame:
        jal initBoard
        jal initTimer
        jr $ra

    # initTimer: Initializes the timer
    initTimer:
        li $v0, 30
        syscall
        sw $a0, startTime
        jr $ra

    # updateTimer: Updates the timer
    updateTimer:
        li $v0, 30
        syscall
        lw $t0, startTime
        sub $v0, $a0, $t0
        jr $ra

    # displayTime: Displays the elapsed time
    displayTime:
        # ... (implementation in timer.asm)