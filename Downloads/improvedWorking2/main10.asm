.data
    .align 2
    board:          .word   0:16       # 16 cells for 4x4 board
    .align 2
    equations:      .asciiz "2×3","4×2","3×5","6×2","4×5","2×8","5×2","7×2"  # 8 unique equations
    .align 2
    answers:        .word   6, 8, 15, 12, 20, 16, 10, 14                     # 8 matching answers
    .align 2
    shown_board:    .byte   0:16       # 0 = hidden, 1 = shown
    .align 2
    matched_pairs:  .byte   0:16       # 0 = unmatched, 1 = matched
    .align 2
    sleep_time:     .word   1000       # 1 second delay (1000 milliseconds)

    # Game messages
    invalid_msg:    .asciiz "\nInvalid selection. Try again.\n"
    win_msg:        .asciiz "\nCongratulations! You've matched all pairs!\n"
    first_prompt:   .asciiz "\nSelect first card (1-16): "
    second_prompt:  .asciiz "\nSelect second card (1-16): "
    time_msg:       .asciiz "\nTime taken: "
    seconds_msg:    .asciiz " seconds\n"
    attempts_msg:   .asciiz "Attempts made: "

    # Make data accessible to other files
    .globl board
    .globl equations
    .globl answers
    .globl shown_board
    .globl matched_pairs

.text
.globl main

main:
    # Get start time (in milliseconds)
    li $v0, 30
    syscall
    move $t9, $a0       # Store lower 32 bits of start time
    
    # Initialize attempts counter
    li $t8, 0           # $t8 = attempt counter

    # Initialize stack pointer
    lui $sp, 0x1001
    ori $sp, $sp, 0x0000
    
    # Initialize the game
    jal init_board
    
    # Initialize matched cards and shown cards to 0
    li $t0, 0              # Counter
    li $t1, 16             # Total cards
init_arrays:
    la $t2, matched_pairs
    la $t3, shown_board
    add $t2, $t2, $t0
    add $t3, $t3, $t0
    sb $zero, ($t2)        # matched_pairs[i] = 0
    sb $zero, ($t3)        # shown_board[i] = 0
    addi $t0, $t0, 1
    bne $t0, $t1, init_arrays

game_loop:
    # Clear screen and display current board
    jal clear_and_display

get_first:
    # Show first prompt
    li $v0, 4
    la $a0, first_prompt
    syscall
    
    # Read selection (1-16)
    li $v0, 5
    syscall
    addi $s0, $v0, -1      # Convert to 0-based index
    
    # Validate selection
    bltz $s0, invalid_first
    bge $s0, 16, invalid_first
    
    # Check if already matched
    la $t0, matched_pairs
    add $t0, $t0, $s0
    lb $t1, ($t0)
    bnez $t1, get_first    # Silently ignore matched cards
    
    # Show first card
    la $t0, shown_board
    add $t0, $t0, $s0
    li $t1, 1
    sb $t1, ($t0)
    
    # Clear screen and show updated board
    jal clear_and_display

get_second:
    # Increment attempt counter
    addi $t8, $t8, 1    # Increment attempt counter

    # Show second prompt
    li $v0, 4
    la $a0, second_prompt
    syscall
    
    # Read selection (1-16)
    li $v0, 5
    syscall
    addi $s1, $v0, -1      # Convert to 0-based index
    
    # Validate selection
    bltz $s1, invalid_second
    bge $s1, 16, invalid_second
    beq $s1, $s0, same_card
    
    # Check if already matched
    la $t0, matched_pairs
    add $t0, $t0, $s1
    lb $t1, ($t0)
    bnez $t1, get_second   # Silently ignore matched cards
    
    # Show second card
    la $t0, shown_board
    add $t0, $t0, $s1
    li $t1, 1
    sb $t1, ($t0)
    
    # Clear screen and show both cards
    jal clear_and_display
    
    # Delay for 1 second to show cards
    li $v0, 32
    lw $a0, sleep_time
    syscall
    
    # Check for match
    la $t0, board
    sll $t1, $s0, 2       # Multiply index by 4 for word alignment
    sll $t2, $s1, 2
    add $t0, $t0, $t1
    lw $t3, ($t0)         # First card value
    la $t0, board
    add $t0, $t0, $t2
    lw $t4, ($t0)         # Second card value
    
    # Compare cards (one must be equation, one must be answer)
    li $t0, 8             # Dividing line between equations and answers
    blt $t3, $t0, check_first_eq
    j check_first_ans

check_first_eq:
    # First card is equation, second must be answer
    blt $t4, $t0, no_match_found
    addi $t4, $t4, -8     # Convert answer index to equation index
    beq $t3, $t4, match_found
    j no_match_found

check_first_ans:
    # First card is answer, second must be equation
    bge $t4, $t0, no_match_found
    addi $t3, $t3, -8     # Convert answer index to equation index
    beq $t3, $t4, match_found
    j no_match_found

invalid_first:
    li $v0, 4
    la $a0, invalid_msg
    syscall
    j get_first

invalid_second:
    li $v0, 4
    la $a0, invalid_msg
    syscall
    # Hide first card
    la $t0, shown_board
    add $t0, $t0, $s0
    sb $zero, ($t0)
    jal clear_and_display
    j get_first

same_card:
    li $v0, 4
    la $a0, invalid_msg
    syscall
    # Hide first card
    la $t0, shown_board
    add $t0, $t0, $s0
    sb $zero, ($t0)
    jal clear_and_display
    j get_first

match_found:
    # Mark both cards as matched
    la $t0, matched_pairs
    add $t0, $t0, $s0
    li $t1, 1
    sb $t1, ($t0)
    la $t0, matched_pairs
    add $t0, $t0, $s1
    sb $t1, ($t0)
    
    # Hide shown status
    la $t0, shown_board
    add $t0, $t0, $s0
    sb $zero, ($t0)
    la $t0, shown_board
    add $t0, $t0, $s1
    sb $zero, ($t0)
    
    # Check if game is complete
    jal check_win
    bnez $v0, game_won
    j game_loop

no_match_found:
    # Hide both cards
    la $t0, shown_board
    add $t0, $t0, $s0
    sb $zero, ($t0)
    la $t0, shown_board
    add $t0, $t0, $s1
    sb $zero, ($t0)
    j game_loop

check_win:
    li $t0, 0              # Counter
    li $t1, 0              # Matched count
    li $t2, 16             # Total cards
check_win_loop:
    beq $t0, $t2, check_win_done
    la $t3, matched_pairs
    add $t3, $t3, $t0
    lb $t4, ($t3)
    add $t1, $t1, $t4
    addi $t0, $t0, 1
    j check_win_loop

check_win_done:
    li $t0, 16
    seq $v0, $t1, $t0      # Return 1 if all matched
    jr $ra

game_won:
    # Get end time (in milliseconds)
    li $v0, 30
    syscall
    
    # Calculate elapsed time in milliseconds
    sub $t1, $a0, $t9    # $t1 = end time - start time
    
    # Convert to seconds (divide by 1000)
    li $t2, 1000
    div $t1, $t2
    mflo $t1            # $t1 now contains seconds

    # Display win message
    li $v0, 4
    la $a0, win_msg
    syscall

    # Display elapsed time
    li $v0, 4
    la $a0, time_msg
    syscall

    move $a0, $t1       # Time in seconds
    li $v0, 1
    syscall

    li $v0, 4
    la $a0, seconds_msg
    syscall

    # Display attempts made
    li $v0, 4
    la $a0, attempts_msg
    syscall

    move $a0, $t8       # Number of attempts
    li $v0, 1
    syscall
    
    # Print final newline
    li $v0, 11
    li $a0, 10        # ASCII code for newline
    syscall
    
    # Display final board state
    jal display_board
    
    # Exit program
    li $v0, 10
    syscall

init_board:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, 0($sp)
    
    # Initialize random seed
    li $v0, 30
    syscall
    move $a0, $v0
    li $v0, 40
    li $a1, 0
    syscall
    
    # First, place equations (0-7)
    li $t0, 0              # Counter
    li $t1, 8              # Number of equations

place_equations:
    beq $t0, $t1, place_answers
    
    # Generate random position
    li $v0, 42
    li $a1, 16
    syscall
    move $t2, $a0
    
    # Calculate word-aligned address
    sll $t3, $t2, 2
    la $t4, board
    add $t4, $t4, $t3
    
    # Check if position is taken
    lw $t5, ($t4)
    bnez $t5, place_equations
    
    # Place equation index
    sw $t0, ($t4)
    
    addi $t0, $t0, 1
    j place_equations

place_answers:
    li $t0, 0              # Counter

place_answers_loop:
    beq $t0, $t1, init_done
    
    # Generate random position
    li $v0, 42
    li $a1, 16
    syscall
    move $t2, $a0
    
    # Calculate word-aligned address
    sll $t3, $t2, 2
    la $t4, board
    add $t4, $t4, $t3
    
    # Check if position is taken
    lw $t5, ($t4)
    bnez $t5, place_answers_loop
    
    # Place answer (add 8 to distinguish from equations)
    addi $t6, $t0, 8
    sw $t6, ($t4)
    
    addi $t0, $t0, 1
    j place_answers_loop

init_done:
    # Restore return address and return
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra