#!/usr/bin/env python3
#
# Shellcoder.py : 
#
# Author: Print3M (https://github.com/Print3M)
# 
# This script helps automate the shellcode testing process.
# It takes an Assembly file with shellcode, compiles
# it into machine code (NASM), generates a payload in C with that,
# and pastes it into the loader C file. Finally, the prepared C file
# is compiled using MSVC. With this script you go from Assembly
# shellcode to executable file with one command! 
#   
# External dependencies:
#   - Python 3
#   - NASM (Netwide Assembler)
#   - Visual Studio 2022

"""
[ ] Sprawdz czy zwykly shellcode dziala
[ ] Moze NASM trzeba jakos inaczej kompilowac / pobierac?
"""

import subprocess
import os
import sys

# Directory with output files
OUT_DIR = "out"

# Utility files
SHELLCODE_INPUT_FILE = "shellcode.asm"
SHELLCODE_OUTPUT_FILE = f"{OUT_DIR}\\shellcode.bin"
LOADER_INPUT_FILE = "loader.c"
LOADER_OUTPUT_FILE = f"{OUT_DIR}\\malware.c"

# String to be replaced by generated payload
PAYLOAD_STRING = ":PAYLOAD:"

# Name of final binary output file
BINARY_OUTPUT_FILE = f"{OUT_DIR}\\malware.exe"

# Batch script with Visual Studio compiler environment variables
MSVC_BATCH_SCRIPT = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat"


def is_cmd_available(cmd: str):
    try:
        subprocess.call(cmd, text=True)
    except FileNotFoundError:
        return False
    
    return True


def assert_cmd(cmd: str):
    if (is_cmd_available(cmd)):
        return 

    print(f"[!] command not found: {cmd}", file=sys.stderr)    
    sys.exit(-1)


if __name__ == "__main__":
    # Check if NASM is available
    assert_cmd("nasm")

    # Prepare output directory
    os.makedirs(OUT_DIR, exist_ok=True)

    # Compile Assembly
    subprocess.run(
        ["nasm", "-f", "bin", SHELLCODE_INPUT_FILE, "-o", SHELLCODE_OUTPUT_FILE], check=True
    )

    print(f"[+] NASM: {SHELLCODE_INPUT_FILE} -> {SHELLCODE_OUTPUT_FILE}")

    # Prepare C array with shellcode payload
    payload = ""
    with open(SHELLCODE_OUTPUT_FILE, "rb") as f:
        bytes = bytearray(f.read())

    size = len(bytes)

    for byte in bytes:
        payload += "\\" + hex(byte).lstrip("0")

    print(f"[+] Payload size: {size} bytes")

    # Inject payload into loader source code
    with open(LOADER_INPUT_FILE, "r") as f:
        loader = f.read()

    loader = loader.replace(PAYLOAD_STRING, payload)

    with open(LOADER_OUTPUT_FILE, "w") as f:
        f.write(loader)

    print(f"[+] {LOADER_INPUT_FILE} -> {LOADER_OUTPUT_FILE}")

    # Compile final binary
    print(f"[*] MSVC: Compilation of {LOADER_OUTPUT_FILE} \n")

    cmd = f'"{MSVC_BATCH_SCRIPT}" && cd "{OUT_DIR}" && cl.exe "../{LOADER_OUTPUT_FILE}"'
    proc = subprocess.run(cmd, check=True, text=True)

    print(f"\n[+] Output binary ({BINARY_OUTPUT_FILE}) is ready to be executed!")
