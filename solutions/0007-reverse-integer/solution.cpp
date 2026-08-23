/*
 * Problem: 7. Reverse Integer
 * URL: https://leetcode.com/problems/reverse-integer/
 * Difficulty: Medium
 * Date: 23/08/2026
 */

#include <climits>
#include <cmath>
class Solution {
public:
  int number_of_digits(int x) {
    int count = 0;
    while (x != 0) {
      count++;
      x = x / 10;
    }
    return count;
  }

  int reverse(int x) {
    bool is_negative = false;

    if (x >= INT_MAX || x <= INT_MIN) {
      return 0;
    }

    if (x < 0) {
      is_negative = true;
      x *= -1;
    }

    int ndigits = number_of_digits(x);

    if (x <= 9 && !is_negative) {
      return x;
    } else {
      int y = x % 10; // take the first digit
      if (is_negative) {

        if ((-1 * (y * pow(10, ndigits - 1) + reverse(x / 10))) <= INT_MIN) {
          return 0;
        }

        return -1 * ((y * pow(10, ndigits - 1)) + reverse(x / 10));
      } else {

        if ((y * pow(10, ndigits - 1) + reverse(x / 10)) > INT_MAX) {
          return 0;
        }

        return (y * pow(10, ndigits - 1)) + reverse(x / 10);
      }
    }
  }
};
