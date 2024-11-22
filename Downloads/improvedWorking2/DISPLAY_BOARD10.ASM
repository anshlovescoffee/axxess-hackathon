#DISPLAY_BOARD10.ASM
.data
    star:           .asciiz "*"
    space:          .asciiz " "
    newline:        .asciiz "\n"
    row_border:     .asciiz "+-----+-----+-----+-----+\n"
    cell_border:    .asciiz "|"
    remaining_msg:  .asciiz "\nYou have "
    cards_msg:      .asciiz " cards remaining!\n"
    clear_screen:   .asciiz "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                             "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
.text
.globl display_board
.globl clear_and_display
clear_and_display:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, 0($sp)
    # Clear screen with newlines
    li $v0, 4
    la $a0, clear_screen
    syscall
    # Display board
    jal display_board
    # Restore and return
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra
display_board:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, 0($sp)
    # Print initial border
    li $v0, 4
    la $a0, row_border
    syscall
    li $t0, 0          # Row counter
    li $t1, 0          # Position counter
row_loop:
    # Print left border
    li $v0, 4
    la $a0, cell_border
    syscall
    li $t2, 0          # Column counter
col_loop:
    # Print space padding
    li $v0, 4
    la $a0, space
    syscall
    # Check if card is revealed or matched
    la $t3, shown_board
    add $t3, $t3, $t1
    lb $t4, ($t3)
    la $t3, matched_pairs
    add $t3, $t3, $t1
    lb $t5, ($t3)
    or $t4, $t4, $t5   # Show if either shown or matched
    beqz $t4, print_hidden
    # Print revealed card
    la $t3, board
    sll $t6, $t1, 2    # Multiply by 4 for word alignment
    add $t3, $t3, $t6
    lw $t4, ($t3)
    li $t6, 8
    bge $t4, $t6, print_number
    # Print equation
    la $t6, equations
    mul $t7, $t4, 4    # Each equation is 4 chars
    add $t6, $t6, $t7
    li $v0, 4
    move $a0, $t6
    syscall
    j print_cell_end
print_number:
    # Print answer number
    addi $t4, $t4, -8  # Convert to index
    sll $t6, $t4, 2
    la $t7, answers
    add $t7, $t7, $t6
    lw $a0, ($t7)
    li $v0, 1
    syscall
    # Print space after number for alignment
    li $v0, 4
    la $a0, space
    syscall
    j print_cell_end
print_hidden:
    # Print hidden symbol with padding
    li $v0, 4
    la $a0, star
    syscall
    # Print spaces for alignment
    li $v0, 4
    la $a0, space
    syscall
    la $a0, space
    syscall
print_cell_end:
    # Print space padding
    li $v0, 4
    la $a0, space
    syscall
    # Print cell border
    li $v0, 4
    la $a0, cell_border
    syscall
    addi $t1, $t1, 1   # Next position
    addi $t2, $t2, 1   # Next column
    blt $t2, 4, col_loop
    # Print newline
    li $v0, 4
    la $a0, newline
    syscall
    # Print row border
    li $v0, 4
    la $a0, row_border
    syscall
    addi $t0, $t0, 1   # Next row
    blt $t0, 4, row_loop
    # Count and print remaining cards
    li $t0, 0          # Counter
    li $t1, 0          # Matched count
    li $t2, 16         # Total cards
count_remaining:
    beq $t0, $t2, print_count
    la $t3, matched_pairs
    add $t3, $t3, $t0
    lb $t4, ($t3)
    add $t1, $t1, $t4
    addi $t0, $t0, 1
    j count_remaining
print_count:
    li $v0, 4
    la $a0, remaining_msg
    syscall
    li $t2, 16
    sub $t1, $t2, $t1
    li $v0, 1
    move $a0, $t1
    syscall
    li $v0, 4
    la $a0, cards_msg
    syscall
    # Restore return address and return
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra