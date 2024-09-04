In this problem, we implement the iconic quicksort algorithm, a divide and conquer algorithm than can easily be implemented without additional space, and tends to perform better in practice than other O(n log n) sorting algorithms like merge sort and heapsort.

Quicksort is particularly interesting in that it shows how we can essentially do divide and conquer with a partitioning step before recursing, rather than a merge step after recursive. Both approaches can be useful.

There are a number of ways to implement the partitioning in quicksort; here I show you one that's relatively simple to explain and code up, designed by Nico Lomuto and popularized by Bentley (in his fantastic Programming Pearls column, and also discussed in [this talk](https://www.youtube.com/watch?v=aMnn0Jq0J-E)).
