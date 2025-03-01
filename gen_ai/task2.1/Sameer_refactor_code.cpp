// GPT CODE
#include <iostream>
using namespace std;

struct Node {
    int data;
    Node *next;
};

class singlyLL {
private:
    Node *head;
    Node *tail;

    void split(Node* source, Node** front, Node** back);
    Node* mergeSortedLists(Node* a, Node* b);
    Node* mergeSort(Node* node); // New helper function for sorting

public:
    singlyLL() : head(nullptr), tail(nullptr) {}

    void insert_at_head(int h);
    void insert_at_tail(int t);
    void insert_at_position(int dat, int position);
    void delete_at_head();
    void delete_at_tail();
    void displayLL();
    void sortList(); // Sorts the linked list

    ~singlyLL();
};

// Insert at head
void singlyLL::insert_at_head(int h) {
    Node *temp = new Node{h, head};
    if (!head) {
        tail = temp;
    }
    head = temp;
}

// Insert at tail
void singlyLL::insert_at_tail(int t) {
    Node *temp = new Node{t, nullptr};
    if (!head) {
        head = tail = temp;
    } else {
        tail->next = temp;
        tail = temp;
    }
}

// Insert at a given position
void singlyLL::insert_at_position(int dat, int position) {
    if (position == 0) {
        insert_at_head(dat);
        return;
    }

    Node *temp = new Node{dat, nullptr};
    Node *midptr = head;
    int counter = 1;

    while (midptr && counter < position) {
        midptr = midptr->next;
        counter++;
    }

    if (midptr) {
        temp->next = midptr->next;
        midptr->next = temp;
        if (midptr == tail) { // If inserting at tail, update tail
            tail = temp;
        }
    } else {
        cout << "Wrong position. You can't insert." << endl;
        delete temp;
    }
}

// Delete at head
void singlyLL::delete_at_head() {
    if (!head) return;
    Node *ptr = head;
    head = head->next;
    if (!head) tail = nullptr; // If list is empty, reset tail
    delete ptr;
}

// Delete at tail
void singlyLL::delete_at_tail() {
    if (!head) return;
    if (head == tail) { // Only one element in the list
        delete head;
        head = tail = nullptr;
        return;
    }

    Node *ptr = head;
    while (ptr->next != tail) {
        ptr = ptr->next;
    }
    delete tail;
    tail = ptr;
    tail->next = nullptr;
}

// Display the linked list
void singlyLL::displayLL() {
    Node *ptr = head;
    while (ptr) {
        cout << ptr->data << " ";
        ptr = ptr->next;
    }
    cout << endl;
}

// Split the linked list into two halves
void singlyLL::split(Node* source, Node** front, Node** back) {
    if (!source || !source->next) {
        *front = source;
        *back = nullptr;
        return;
    }

    Node* slow = source;
    Node* fast = source->next;

    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }

    *front = source;
    *back = slow->next;
    slow->next = nullptr;
}

// Merge two sorted linked lists
Node* singlyLL::mergeSortedLists(Node* a, Node* b) {
    if (!a) return b;
    if (!b) return a;

    if (a->data <= b->data) {
        a->next = mergeSortedLists(a->next, b);
        return a;
    } else {
        b->next = mergeSortedLists(a, b->next);
        return b;
    }
}

// Merge Sort Helper Function
Node* singlyLL::mergeSort(Node* node) {
    if (!node || !node->next) return node;

    Node *a, *b;
    split(node, &a, &b);

    a = mergeSort(a);
    b = mergeSort(b);

    return mergeSortedLists(a, b);
}

// Sort the linked list using Merge Sort
void singlyLL::sortList() {
    head = mergeSort(head);

    // Update tail pointer after sorting
    tail = head;
    while (tail && tail->next) {
        tail = tail->next;
    }
}

// Destructor to free memory
singlyLL::~singlyLL() {
    Node *ptr = head;
    while (ptr) {
        Node *nextNode = ptr->next;
        delete ptr;
        ptr = nextNode;
    }
}

// Main Function
int main() {
    singlyLL list;
    list.insert_at_head(10);
    list.insert_at_tail(7);
    list.insert_at_position(15, 0);
    list.insert_at_position(25, 3);

    cout << "Original List: ";
    list.displayLL();

    list.sortList();
    cout << "Sorted List: ";
    list.displayLL();

    list.delete_at_head();
    cout << "After deleting head: ";
    list.displayLL();

    list.delete_at_tail();
    cout << "After deleting tail: ";
    list.displayLL();

    return 0;
}
