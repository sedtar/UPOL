#include <stdio.h>
#include <stdlib.h>
 
#include "rbtree.h"

//dynamically allocates a new node
struct node* rbtree_node_alloc() {
	//Creates a pointer 'root' and allocates memory equal to the size of a 'node' structure
	struct node* root = (struct node*)malloc(sizeof(struct node));
	if (root == NULL) { // checks if the memory allocation was successful (NULL means failure)
		printf("Memory allocation failed.\n");
		return NULL; //returns null to indicate the node creation failed
	}
	return root; //if everything succeeded, returns a pointer to the newly allocated node
}

//initializes the values of a tree node
void rbtree_node_initialize(struct node* node, int key, int value)
{
	node->key = key; //key of the node
	node->value = value; 
	node->color = RED; // new nodes are always red (red-black tree property)
	node->parent = NULL; // parent pointer is set to NULL (no parent yet)
	node->left = NULL;
	node->right = NULL;
}

// searches for a node by its key in the red-black tree
struct node* rbtree_node_search(struct node* root, int key) {
	struct node* current = root; //sets pointer 'current' to the root of the tree


	while (current != NULL) { //loop until we reach the end (current == NULL)
		if (key != current->key && key < current->key) { // if it's not the searched key and the searched key is smaller than the current node's key
			
			current = current->left; //move to the left subtree
		}
		else if (key != current->key && key > current->key) {
			current = current->right; // move to the right subtree
		}
		else { // otherwise we foudn the key
			return current; 
		}		
	}
	return NULL; // if we reached the end, node not found
}

//recursively frees all nodes in the tree
void rbtree_node_free(struct node* n) {
	if (n == NULL) { // if the pointer is NULL, stop (nothing to free)
		return;
	}
	rbtree_node_free(n->left) // First, free the left subtree recursively
	rbtree_node_free(n->right);     // Then, free the right subtree recursively
	free(n); // Finally, free the current node from memory
}

// Deletes a node by its key
void rbtree_node_delete(struct node* root, int key) {
	struct node* node = rbtree_node_search(root, key);     // Finds the node with the given key using the search function
	if (node == NULL) {
		printf("Uzel s danym klicem neexistuje");
		return;
	}

	struct node* parent = node->parent;   // Gets the parent of the found node

	// If the node has a parent (it’s not the root)
	if (parent != NULL) {     // If the node has a parent (it’s not the root)
		if (parent->left == node) {
			parent->left = NULL;
		}
		else {
			/ Otherwise, it's the right child
			parent->right = NULL;     // Remove right pointer
		}
	}

	rbtree_node_free(node);     // Frees the node and any of its subtrees
}

// Left rotation around node x
static void left_rotate(struct node** root, struct node* x) {
	struct node* y = x->right; //     // y is the right child of x
	if (y == NULL) return;   // If x has no right child, rotation cannot be performed

	x->right = y->left;  // Move y's left subtree to x's right subtree
	if (y->left != NULL) {
		y->left->parent = x; //x se poesune doleva a y->left se stane podstromem x
	}

	y->parent = x->parent;     // Set y's parent to x's parent (y takes x's place)
	if (x->parent == NULL) {
		*root = y;  // If x was the root, y becomes the new root
	}
	else if (x == x->parent->left) {  // If x was a left child, the parent now points to y on the left
		x->parent->left = y;
	}
	else {   // Otherwise x was a right child, parent now points to y on the right
		x->parent->right = y;
	}

	y->left = x; // Put x as the left child of y
	x->parent = y; // Update x's parent to y
}

static void right_rotate(struct node** root, struct node* y) {
	struct node* x = y->left;
	if (x == NULL) return; 

	y->left = x->right;
	if (x->right != NULL) {
		x->right->parent = y;
	}

	x->parent = y->parent; 
	if (y->parent == NULL) {
		*root = x; 
	}
	else if (y == y->parent->right) {
		y->parent->right = x;
	}
	else {
		y->parent->left = x;
	}

	x->right = y;
	y->parent = x;

}

// Fixes red-black tree properties after insertion
static void insert_fixup(struct node** root, struct node* node) {
	while (node->parent != NULL && node->parent->color == RED) {  // Loop runs while the parent exists and is red (two consecutive red nodes are not allowed)
		if (node->parent == node->parent->parent->left) { // CASE 1: parent is the left child of grandparent
			struct node* uncle = node->parent->parent->right;    // Find the uncle – the right child of the grandparent
			if (uncle != NULL && uncle->color == RED) { // CASE 1A: uncle is red
				// Recolor parent and uncle to black
				node->parent->color = BLACK;      
				uncle->color = BLACK;
				// Grandparent becomes red
				node->parent->parent->color = RED;
				node = node->parent->parent;   // Move up the tree (grandparent becomes new node)
			}else {
				//CASE 1B: uncle is black
				if (node == node->parent->right) { // If the node is a right child
					node = node->parent; 
					left_rotate(root, node);  
				}
				node->parent->color = BLACK; // After rotation, recolor parent to black
				node->parent->parent->color = RED;    // And grandparent to red
				right_rotate(root, node->parent->parent); 
			}
		}
		else {
			//CASE 2: parent is the right child of grandparent
			struct node* uncle = node->parent->parent->left; // Find the uncle – the left child of the grandparent
			if (uncle != NULL && uncle->color == RED) {
				//CASE 2A: uncle is red
				node->parent->color = BLACK;
				uncle->color = BLACK;
				node->parent->parent->color = RED;
				node = node->parent->parent; // posuneme se na dideeka
			}
			else {
				//CASE 2B: uncle is black
				if (node == node->parent->left) {  // If the node is a left child
					node = node->parent;
					right_rotate(root, node);
				}
				node->parent->color = BLACK;
				node->parent->parent->color = RED;
				left_rotate(root, node->parent->parent);
			}
		}
	}
	(*root)->color = BLACK; //kooen musí být vždy eerný
}

//Inserts a new node with key and value into a red - black tree
struct node* rbtree_node_insert(struct node* root, int key, int value) {
	struct node* node = rbtree_node_alloc();  // Allocate a new node
	rbtree_node_initialize(node, key, value);   // Initialize node values (key, value, color=RED, parent=NULL, left=NULL, right=NULL)
	if (root == NULL) { //    // If the tree is empty, the new node becomes the root
		node->color = BLACK; // the root will always be black
		return node;
	}
	//Helper pointers for finding the insertion point
	struct node* current = root;
	struct node* parent = NULL;

	//// Find the proper location for the new node (BST rule)
	while (current != NULL) {// while is not a list node
		parent = current;
		if (key < current->key) {
			current = current->left; //go to the left subtree
		}
		else {
			current = current->right; //go to the right subtree
		}
	}
	
	node->parent = parent; //Set the parent of the new node
	

	//Attach the new node as left or right child
	if (key < parent->key) {
		parent->left = node;
	}
	else {
		parent->right = node;
	}
	insert_fixup(&root, node);
	return root;
	
}