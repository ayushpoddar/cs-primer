from __future__ import annotations
from collections import deque

"""
Need a struct that represents a jug - maxCapacity, currentCapacity
A state is the current state of all the jugs
One operation means - pouring from one jug to another, filling water from river to jug, emptying water from jug to river

- Start with the initial state of all jugs empty
- To get the children of the state,
    - For each jug, try to perform the three operations one by one (one operation gives one new state)
    - In case of the jug transfer operation,
        - The operation needs to be performed on each jug separately
        - The recipient jug will tell the amount of water it took so that the source jug knows its new currentCapacity

- A state can be a struct of all the jugs and the parent states

- Initialise the empty state - all jugs empty
- Add the initial state to the queue
- As long as the queue is not empty
  - Dequeue the state (current state) which is first in the queue
  - Check if any of the jugs in the current state contains the target amount. If yes, return the state
  - Get the children of the current state
  - For each child,
      - Check if the child is already visited
      - If not, add the child to the queue
      - Add the child to the visited set

"""

class Jug:
    def __init__(self, maxCapacity, currentCapacity = 0):
        self.maxCapacity = maxCapacity
        self.__currentCapacity = currentCapacity

    @staticmethod
    def equivalentListOfJugs(listA: list[Jug], listB: list[Jug]):
        matched = set()
        for jugA in listA:
            for i, jugB in enumerate(listB):
                if i in matched:
                    continue
                if jugA == jugB:
                    matched.add(i)
                    break
                # No match found for jugA in listB
                return False
        return True

    def isNotEmpty(self):
        return self.__currentCapacity > 0

    def hasSpace(self):
        return self.__currentCapacity < self.maxCapacity

    def hasExactly(self, amount: int):
        return self.__currentCapacity == amount

    def __eq__(self, other: object):
        if not isinstance(other, Jug):
            return False
        return self.maxCapacity == other.maxCapacity and self.__currentCapacity == other.__currentCapacity

    def __str__(self) -> str:
        return f"🍶({self.__currentCapacity} out of {self.maxCapacity})"

    def __fillableCapacity(self):
        return self.maxCapacity - self.__currentCapacity

    def transferFromRiver(self):
        return (
                Jug(self.maxCapacity, self.maxCapacity),
                f"Transfer from river to {self.maxCapacity} L jug"
                )

    def transferToRiver(self):
        return (
                Jug(self.maxCapacity, 0),
                f"Transfer from {self.maxCapacity} L jug to river"
                )

    def transferToJug(self, jug: Jug):
        otherNewJug, amountTransferred = jug.__fill(self.__currentCapacity)
        return (
            Jug(self.maxCapacity, self.__currentCapacity - amountTransferred),
            otherNewJug,
            f"Transfer {amountTransferred} L from {self.maxCapacity} L jug to {otherNewJug.maxCapacity} L jug"
        )

    def __fill(self, amount: int):
        possibleFillable = min(self.__fillableCapacity(), amount)
        return (Jug(self.maxCapacity, self.__currentCapacity + possibleFillable), possibleFillable)

class State:
    def __init__(self, jugs: list[Jug], parents: list[State] = [], operation: str = ""):
        self.jugs = jugs
        self.parents = parents
        self.operation = operation

    def jugsStr(self):
        return ", ".join([str(j) for j in self.jugs])

    def __str__(self) -> str:
        result = []
        for parent in self.parents:
            result.append(parent.jugsStr() + f" [{parent.operation}]")
        result.append(self.jugsStr() + f" [{self.operation}]")
        result.append(f"{len(self.parents)} operations performed")
        return "\n".join(result)

    def isVisited(self, jugsList: list[Jug]):
        for parent in self.parents:
            if Jug.equivalentListOfJugs(parent.jugs, jugsList):
                return True

    def containsTargetAmount(self, targetAmount: int):
        for jug in self.jugs:
            if jug.hasExactly(targetAmount):
                return True
        return False

    def __cloneJugs(self):
        return [j for j in self.jugs]

    def children(self):
        for i, thisJug in enumerate(self.jugs):
            if thisJug.isNotEmpty():
                for j, otherJug in enumerate(self.jugs):
                    if j != i:
                        thisNewJug, otherNewJug, operation = thisJug.transferToJug(otherJug)
                        if thisNewJug != thisJug:
                            clonedJugs = self.__cloneJugs()
                            clonedJugs[i] = thisNewJug
                            clonedJugs[j] = otherNewJug
                            if not self.isVisited(clonedJugs):
                                yield State(
                                    clonedJugs,
                                    self.parents + [self],
                                    operation,
                                )

                newJug, operation = thisJug.transferToRiver()
                clonedJugs = self.__cloneJugs()
                clonedJugs[i] = newJug
                if not self.isVisited(clonedJugs):
                    yield State(clonedJugs, self.parents + [self], operation)

            if thisJug.hasSpace():
                newJug, operation = thisJug.transferFromRiver()
                clonedJugs = self.__cloneJugs()
                clonedJugs[i] = newJug
                if not self.isVisited(clonedJugs):
                    yield State(clonedJugs, self.parents + [self], operation)

if __name__ == "__main__":
    jugs = [Jug(3), Jug(5), Jug(7)]
    targetAmount = 1
    states = deque([State(jugs)])
    while states:
        currentState = states.popleft()
        if currentState.containsTargetAmount(targetAmount):
            print(currentState)
            break
        for child in currentState.children():
            states.append(child)
