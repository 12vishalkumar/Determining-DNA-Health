import math
import os
import random
import re
import sys
import bisect

bisect_left = bisect.bisect_left
bisect_right = bisect.bisect_right
class ScoreTable:
    def __init__(self):
        self.scoreIndexes = []
        self.scoreSums = []
    def append(self, i, s):
        self.scoreIndexes.append(i)
        partial = self.scoreSums[-1] if len(self.scoreSums) > 0 else 0
        self.scoreSums.append(s + partial)
    def getScore(self, start, end):
        lo = bisect_left(self.scoreIndexes, start)
        hi = bisect_right(self.scoreIndexes, end)
        if hi == lo:
            return 0
        elif lo == 0:
            return self.scoreSums[hi-1]
        else:
            return self.scoreSums[hi-1] - self.scoreSums[lo-1]

def longestCommonPrefix(s, t):
    stop = min(len(s), len(t))
    i = 0
    while i < stop and s[i] == t[i]:
        i += 1
    return s[:i]

class TrieNode:
    def __init__(self, label):
        self.label = label
        self.child = {}
        self.scores = None

    def __str__(self):
        return '{' + ','.join([c + ':' + str(n) for c,n in self.child.items()]) + '}'

    def insert(self, k, ix, score):
        '''Insert the key k into the trie rooted at this node.'''
        i = 0
        node = self
        while i < len(k):
            if k[i] in node.child:
                child = node.child[k[i]]
                lcp = longestCommonPrefix(k[i:], child.label)
                if len(lcp) < len(child.label):
                    # Split child node at longest common prefix
                    suffix = child.label[len(lcp):]
                    child.label = suffix
                    prefNode = TrieNode(lcp)
                    prefNode.child[suffix[0]] = child
                    node.child[lcp[0]] = prefNode
                    child = prefNode
                node = child
                i += len(lcp)
            else:
                newNode = TrieNode(k[i:])
                node.child[k[i]] = newNode
                node = newNode
                i = len(k)
        if not node.scores:
            node.scores = ScoreTable()
        node.scores.append(ix, score)

    def traverse(self):
        yield self
        for node in self.child.values():
            yield from node.traverse()

def countNodes(t):
    return sum(1 for _ in t.traverse())

def soloChildren(t):
    return sum(1 for n in t.traverse() if len(n.child) == 1)

def buildGeneTrie(genes, healths):
    trie = TrieNode('')
    for i in range(len(genes)):
        trie.insert(genes[i], i, healths[i])
    return trie

def checkDNA(geneTrie, dna, start, end):
    score = 0
    z = len(dna)
    for i in range(z):
        node = geneTrie
        j = i
        while j < z and dna[j] in node.child:
            node = node.child[dna[j]]
            x = len(node.label)
            if node.label != dna[j:j+x]: break
            if node.scores:
                score += node.scores.getScore(start, end)
            j += x
    return score

def main():
    n = int(input())
    genes = input().split()
    healths = list(map(int, input().split()))
    geneTrie = buildGeneTrie(genes, healths)
    best = 0
    worst = float('inf')
    s = int(input())
    for i in range(s):
        first,last,d = input().split()
        first,last = int(first), int(last)
        score = checkDNA(geneTrie, d, first, last)
        best = max(best, score)
        worst = min(worst, score)
    print(worst, best)

if __name__ == '__main__':
    main()