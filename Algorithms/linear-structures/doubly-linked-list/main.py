class Node:
    def __init__(self, value, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev


class DoubleEndedQueue:
    def __init__(self):
        self.head: Node = None
        self.tail: Node = None

    def is_empty(self):
        return self.head is None

    def __createNode(self, value, next=None, prev=None):
        return Node(value, next, prev)

    def push(self, value):
        node = self.__createNode(value, None, self.tail)
        if self.is_empty():
            self.tail = self.head = node
        else:
            self.tail.next = node
            self.tail = node

    def pop(self):
        if self.is_empty():
            return None

        current_tail = self.tail
        if current_tail.prev is None:
            self.head = self.tail = None
            return current_tail.value
        new_tail = current_tail.prev
        self.tail = new_tail
        self.tail.next = None
        return current_tail.value

    def queue(self, value):
        node = self.__createNode(value, self.head, None)
        if self.is_empty():
            self.head = self.tail = node
        else:
            self.head.prev = node
            self.head = node

    def dequeue(self):
        if self.is_empty():
            return None
        current_head = self.head
        if current_head.next is None:
            self.head = self.tail = None
            return current_head.value
        new_head = current_head.next
        self.head = new_head
        self.head.prev = None
        return current_head.value

    def peek_tail(self):
        if self.is_empty():
            return None
        return self.tail.value

    def peek_head(self):
        if self.is_empty():
            return None
        return self.head.value


def test_doubly_linked_list():
    # Test initialization
    deque = DoubleEndedQueue()
    assert deque.is_empty() is True
    assert deque.peek_head() is None
    assert deque.peek_tail() is None

    # Test push
    deque.push(1)
    assert deque.peek_tail() == 1
    assert deque.peek_head() == 1
    assert deque.is_empty() is False

    # Test queue
    deque.queue(2)
    assert deque.peek_head() == 2
    assert deque.peek_tail() == 1

    # Test pop
    assert deque.pop() == 1
    assert deque.peek_tail() == 2
    assert deque.peek_head() == 2

    # Test dequeue
    deque.push(3)
    assert deque.dequeue() == 2
    assert deque.peek_head() == 3
    assert deque.peek_tail() == 3

    # Test clearing the list
    assert deque.pop() == 3
    assert deque.is_empty() is True
    assert deque.pop() is None
    assert deque.dequeue() is None

    print("All test cases passed!")


if __name__ == "__main__":
    test_doubly_linked_list()
