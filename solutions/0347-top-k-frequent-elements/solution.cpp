/*
 * Problem: 347. Top K Frequent Elements
 * URL: https://leetcode.com/problems/top-k-frequent-elements/
 * Difficulty: Medium
 * Date: X/X/2024
 */

#include <unordered_map>
#include <vector>

using namespace std;
class Solution {
public:
  vector<int> topKFrequent(vector<int> &nums, int k) {
    // [1,1,1,2,2,3], k = 2
    // vector<> must be of length 2 at the end
    // if its not of length 2 then return -1
    vector<int> res;
    std::unordered_map<int, int> occ;
    for (int i = 0; i < nums.size(); i++) {
      occ[nums[i]]++;
    }

    for (int i = 0; i < k; i++) {
      int currentMax = -1;
      int arg_max = 0;

      for (auto it = occ.cbegin(); it != occ.cend(); ++it) {
        if (it->second > currentMax) {
          arg_max = it->first;
          currentMax = it->second;
        }
      }

      res.push_back(arg_max);
      occ.erase(arg_max);
    }

    return res;
  }
};
