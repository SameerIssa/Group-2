#include <iostream>
#include <stack>
using namespace std;

struct node {
    int data;
    node *next;
};

class queueLL {
private:
    node *head;
    node *tail;

public:
    queueLL() : head(nullptr), tail(nullptr) {}
    ~queueLL();
    bool isEmpty();
    void enqueue(int value);
    void dequeue();
    int nodeCount();
    void showFront();
    void printQueue();
    void printReverseQueue();
};

queueLL::~queueLL() {
    while (!isEmpty()) {
        dequeue();
    }
}

bool queueLL::isEmpty() {
    return head == nullptr;
}

void queueLL::enqueue(int value) {
    node *temp = new node{value, nullptr};
    if (isEmpty()) {
        head = tail = temp;
    } else {
        tail->next = temp;
        tail = temp;
    }
}

void queueLL::dequeue() {
    if (isEmpty()) {
        cout << "Queue is empty" << endl;
        return;
    }
    node *ptr = head;
    head = head->next;
    delete ptr;
    if (head == nullptr) {
        tail = nullptr;
    }
}

int queueLL::nodeCount() {
    int count = 0;
    node *ptr = head;
    while (ptr != nullptr) {
        count++;
        ptr = ptr->next;
    }
    return count;
}

void queueLL::printQueue() {
    if (isEmpty()) {
        cout << "Queue is empty" << endl;
        return;
    }
    node *ptr = head;
    while (ptr != nullptr) {
        cout << ptr->data << " ";
        ptr = ptr->next;
    }
    cout << endl;
}

void queueLL::printReverseQueue() {
    if (isEmpty()) {
        cout << "Queue is empty" << endl;
        return;
    }
    stack<int> s;
    node *ptr = head;
    while (ptr != nullptr) {
        s.push(ptr->data);
        ptr = ptr->next;
    }
    while (!s.empty()) {
        cout << s.top() << " ";
        s.pop();
    }
    cout << endl;
}

void queueLL::showFront() {
    if (isEmpty()) {
        cout << "Queue is empty" << endl;
    } else {
        cout << head->data << endl;
    }
}

int main() {
    queueLL qobj;

    cout << (qobj.isEmpty() ? "Queue is empty" : "Queue is not empty") << endl;

    qobj.enqueue(10);
    qobj.enqueue(13);
    qobj.enqueue(19);

    qobj.printQueue();
    qobj.printReverseQueue();
    qobj.showFront();

    qobj.dequeue();
    qobj.printQueue();
    
    cout << "Node Count: " << qobj.nodeCount() << endl;

    return 0;
}
