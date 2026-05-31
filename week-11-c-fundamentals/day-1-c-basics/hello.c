/*
 * First C program — compile and run:
 *   gcc hello.c -o hello
 *   ./hello        (Linux/Mac)
 *   hello.exe      (Windows)
 */
#include <stdio.h>
#include <string.h>

int main() {
    // --- Variables ---
    int port = 443;
    char ip[] = "192.168.1.1";
    float timeout = 1.5;
    int is_open = 1;  // C has no bool (before C99), use int

    printf("=== C Basics Demo ===\n\n");

    // --- Printf formatting ---
    printf("Target: %s:%d\n", ip, port);
    printf("Timeout: %.1f seconds\n", timeout);
    printf("Open: %s\n", is_open ? "yes" : "no");
    printf("\n");

    // --- Sizes of types (this matters for exploits) ---
    printf("--- Type sizes ---\n");
    printf("char:      %zu byte\n", sizeof(char));
    printf("short:     %zu bytes\n", sizeof(short));
    printf("int:       %zu bytes\n", sizeof(int));
    printf("long:      %zu bytes\n", sizeof(long));
    printf("long long: %zu bytes\n", sizeof(long long));
    printf("float:     %zu bytes\n", sizeof(float));
    printf("double:    %zu bytes\n", sizeof(double));
    printf("pointer:   %zu bytes\n", sizeof(void*));
    printf("\n");

    // --- Hex output (you'll use this constantly) ---
    int value = 0xDEADBEEF;
    printf("--- Hex ---\n");
    printf("Decimal:  %d\n", value);
    printf("Hex:      0x%x\n", value);
    printf("Padded:   0x%08x\n", value);
    printf("Unsigned: %u\n", (unsigned int)value);
    printf("\n");

    // --- Strings ---
    char greeting[50];
    snprintf(greeting, sizeof(greeting), "Scanning %s on port %d", ip, port);
    printf("%s\n", greeting);
    printf("String length: %zu\n", strlen(greeting));

    return 0;
}
