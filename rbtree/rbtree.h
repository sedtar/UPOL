
#ifndef TREE_H
#define TREE_H

#include <stdlib.h>

typedef enum { RED, BLACK } Color;

struct node {
    int key;
    int value;
    Color color;  

    struct node* left;   
    struct node* right;  
    struct node* parent; 
};
struct node* rbtree_node_alloc();
void rbtree_node_initialize(struct node* node, int key, int value);
struct node* rbtree_node_insert(struct node* root, int key, int value);
struct node* rbtree_node_search(struct node* root, int key); 
void rbtree_node_delete(struct node* root, int key); 
void rbtree_node_free(struct node* n);
#endif