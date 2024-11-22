.data
invalid_msg:    .asciiz "\nInvalid selection. Try again.\n"
.text
.globl validate_selection
.globl check_match
.globl match_found
.globl no_match
validate_selection:
    # Check if position is valid (1-16 input, 0-15 internal)
    bltz $a0, invalid_sel
    bge $a0, 16, invalid_sel
    # Check if already matched (silent ignore)
    la $t0, matched_pairs
    add $t0, $t0, $a0
    lb $t1, ($t0)
    bnez $t1, card_matched
    li $v0, 1          # Valid selection
    jr $ra
invalid_sel:
    li $v0, 4
    la $a0, invalid_msg
    syscall
    li $v0, 0
    jr $ra
card_matched:
    li $v0, 0          # Invalid selection (already matched)
    jr $ra
check_match:
    # $a0 = first position, $a1 = second position
    sll $t0, $a0, 2    # Multiply by 4 for word alignment
    sll $t1, $a1, 2
    la $t2, board
    add $t2, $t2, $t0
    lw $t3, ($t2)      # First card value
    la $t2, board
    add $t2, $t2, $t1
    lw $t4, ($t2)      # Second card value
    # One must be equation (0-7) and other answer (8-15)
    li $t0, 8
    blt $t3, $t0, first_is_eq
    j first_is_ans
first_is_eq:
    blt $t4, $t0, no_match    # Both equations
    addi $t4, $t4, -8         # Convert answer to equation index
    beq $t3, $t4, match_found
    j no_match
first_is_ans:
    bge $t4, $t0, no_match    # Both answers
    addi $t3, $t3, -8         # Convert answer to equation index
    beq $t3, $t4, match_found
    j no_match
no_match:
    li $v0, 0
    jr $ra
match_found:
    li $v0, 1
    jr $ra
