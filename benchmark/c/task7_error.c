#include <stdlib.h>
#include <errno.h>

typedef struct {
    int success;
    int value;
    const char* error;
} ParseResult;

ParseResult parse_int(const char* s) {
    char* end;
    errno = 0;
    long val = strtol(s, &end, 10);

    if (errno != 0 || *end != '\0')
        return (ParseResult){0, 0, "Invalid integer format"};

    return (ParseResult){1, (int)val, NULL};
}
