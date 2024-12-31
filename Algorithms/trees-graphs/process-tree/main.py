import sys
from collections import deque


def prefix(level, hasChildren, isLastSibling):
    last = "-+=" if hasChildren else "--="
    if level == 0:
        return last

    if level == 1:
        start = " \\" if isLastSibling else " |"
        return start + last

    n = level - 1
    spaces = (1 + (n - 1) * 2)
    sep = "\\" if isLastSibling else "|"

    return " |" + (" " * spaces) + sep + last


class Node:
    def __init__(self, pid, ppid, args):
        self.pid = pid
        self.ppid = ppid
        self.args = args
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def has_children(self):
        return len(self.children) > 0

    def print(self, level=0, isLastSibling=False):
        start = prefix(level, self.has_children(), isLastSibling)
        print(f"{start}PID: {self.pid}, PPID: {self.ppid}, ARGS: {self.args}")
        for i, child in enumerate(self.children):
            child.print(level + 1, i == len(self.children) - 1)


headers = []
nodes = []
for i, line in enumerate(sys.stdin):
    if i == 0:
        line = line.strip().split()
        headers = line
    else:
        line = line.strip().split(maxsplit=(len(headers) - 1))
        nodes.append(Node(line[0], line[1], line[2]))

all_pids = set([node.pid for node in nodes])
root_nodes = filter(lambda node: node.ppid not in all_pids, nodes)
root_nodes = list(root_nodes)

queue = deque(root_nodes)

while len(queue):
    current_node = queue.popleft()
    for node in nodes:
        if node.ppid == current_node.pid:
            current_node.add_child(node)
            queue.append(node)

for node in root_nodes:
    node.print()
