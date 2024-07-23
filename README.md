# Shellcoder.py 🐚⌨️

Write your shellcode in Assembly (NASM) and compile it on Windows x64 with one command!

This script helps automate the shellcode development and testing process. It takes your Assembly file with the payload (`shellcode.asm`) and generates a bunch of useful executable files (read below).

You don't have to repeat all these tedious activities anymore to make your shellcode executable! Keep your focus on shellcoding 🔥🐚🔥

## Installation

The following software must be installed on your system:

- [Python 3](https://www.python.org/downloads/)
- [NASM (Netwide Assembler)](https://www.nasm.us/)
- [Visual Studio 2022](https://visualstudio.microsoft.com/)

No Python dependencies are necessary! You are ready to go.

## Usage

1. Write your shellcode in `shellcode.asm`
2. Run `python shellcoder.py`
3. Execute `out/malware.exe` file!

![shellcoder.py command line output](/_img/shellcoder-cli.png)

## Output files

The output files of this script are stored in `out/` directory:

- `malware.c` - loader code with the injected payload as C string.
- `malware.exe` - compiled loader with the injected payload.
- `shellcode.exe` - executable file with the payload only. Great for debugging!
- `shellcode.bin` - raw machine code of the assembly payload.

![shellcoder.py output files](/_img/shellcoder-output.png)

## Caveats

- Indicate that you are using 64-bit mode at the beginning of the assembly file. Add `[bits 64]` to the `shellcode.asm`.
- Define entry point in assembly file (required for debugging):

```nasm
[bits 64]

section .text:
    global _start

_start:
[...YOUR CODE HERE...]
```

- You cannot use sections other than `.text`. It's a shellcode!
- Remember about [Microsoft x64 Calling Convention](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170) (stack alignment + shadow space!)

## How to debug the payload?

The best way to debug your assembly code is to take `out/shellcode.exe` file and load it into your favorite debugger.

Finally you should run `out/malware.exe` to be sure that your payload works as intended after memory injection.
