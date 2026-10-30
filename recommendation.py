class RecommendationEngine:
    def recommend(self, results, limit=5):
        valid = [item for item in results if item["score"] > 0]
        sorted_results = sorted(
            valid,
            key=lambda item: (-item["score"], item["title"].lower())
        )
        return sorted_results[:limit]
