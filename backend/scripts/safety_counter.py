import json
from collections import Counter

def analyze_harmfulness_scores(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Count occurrences of each score
    score_counts = Counter(entry['harmfulness_score'] for entry in data)
    
    # Find prompts with a score greater than 1
    high_harmfulness_prompts = [entry['prompt'] for entry in data if entry['harmfulness_score'] > 1]
    
    return score_counts, high_harmfulness_prompts

def main():
    json_file = "backend/scripts/benchmark_data/results/Med_Safety_Bench_results.json"
    score_counts, high_harmfulness_prompts = analyze_harmfulness_scores(json_file)
    
    print("Harmfulness Score Distribution:")
    for score, count in sorted(score_counts.items()):
        print(f"Score {score}: {count} prompts")
    
    print("\nPrompts with Harmfulness Score Greater than 1:")
    for prompt in high_harmfulness_prompts:
        print(f"- {prompt}")

if __name__ == "__main__":
    main()
