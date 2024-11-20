# timer.asm - Time tracking and display
.data
    startTime:      .word 0           # Start time in milliseconds
    colonChar:      .asciiz ":"

.text
initTimer:
    # Get current time
    li $v0, 30
    syscall
    sw $a0, startTime
    jr $ra

updateTimer:
    # Get current time
    li $v0, 30
    syscall
    
    # Calculate elapsed time
    lw $t0, startTime
    sub $v0, $a0, $t0    # Return elapsed time in milliseconds
    jr $ra

displayTime:
    # Save return address
    addi $sp, $sp, -4
    sw $ra, ($sp)
    
    # Get elapsed time
    jal updateTimer
    
    # Convert to seconds
    li $t0, 1000
    div $v0, $t0
    mflo $t0            # Total seconds
    
    # Calculate minutes and seconds
    li $t1, 60
    div $t0, $t1
    mflo $t2            # Minutes
    mfhi $t3            # Seconds
    
    # Display minutes
    li $v0, 1
    move $a0, $t2
    syscall
    
    # Display colon
    li $v0, 4
    la $a0, colonChar
    syscall
    
    # Display seconds with leading zero if needed
    bge $t3, 10, skipLeadingZero
    
    li $v0, 11
    li $a0, 48          # ASCII for '0'
    syscall
    
skipLeadingZero:
    li $v0, 1
    move $a0, $t3
    syscall
    
    # Restore return address
    lw $ra, ($sp)
    addi $sp, $sp, 4
    jr $ra