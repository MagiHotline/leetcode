/*
 * Problem: 60. Plus One
 * URL: https://leetcode.com/problems/plus-one/
 * Difficulty: Easy
 * Date: 22/08/2026
 */

#include <vector>

using namespace std;
class Solution {
public:
  vector<int> plusOne(vector<int> &digits) {
    int last = digits.size() - 1;
    for (int i = last; i >= 0; i--) {
      if (digits[i] + 1 <= 9) {
        digits[i]++;
        break;
      } else {
        digits[i] = 0;
      }
    }
    // if the last was 9 then
    if (digits[0] == 0) {
      digits[0] = 1;
      digits.push_back(0);
    }
    return digits;
  }
};
