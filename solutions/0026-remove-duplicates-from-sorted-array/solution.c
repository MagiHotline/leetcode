/*
 * Problem: 26. Remove Duplicates from Sorted Array
 * URL: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
 * Difficulty: Easy
 * Topics: Array, Two Pointers
 * Date: 2024/X/X
 */

#include <stdio.h>

int removeDuplicates(int* nums, int numsSize) {
    int k = 0;
    int ok;
    int t = 0;
    int notDuplicates[numsSize];
    for(int i = 0; i < numsSize; i++) {
        ok = 1;
        if(i != 0) {
            for(int j = i; j > 0 && ok; j--) {
                if(nums[i] == nums[j-1]) ok = 0;
            }
        }
        
        if(ok) {
            notDuplicates[t] = nums[i];
            k++;
            t++;
        }
    }
    
    for(int i = 0; i < numsSize; i++) {
        nums[i] = notDuplicates[i];
    }

    return k;
}
