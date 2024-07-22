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

import subprocess
import os
import sys

# Directory with output files
OUT_DIR = "out"

# Utility files
SHELLCODE_INPUT_FILE = "shellcode.asm"
SHELLCODE_OUTPUT_NAME = f"{OUT_DIR}\\shellcode"
LOADER_INPUT_FILE = "loader.c"
LOADER_OUTPUT_FILE = f"{OUT_DIR}\\malware.c"

# String to be replaced by generated payload
PAYLOAD_STRING = ":PAYLOAD:"

# Name of final binary output file
BINARY_OUTPUT_FILE = f"{OUT_DIR}\\malware.exe"

# Batch script with Visual Studio compiler environment variables
MSVC_BATCH_SCRIPT = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat"

global ENVIRON 


def get_msvc_console_environs() -> dict[str, str]:
    cmd = f'"{MSVC_BATCH_SCRIPT}" && set'
    executable = "C:\\Windows\\System32\\cmd.exe"
    process = subprocess.run(cmd, text=True, check=True, capture_output=True, shell=True, executable=executable)

    if process.returncode != 0:
        print(f"[!] MSVC Developer Console error: {process.stderr}")
        sys.exit(-1)

    envs = {}
    for line in process.stdout.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            envs[key] = value
            
    return envs
  

def is_cmd_available(cmd: str):
    try:
        subprocess.call(cmd, text=True, stderr=subprocess.PIPE)
    except FileNotFoundError:
        return False
    
    return True


def assert_cmd(cmd: str):
    if (is_cmd_available(cmd)):
        return 

    print(f"[!] Command not found: {cmd}", file=sys.stderr)    
    sys.exit(-1)

def cmd_exec(cmd: str):
    subprocess.run(cmd, text=True, check=True, shell=True, env=ENVIRON)

if __name__ == "__main__":
    # Check if NASM is available
    assert_cmd("nasm")
    print("[*] Fetching VS Developer Console envs...")
    ENVIRON = get_msvc_console_environs()

    # Prepare output directory
    os.makedirs(OUT_DIR, exist_ok=True)

    # Compile Assembly (exe)
    SHELLCODE_OBJ_OUTPUT = f"{SHELLCODE_OUTPUT_NAME}.obj"
    cmd_exec(f"nasm -f win64 {SHELLCODE_INPUT_FILE} -o {SHELLCODE_OBJ_OUTPUT}")
    print(f"[+] NASM: {SHELLCODE_INPUT_FILE} -> {SHELLCODE_OUTPUT_NAME}.exe")
    cmd_exec(f'cd "{OUT_DIR}" && link "..\\{SHELLCODE_OBJ_OUTPUT}" /out:shellcode.exe /entry:_start /subsystem:console')

    # Compile Assembly (bin)
    SHELLCODE_BIN_OUTPUT = f"{SHELLCODE_OUTPUT_NAME}.bin"
    cmd_exec(f"nasm -f bin {SHELLCODE_INPUT_FILE} -o {SHELLCODE_BIN_OUTPUT}")
    print(f"[+] NASM: {SHELLCODE_INPUT_FILE} -> {SHELLCODE_BIN_OUTPUT}")

    # Prepare C array with shellcode payload
    payload = ""
    with open(SHELLCODE_BIN_OUTPUT, "rb") as f:
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
    cmd_exec(f'cd "{OUT_DIR}" && cl.exe "../{LOADER_OUTPUT_FILE}"')
    print(f"\n[+] Output binary ({BINARY_OUTPUT_FILE}) is ready to be executed!")
