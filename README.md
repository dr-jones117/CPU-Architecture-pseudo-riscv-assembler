# RISC-V -> IntelHEX Assembler
Converts RISC-V assembly into Intel HEX object files

https://en.wikipedia.org/wiki/Intel_HEX

- Labels are memory locations in HEX.
- Most RISC-V instructions have been implemented.

## Example Assembly
```
200: addi x10 x0 -1
     addi x10 x10 1
     addi x11 x0 2
     blt x10 x11 -8
     addi x10 x0 1
     addi x25 x0 2
     addi x26 x0 8
     mul x10 x10 x25
     bne x10 x26 -4
     beq x10 x26 4

228: addi x2 x0 -1
     addi x3 x0 -12
     bltu x2 x3 8
     addi x10 x0 12345
     bgeu x3 x2 8
     addi x11 x0 12345
     jal x2 20

254: addi x31 x0 -1
     addi x30 x0 -1
     addi x10 x0 1
     addi x5 x0 1
     addi x11 x0 3
     add x5 x5 x10
     bge x5 x11 8
     blt x5 x11 -8
     break
```
* Note: Will convert this to a object file.
