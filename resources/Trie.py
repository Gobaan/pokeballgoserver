from typing import List

class Trie:
    def __init__(self, string: str):
        self.string = string
        self.children = {}
        self.is_final = False

    def add_word(self, word: str):
        if not word:
            self.is_final = True

            return
        start, rest = word[0], word[1:]

        if start not in self.children:
            self.children[start] = Trie(self.string + start)
        self.children[start].add_word(rest)

    def next_state(self, c: str):
        if not c:
            return self

        if c not in self.children:
            return

        return self.children[c]

    def __str__(self):
        return f'{self.string} {self.is_final} {self.children.keys()}'

    def get_match(self, word: str):
        old_subsequences = [self]
        finalized_names = []

        # Implements a simple NFA, check every character against the root
        # and every word matching so far
        for c in word:
            new_subsequences = []

            for t in old_subsequences:
                new_subsequence = t.next_state(c)

                if new_subsequence:
                    new_subsequences += [new_subsequence]

                    if new_subsequence.is_final:
                        finalized_names += [new_subsequence.string]
            old_subsequences = [self] + new_subsequences

        return finalized_names

    def get_longest_match(self, word: str):
        matches = self.get_match(word)
        matches = sorted(matches, key=lambda x: -len(x))

        if not matches:
            return None

        return matches[0]


def create_trie(lines: List[str]):
    root = Trie('')
    for line in lines:
        root.add_word(line.lower().strip())

    return root


if __name__ == '__main__':
    root = Trie('')
    root.add_word('hello')
    root.add_word('hell')
    root.add_word('goodbye')
    print(root.get_longest_match('goodbye i said hello'))

