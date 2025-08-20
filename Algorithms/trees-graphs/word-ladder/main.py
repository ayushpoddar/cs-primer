import sys
from collections import deque

def build_word_map():
    result: dict[str, list[str]] = {}
    with open("words.txt", "r") as f:
        for line in f:
            word = line.strip().lower()
            for i in range(len(word)):
                # Create a key by replacing one character with '*'
                # This allows us to group words that differ by one character
                key = word[:i] + "*" + word[i+1:]
                if key not in result:
                    result[key] = []
                result[key].append(word)
    return result

word_map = build_word_map()
visited = set()

class Block:
    def __init__(self, words: list[str], parents: list[str] = []):
        self.words = words
        self.parents = parents
        for w in words:
            visited.add(w)

    def parents_path(self):
        return self.parents

    def path_length(self):
        return len(self.parents)

    def has_word(self, word: str):
        return word in self.words

    def add_word(self, word: str):
        self.words.append(word)
        visited.add(word)

    def is_visited(self, word: str):
        return word in visited

    def next_blocks(self):
        for word in self.words:
            next_block = Block([], self.parents + [word])
            for i in range(len(word)):
                key = word[:i] + "*" + word[i+1:]
                if key in word_map:
                    for new_word in word_map[key]:
                        if not next_block.is_visited(new_word):
                            next_block.add_word(new_word)
            yield next_block


def main():
    start_word = sys.argv[1]
    end_word = sys.argv[2]

    result = get_shortest_path_length(start_word, end_word)
    if result["path_length"]:
        print(f"The shortest path from {start_word} to {end_word} is {' -> '.join(result['parents_path']) + ' -> ' + end_word} ({result['path_length']} steps)")
        return

    print(f"No path from {start_word} to {end_word} exists")

def get_shortest_path_length(start: str, end: str):
    processable_blocks = deque([Block([start])])
    while processable_blocks:
        current_block = processable_blocks.popleft()
        if current_block.has_word(end):
            return {
                "path_length": current_block.path_length(),
                "parents_path": current_block.parents_path()
            }

        for next_block in current_block.next_blocks():
            processable_blocks.append(next_block)

    return {
            "path_length": 0,
            "parents_path": ""
            }

if __name__ == "__main__":
    main()
