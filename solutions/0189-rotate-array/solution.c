/*
 * Problem: 189. Rotate Array
 * URL: https://leetcode.com/problems/rotate-array/
 * Difficulty: Medium
 * Date: X/X/2024
 */

#include <stdio.h>

void reverse(int* nums, int start, int end) {
    while (start < end) {
        // Swap elements at start and end indices
        int temp = nums[start];
        nums[start] = nums[end];
        nums[end] = temp;
        // Move indices inward
        start++;
        end--;
    }
}

void rotate(int* nums, int numsSize, int k) {
    // If k is larger than numsSize, take modulo to reduce unnecessary rotations
    k = k % numsSize;
    
    // Reverse the entire array
    reverse(nums, 0, numsSize - 1);
    
    // Reverse the first k elements
    reverse(nums, 0, k - 1);
    
    // Reverse the remaining elements
    reverse(nums, k, numsSize - 1);
}
