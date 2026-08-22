/*
 * Problem: 20. Valid Paranthesis
 * URL: https://leetcode.com/problems/valid-parentheses/
 * Difficulty: Easy
 * Date: 22/08/2026
 */
#include <stack>
#include <string>

using namespace std;

class Solution {
public:
  bool isValid(string s) {
    stack<int> chars;
    for (int i = 0; i < s.length(); i++) {
      if (s[i] == '(' || s[i] == '[' || s[i] == '{') {
        chars.push(s[i]);
      } else {
        if ((s[i] == ')' && chars.top() == '(') ||
            (s[i] == ']' && chars.top() == '[') ||
            (s[i] == '}' && chars.top() == '{')) {
          chars.pop();
        } else {
          return false;
        }
      }
    }

    return true;
  }
};
