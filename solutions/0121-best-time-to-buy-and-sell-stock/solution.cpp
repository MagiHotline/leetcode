/*
 * Problem: 121. Best Time to Buy and Sell Stock
 * URL: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
 * Difficulty: Easy
 */

#include <vector>

using namespace std;
class Solution {
public:
  int maxProfit(vector<int> &prices) {
    int minVal = prices[0];
    // prices[1st] = 30$
    int profit = 0;
    // just take the biggest difference that is subsequential
    for (int price : prices) {
      if (price < minVal) {
        minVal = price;
      } else {
        profit = std::max(profit, price - minVal);
      }
    }

    // maxProfit -> maxValue(future) - minValue (past)
    return profit;
  }
};
