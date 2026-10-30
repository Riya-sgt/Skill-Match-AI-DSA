from skill_utils import normalize_skill


class CourseRecommender:
    """Small offline course-title catalog for common skills."""

    def __init__(self):
        self.courses = {
            "python": "Python for Beginners",
            "java": "Java Programming Masterclass",
            "c++": "C++ Complete Guide",
            "machine learning": "Machine Learning A-Z",
            "sql": "SQL Bootcamp",
            "aws": "AWS Cloud Practitioner",
            "docker": "Docker Essentials",
            "linux": "Linux Administration",
            "networking": "Networking Fundamentals",
            "cybersecurity": "Cyber Security Basics",
            "javascript": "JavaScript Complete Course",
            "html": "HTML & CSS Web Development",
            "css": "Responsive Web Design",
            "excel": "Excel Data Analysis",
            "design": "UI/UX Design Fundamentals",
            "power bi": "Power BI Data Analytics",
            "statistics": "Statistics for Data Science",
            "excel": "Excel Skills for Business",
            "security": "Introduction to Cybersecurity",
            "testing": "Software Testing Fundamentals",
            "debugging": "Debugging and Problem Solving",
            "manual testing": "Manual Software Testing",
            "user experience": "UX Design Fundamentals",
            "user interface": "UI Design Basics",
            "product management": "Product Management Fundamentals",
            "project management": "Project Management Basics",
            "business analysis": "Business Analysis Foundations",
            "financial analysis": "Financial Analysis Essentials",
            "market research": "Market Research Fundamentals",
            "risk management": "Risk Management Foundations",
            "valuation": "Business Valuation Basics",
            "operations management": "Operations Management Foundations",
            "supply chain": "Supply Chain Management Basics",
            "team leadership": "Team Leadership Essentials",
            "sales management": "Sales Management Fundamentals",
            "marketing": "Digital Marketing Fundamentals",
            "relationship building": "Professional Communication and Relationship Skills",
            "customer service": "Customer Service Foundations",
            "problem-solving": "Critical Thinking and Problem Solving",
            "negotiation": "Negotiation Skills Fundamentals",
            "social media management": "Social Media Marketing",
            "content creation": "Content Strategy and Creation",
            "seo": "SEO Fundamentals",
            "financial planning": "Personal Financial Planning",
            "budgeting": "Budgeting Essentials",
            "human resources": "Human Resources Foundations",
            "recruitment": "Recruitment and Selection",
            "training": "Learning and Development Fundamentals",
        }

    def recommend_course(self, skill):
        key = normalize_skill(skill)
        return self.courses.get(key, "No Course Found")
