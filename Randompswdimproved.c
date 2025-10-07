/*
What Should Be Corrected:

Avoid setting randomizer = rand() % 4; multiple times inside the loop

Move the call to rand() % 4 inside the loop once per iteration instead of repeating it inside each if block to reduce redundancy and improve clarity.

Simplify the character selection logic

Instead of multiple if-else branches, use a single switch-case or array lookup to select the character set, which makes the code easier to read and maintain.

Add null-termination ('\0') to the password array

Since the password is a string, terminate it properly with a null character (password[N] = '\0';) to prevent undefined behavior when treated as a string.

Separate password generation and output

Don’t call printf inside the loop; instead, build the password fully, then print it once. This improves separation of concerns and makes the code cleaner.

Seed the random number generator (srand) only once

Call srand(time(NULL)); once before generating passwords, not inside the password generation function if called multiple times, to avoid resetting the seed repeatedly.

(Optional) Ensure password contains at least one character from each category

To improve password strength, add logic that guarantees the presence of at least one number, one uppercase letter, one lowercase letter, and one symbol.
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to generate a random password of length N
void randomPasswordGeneration(int N) {
    // Character sets
    const char numbers[] = "0123456789";
    const char lowercase[] = "abcdefghijklmnopqrstuvwxyz";
    const char uppercase[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const char symbols[] = "!@#$^&*?";

    // Array of all character sets
    const char* charSets[] = { numbers, lowercase, uppercase, symbols };
    const int setSizes[] = {
        sizeof(numbers) - 1,
        sizeof(lowercase) - 1,
        sizeof(uppercase) - 1,
        sizeof(symbols) - 1
    };

    char* password = malloc(N + 1); // +1 for null-terminator
    if (!password) {
        fprintf(stderr, "Memory allocation failed.\n");
        return;
    }

    // Seed randomness
    srand((unsigned int)time(NULL));

    for (int i = 0; i < N; i++) {
        int setIndex = rand() % 4; // Pick random set
        const char* set = charSets[setIndex];
        int setSize = setSizes[setIndex];

        password[i] = set[rand() % setSize];
    }

    password[N] = '\0'; // Null-terminate string

    printf("Generated Password: %s\n", password);

    free(password);
}

// Driver code
int main() {
    int length = 10;
    randomPasswordGeneration(length);
    return 0;
}
