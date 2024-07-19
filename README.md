# Shellcoder.py

Write your shellcode in Assembly and execute it with one command!

This script helps automate the shellcode testing process. It takes an Assembly file with the shellcode (`shellcode.asm`), compiles it into machine code (NASM), generates a payload in C with that, and pastes it into the `loader.c` file. Finally, the prepared C file is compiled using MSVC. With this script you go from Assembly shellcode to executable file with one command!

## Usage

Shellcoder script most probably should be used on Windows because of the MSVC requirement.

1. Write your shellcode in `shellcode.asm`
2. Run `python shellcoder.py`
3. Execute output `.exe` file in `out/` directory!

> **IMPORTANT**: Indicate that you are using 64-bit mode at the beginning of the assembly file. Add `[bits 64]` to the `shellcode.asm`.

## External dependencies

- Python 3
- NASM (Netwide Assembler)
- Visual Studio 2022
