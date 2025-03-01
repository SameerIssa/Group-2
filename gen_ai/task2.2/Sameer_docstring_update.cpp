//GPT generated code 

#include <iostream>
using namespace std;
const int SIZE = 5;

class stackArray
{
private:
    int top;
    int arr[SIZE];

public:
    stackArray();
    ~stackArray();
    bool isEmpty();         // Check if stack is empty
    bool isFull();          // Check if stack is full
    void push(int value);   // Insert an element
    int pop();              // Remove and return the top element
    int peek(int position); // Return the value at a position
    void printStack();      // Print elements
};

stackArray::stackArray()
{
    top = -1;
    for (int i = 0; i < SIZE; i++)
    {
        arr[i] = 0;
    }
}

stackArray::~stackArray()
{
    cout << "Destructor is invoked" << endl;
}

bool stackArray::isEmpty()
{
    return top == -1;
}

bool stackArray::isFull()
{
    return top == SIZE - 1;
}

void stackArray::push(int value)
{
    if (isFull())
    {
        cout << "Stack is full. Cannot insert " << value << endl;
        return;
    }
    arr[++top] = value;
}

void stackArray::printStack()
{
    if (isEmpty())
    {
        cout << "Stack is empty" << endl;
        return;
    }
    for (int i = 0; i <= top; i++)  // Loop only up to `top`
    {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int stackArray::pop()
{
    if (isEmpty())
    {
        cout << "Stack is empty. Cannot pop a value" << endl;
        return -1;  // Return -1 as an error flag
    }
    return arr[top--]; // Return top element and decrease top
}

int stackArray::peek(int position)
{
    if (position < 0 || position > top)
    {
        cout << "Invalid position: " << position << endl;
        return -1;
    }
    return arr[position];
}

int main()
{
    stackArray starrobj;

    /* 
       Improvements:
       1. Fixed `peek()` to correctly check if the position is within valid bounds.
       2. Updated `printStack()` to display only initialized stack elements (up to `top`).
       3. Changed `pop()` to return `-1` when the stack is empty instead of `0`.
       4. Used a loop in `main()` to pop and print values dynamically instead of redundant calls.
       5. Added better error handling for full and empty stack cases.
    */

    if (starrobj.isEmpty())
        cout << "Stack is Empty" << endl;
    else
        cout << "Stack is not Empty" << endl;

    if (starrobj.isFull())
        cout << "Stack is Full" << endl;
    else
        cout << "Stack is not Full" << endl;

    // Insert elements
    starrobj.push(10);
    starrobj.push(12);
    starrobj.push(7);
    starrobj.push(8);
    starrobj.push(23);
    starrobj.push(76);  // This should display an overflow message

    starrobj.printStack();

    // Pop elements and print the last popped value
    int popValue;
    while (!starrobj.isEmpty())
    {
        popValue = starrobj.pop();
        cout << "Popped value: " << popValue << endl;
    }

    // Trying to pop from an empty stack
    popValue = starrobj.pop();
    if (popValue != -1)
        cout << "This value is deleted using pop(): " << popValue << endl;

    starrobj.printStack();

    return 0;
}