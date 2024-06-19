# Problem statement

In this problem, I introduce the idea of asymptotic analysis by describing three different approaches to a problem, and asking you to think about which you like the most. We then discuss how to reason about this abstractly—that is to say, in a way that is agnostic about system specifics—as well as well as some of the "real system" considerations we might like to make, too

# Solution
- **The first approach (nested loop, checking every other element for equality)**:
    - The benefit of this approach is that it does not use any extra memory.
    - However, the time taken by this approach would be of the order of O(n^2)
- **Second approach (sorting, checking adjacent pairs)**:
    - Depending on the sorting algorithm used, the space used may be O(1) or O(n)
    - If we try to implement the best sorting algorithm (merge sort), then the space required would be O(n)
    - Also, comparing adjacent pairs would also be O(n).
- **Third approach (using hash set)**:
    - The time taken would be O(n)
    - The space would also be O(n) in the worst case

In terms of space, the first approach is the best
In terms of time, the third approach is the best

## Cases

1. Array is already sorted
    - Second approach would outperform because then we just need to compare adjacent pairs
2. Array is small
    - It would not make sense to make the additional effort to maintain a hash set / sort the array
    - The first approach would work best.
3. Duplicates are present in the beginning
    - The first approach would work best since we don't have to iterate a lot

## Final thoughts
- The first approach optimises for space. It works best if the system has a small amount of memory.
Also, if we expect the duplicates to be present in the beginning of the array, then this approach would work well since
it saves on the time required to sort the array / add elements to hash set
- The third approach shines when the duplicates are far apart and we may be required to iterate through almost the whole array. Also,
when nothing much is known on the possible patterns of the array, then this approach is the most balanced approach because of it being
the fastest.
- I do not see any situation where this approach is better than the other two

## Link
- [https://csprimer.com/watch/has-dupe/](https://csprimer.com/watch/has-dupe/)
