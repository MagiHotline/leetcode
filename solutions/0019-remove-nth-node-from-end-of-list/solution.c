/*
 * Problem: 19. Remove Nth Node From End of List
 * URL: https://leetcode.com/problems/remove-nth-node-from-end-of-list/
 * Difficulty: Medium
 * Date: X/X/2024
 */

#include <stdio.h>
#include <stdlib.h>

struct ListNode {
    int val;
    struct ListNode *next;
};

struct ListNode* removeNthFromEnd(struct ListNode* head, int n) {
    struct ListNode dummy;
    dummy.val = 0;
    dummy.next = head;

    struct ListNode* fast = &dummy;
    struct ListNode* slow = &dummy;

    for (int i = 0; i <= n; i++) {
        if (fast == NULL) return head;
        fast = fast->next;
    }

    while (fast != NULL) {
        fast = fast->next;
        slow = slow->next;
    }

    struct ListNode* nodeToDelete = slow->next;
    if (nodeToDelete != NULL) {
        slow->next = nodeToDelete->next;
        free(nodeToDelete);
    }

    return dummy.next;
}
