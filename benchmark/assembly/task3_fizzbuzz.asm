section .data
    fizz db "Fizz", 10
    buzz db "Buzz", 10
    fizzbuzz db "FizzBuzz", 10
    newline db 10

section .bss
    buffer resb 4

section .text
    global _start

_start:
    mov r12, 1

.loop:
    cmp r12, 101
    jge .done

    mov rax, r12
    xor rdx, rdx
    mov rcx, 15
    div rcx
    test rdx, rdx
    jz .print_fizzbuzz

    mov rax, r12
    xor rdx, rdx
    mov rcx, 3
    div rcx
    test rdx, rdx
    jz .print_fizz

    mov rax, r12
    xor rdx, rdx
    mov rcx, 5
    div rcx
    test rdx, rdx
    jz .print_buzz

    call print_number
    jmp .next

.print_fizzbuzz:
    mov rax, 1
    mov rdi, 1
    mov rsi, fizzbuzz
    mov rdx, 9
    syscall
    jmp .next

.print_fizz:
    mov rax, 1
    mov rdi, 1
    mov rsi, fizz
    mov rdx, 5
    syscall
    jmp .next

.print_buzz:
    mov rax, 1
    mov rdi, 1
    mov rsi, buzz
    mov rdx, 5
    syscall

.next:
    inc r12
    jmp .loop

.done:
    mov rax, 60
    xor rdi, rdi
    syscall

print_number:
    mov rax, r12
    mov rdi, buffer + 3
    mov byte [rdi], 10
    dec rdi
    mov rcx, 10

.convert:
    xor rdx, rdx
    div rcx
    add dl, '0'
    mov [rdi], dl
    dec rdi
    test rax, rax
    jnz .convert

    inc rdi
    mov rsi, rdi
    mov rdx, buffer + 4
    sub rdx, rdi
    mov rax, 1
    mov rdi, 1
    syscall
    ret
