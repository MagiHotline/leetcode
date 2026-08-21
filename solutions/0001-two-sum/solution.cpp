#include <unordered_map>
#include <vector>

using namespace std;

class Solution {
public:
  vector<int> twoSum(vector<int> &nums, int target) {
    unordered_map<int, int> results;
    for (int i = 0; i < nums.size(); i++) {
      int j = target - nums[i];

      if (results.contains(j)) {
        return {results[j], i};
      }

      results[nums[i]] = i;
    }

    return {};
  }
};
