/*
 * Problem: 237. Delete Node in a Linked List
 * URL: https://leetcode.com/problems/delete-node-in-a-linked-list/
 * Difficulty: Medium
 * Topics: Linked List
 * Date: 2024/X/X
 */

#include <stdio.h>
#include <stdlib.h>

struct ListNode {
    int val;
    struct ListNode *next;
};

void deleteNode(struct ListNode* node) {
    if (node == NULL || node->next == NULL) {
        return; // if there are 0 or 1 elements then we can't delete anything
    }

    // Pointer to the next node
    struct ListNode* nextNode = node->next;
    
    // Copy the value of the next node to the current node
    node->val = nextNode->val; 
    
    // Adjust the next pointer of the current node
    node->next = nextNode->next; 

    free(nextNode); // Free the memory of the next node
}
