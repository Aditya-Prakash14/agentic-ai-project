import os
import time
from dotenv import load_dotenv
load_dotenv()

from search import search_jobs
from analyze import score_job
from draft import draft_cover_letter
from apply import apply_to_job

# Configuration
ENABLE_APPLY = os.getenv('ENABLE_APPLY', 'false').lower() == 'true'
AUTO_APPLY = os.getenv('AUTO_APPLY', 'false').lower() == 'true'  # If true, no confirmation prompts

def run(query: str):
    resume = open("resume.txt").read()

    print(f"\n🔍 Searching: {query}\n")
    jobs = search_jobs(query, num=5)

    for job in jobs:
        print(f"📋 {job['title']}")
        print(f"   {job['url']}")

        analysis = score_job(job, resume)
        score = analysis.get("fit_score", 0)
        print(f"   Fit score: {score}/100")

        if analysis.get("proceed"):
            print(f"   ✅ Good match — drafting cover letter...")
            letter = draft_cover_letter(job, resume, analysis)
            
            # Save to file
            safe_title = job['title'][:40].replace(" ", "_").replace("/", "-")
            filename = f"output_{safe_title}.txt"
            with open(filename, "w") as f:
                f.write(f"Job: {job['title']}\n")
                f.write(f"URL: {job['url']}\n")
                f.write(f"Fit Score: {score}/100\n")
                f.write(f"Strengths: {', '.join(analysis.get('strengths', []))}\n")
                f.write(f"Gaps: {', '.join(analysis.get('gaps', []))}\n\n")
                f.write("--- COVER LETTER ---\n\n")
                f.write(letter)
            print(f"   💾 Saved to {filename}")
            
            # Stage 4: Apply (optional)
            if ENABLE_APPLY:
                apply_prompt = "Submit application now? (y/n): " if not AUTO_APPLY else ""
                if AUTO_APPLY or (apply_prompt and input(apply_prompt).lower() == 'y'):
                    print(f"   📤 Submitting application...")
                    success = apply_to_job(job['url'], letter)
                    if success:
                        print(f"   ✅ Application submitted!")
                    else:
                        print(f"   ⚠️  Application submission failed - may require manual action")
        else:
            print(f"   ⏭️  Low fit ({score}) — skipping")
        print()

if __name__ == "__main__":
    # Load and process all queries from queries.txt
    try:
        with open("queries.txt", "r") as f:
            queries = [line.strip() for line in f if line.strip()]
        
        print(f"📋 Loaded {len(queries)} search queries\n")
        
        for i, query in enumerate(queries, 1):
            print(f"[{i}/{len(queries)}] Processing query: {query}")
            run(query)
            time.sleep(1)  # Rate limiting between queries
        
        print("\n✅ All queries processed!")
    except FileNotFoundError:
        print("❌ queries.txt not found. Please create it with one search query per line.")
        # Fallback to single query if file doesn't exist
        run("software engineer internship 2025 India")