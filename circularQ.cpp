#include <iostream>
using namespace std;

class CircularQueue {
private:
    int front, rear;
    int size;
    int* queue;

public:
    CircularQueue(int s) {
        front = -1;
        rear = -1;
        size = s;
        queue = new int[size];
    }

    ~CircularQueue() {
        delete[] queue;
    }

    // Check if the queue is full
    bool isFull() {
        return (front == 0 && rear == size - 1) || (front == rear + 1);
    }

    // Check if the queue is empty
    bool isEmpty() {
        return front == -1;
    }

    // Enqueue operation
    void enqueue(int value) {
        if (isFull()) {
            cout << "Queue is full (Overflow)\n";
            return;
        }

        if (isEmpty()) {
            front = rear = 0;
        } else if (rear == size - 1 && front != 0) {
            rear = 0;  // wrap around
        } else {
            rear++;
        }

        queue[rear] = value;
        cout << "Inserted " << value << endl;
    }

    // Dequeue operation
    int dequeue() {
        if (isEmpty()) {
            cout << "Queue is empty (Underflow)\n";
            return -1;
        }

        int data = queue[front];
        queue[front] = -1;  // optional: for clarity

        if (front == rear) {
            front = rear = -1;  // Queue is now empty
        } else if (front == size - 1) {
            front = 0;  // wrap around
        } else {
            front++;
        }

        return data;
    }

    // Display the queue
    void display() {
        if (isEmpty()) {
            cout << "Queue is empty\n";
            return;
        }

        cout << "Queue elements: ";
        if (rear >= front) {
            for (int i = front; i <= rear; i++)
                cout << queue[i] << " ";
        } else {
            for (int i = front; i < size; i++)
                cout << queue[i] << " ";
            for (int i = 0; i <= rear; i++)
                cout << queue[i] << " ";
        }
        cout << endl;
    }
};

int main() {
    CircularQueue q(5);

    q.enqueue(10);
    q.enqueue(20);
    q.enqueue(30);
    q.enqueue(40);
    q.enqueue(50); // Queue is now full

    q.display();

    cout << "Dequeued: " << q.dequeue() << endl;
    cout << "Dequeued: " << q.dequeue() << endl;

    q.enqueue(60);
    q.enqueue(70); // Wraps around

    q.display();

    return 0;
}
