/*
 * Problem: 136. Single Number
 * URL: https://leetcode.com/problems/single-number/
 * Difficulty: Easy
 * Topics: Array, Bit Manipulation
 * Date: 2024/X/X
 */

#include <stdio.h>

int singleNumber(int* nums, int numsSize) {
    int ok;
    int Single = 0;
    if(numsSize <= 1) {
        return *nums;
    } else {
        for(int i = 0; i < numsSize; i++) {
            ok = 0;
            for(int j = 0; j < numsSize && ok != 2; j++) {
                if(nums[i] == nums[j]) {
                    ok++;
                }
            }
            
            if(ok == 1) {
                Single = nums[i];
            }
        }   
    }
    
    return Single;
}
