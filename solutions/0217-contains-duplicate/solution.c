/*
 * Problem: 217. Contains Duplicate
 * URL: https://leetcode.com/problems/contains-duplicate/
 * Difficulty: Easy
 * Date: X/X/2024
 */

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

// Hash set (using a hash table for simplicity)
typedef struct Node {
    int key;
    struct Node* next;
} Node;

typedef struct {
    Node** buckets;
    int size;
} HashSet;

// Function to create a new node
Node* createNode(int key) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }
    newNode->key = key;
    newNode->next = NULL;
    return newNode;
}

// Function to create a new hash set
HashSet* createHashSet(int size) {
    HashSet* set = (HashSet*)malloc(sizeof(HashSet));
    if (!set) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }
    set->buckets = (Node**)malloc(size * sizeof(Node*));
    if (!set->buckets) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }
    set->size = size;
    // Initialize buckets
    for (int i = 0; i < size; i++) {
        set->buckets[i] = NULL;
    }
    return set;
}

// Function to calculate hash value
int hash(int key, int size) {
    return abs(key) % size;
}

// Function to insert a key into the hash set
void insert(HashSet* set, int key) {
    int index = hash(key, set->size);
    Node* newNode = createNode(key);
    newNode->next = set->buckets[index];
    set->buckets[index] = newNode;
}

// Function to check if a key exists in the hash set
bool contains(HashSet* set, int key) {
    int index = hash(key, set->size);
    Node* current = set->buckets[index];
    while (current) {
        if (current->key == key) {
            return true;
        }
        current = current->next;
    }
    return false;
}

// Function to free memory used by the hash set
void freeHashSet(HashSet* set) {
    if (!set) return;
    for (int i = 0; i < set->size; i++) {
        Node* current = set->buckets[i];
        while (current) {
            Node* temp = current;
            current = current->next;
            free(temp);
        }
    }
    free(set->buckets);
    free(set);
}

// Function to check if the array contains any duplicate elements
bool containsDuplicate(int* nums, int numsSize) {
    HashSet* set = createHashSet(numsSize); // Create a hash set
    for (int i = 0; i < numsSize; i++) {
        if (contains(set, nums[i])) {
            // Found a duplicate
            freeHashSet(set);
            return true;
        }
        insert(set, nums[i]); // Insert current element into hash set
    }
    freeHashSet(set);
    return false; // No duplicates found
}
