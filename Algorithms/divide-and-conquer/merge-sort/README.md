## Problem Statement

If you were tasked to come up with a sorting algorithm on your own, it's almost certain that you would end up at an O(n^2) algorithm like insertion sort or selection sort. In fact the more you try to improve on your approach, the more you may convince yourself that sorting is naturally O(n^2) and that in a way it requires every item to be compared to every other. Spoiler alert: it's possible to do better, and in fact much better, by dividing up the work in a clever way.

In this problem, you'll implement the remarkable merge sort algorithm, one such way to do it, and one of the first "divide and conquer" algorithms.

I suggest that you first do this without regard to extra space used, or the time taken for extra memory allocations. Instead just focus on the core idea of the algorithm: recursively sorting subarrays then merging them. Once you have done this, as a stretch goal, you may wish to reduce your extra space used to an extra array of size n, and ideally to avoid unnecessary memory allocations.

Note: this video is long mostly because I do the stretch goal, and also try to refactor my solution for brevity. The core idea is covered early on.
