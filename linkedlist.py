class JobNode:
    def __init__(self, title, skills):
        self.title = title
        self.skills = skills
        self.next = None


class JobLinkedList:
    """Singly linked list used to store job records."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_job(self, title, skills):
        new_node = JobNode(title, skills)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def display_jobs(self):
        temp = self.head
        if temp is None:
            print("\nNo Jobs Available")
            return
        count = 1
        while temp:
            print(f"{count}. {temp.title} | Skills: {', '.join(temp.skills)}")
            temp = temp.next
            count += 1

    def get_all_jobs(self):
        jobs = []
        temp = self.head
        while temp:
            jobs.append({"title": temp.title, "skills": temp.skills[:]})
            temp = temp.next
        return jobs

    def search_job(self, title):
        temp = self.head
        query = title.strip().lower()
        while temp:
            if temp.title.lower() == query:
                return {"title": temp.title, "skills": temp.skills[:]}
            temp = temp.next
        return None
