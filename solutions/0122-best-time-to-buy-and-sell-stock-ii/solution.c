/*
 * Problem: 122. Best Time to Buy and Sell Stock II
 * URL: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/
 * Difficulty: Medium
 * Date: X/X/2024
 */

#include <stdio.h>

int maxProfit(int* prices, int pricesSize) {
    int maxProfit = 0;
    
    for (int i = 0; i < pricesSize - 1; i++) {
        // If the price on the next day is higher, we can make a profit
        if (prices[i + 1] > prices[i]) {
            // Buy on day i and sell on day i+1
            maxProfit += prices[i + 1] - prices[i];
        }
    }
    
    return maxProfit;
}
