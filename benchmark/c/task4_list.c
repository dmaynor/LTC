#include <stdlib.h>

int* double_evens(int* nums, int len, int* out_len) {
    int count = 0;
    for (int i = 0; i < len; i++)
        if (nums[i] % 2 == 0) count++;

    int* result = malloc(count * sizeof(int));
    int j = 0;
    for (int i = 0; i < len; i++)
        if (nums[i] % 2 == 0)
            result[j++] = nums[i] * 2;

    *out_len = count;
    return result;
}
