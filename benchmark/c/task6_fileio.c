#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_WORDS 10000
#define MAX_WORD_LEN 256

void count_words(const char* input_file, const char* output_file) {
    char words[MAX_WORDS][MAX_WORD_LEN];
    int counts[MAX_WORDS] = {0};
    int word_count = 0;

    FILE* in = fopen(input_file, "r");
    char word[MAX_WORD_LEN];

    while (fscanf(in, "%255s", word) == 1) {
        int found = -1;
        for (int i = 0; i < word_count; i++) {
            if (strcmp(words[i], word) == 0) {
                found = i;
                break;
            }
        }
        if (found >= 0) {
            counts[found]++;
        } else {
            strcpy(words[word_count], word);
            counts[word_count] = 1;
            word_count++;
        }
    }
    fclose(in);

    FILE* out = fopen(output_file, "w");
    for (int i = 0; i < word_count; i++)
        fprintf(out, "%s: %d\n", words[i], counts[i]);
    fclose(out);
}
