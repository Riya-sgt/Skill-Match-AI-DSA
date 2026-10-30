from collections import deque

class JobQueue:
    """FIFO queue for job applications."""

    def __init__(self):
        self.queue = deque()

    def enqueue(self, job):
        self.queue.append(job)

    def dequeue(self):
        if not self.queue:
            return None
        return self.queue.popleft()

    def display(self):
        if not self.queue:
            print("\nNo Jobs In Queue")
            return
        print("\n===== JOB APPLICATION QUEUE (FIFO) =====")
        for i, job in enumerate(self.queue, 1):
            print(f"{i}. {job}")

    def __len__(self):
        return len(self.queue)
