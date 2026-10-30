class ChartGenerator:
    def generate_chart(self, results, filename="skill_chart.png"):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("\nMatplotlib is not installed. Run: pip install matplotlib")
            return None

        if not results:
            print("\nNo results available for chart.")
            return None

        names = [item["title"] for item in results]
        scores = [item["score"] for item in results]

        plt.figure(figsize=(11, 6))
        plt.bar(names, scores)
        plt.title("Skill Match Analysis")
        plt.xlabel("Job Roles")
        plt.ylabel("Match Percentage")
        plt.xticks(rotation=60, ha="right")
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.show()
        print(f"\nChart saved as: {filename}")
        return filename

    def show_dashboard(self, results):
        if not results:
            print("\nNo data available for dashboard.")
            return

        scores = [item["score"] for item in results]
        avg = sum(scores) / len(scores)
        best = max(results, key=lambda x: x["score"])

        print("\n===== STATISTICS DASHBOARD =====")
        print("Total Job Roles :", len(results))
        print("Average Match   :", round(avg, 2), "%")
        print("Highest Match   :", best["title"], "->", best["score"], "%")
        print("Jobs with Match :", sum(1 for s in scores if s > 0))
