class SkillStack:
    """Stack used to maintain recently added skill history."""

    def __init__(self):
        self.stack = []

    def push(self, skill):
        self.stack.append(skill)

    def pop(self):
        if not self.stack:
            return None
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def display(self):
        if self.is_empty():
            print("\nNo Skill History")
            return
        print("\n===== SKILL HISTORY (STACK) =====")
        for i, skill in enumerate(reversed(self.stack), 1):
            print(f"{i}. {skill}")
