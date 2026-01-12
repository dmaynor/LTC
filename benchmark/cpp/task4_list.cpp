#include <vector>
#include <algorithm>

std::vector<int> double_evens(const std::vector<int>& nums) {
    std::vector<int> result;
    for (int n : nums) {
        if (n % 2 == 0)
            result.push_back(n * 2);
    }
    return result;
}
