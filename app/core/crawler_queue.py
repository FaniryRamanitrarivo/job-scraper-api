from collections import deque

class CrawlerQueue:

    def __init__(self):
        self.queue = deque()
        self.seen = set()

    def push(self, url):

        if url in self.seen:
            return

        self.seen.add(url)
        self.queue.append(url)

    def pop(self):
        return self.queue.popleft()

    def empty(self):
        return not self.queue
