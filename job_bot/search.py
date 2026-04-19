import requests, os

def search_jobs(query: str, num: int = 5) -> list[dict]:
    resp = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": os.getenv("SERPER_API_KEY")},
        json={"q": query, "num": num}
    )
    results = resp.json().get("organic", [])
    return [{"title": r["title"], "url": r["link"], "snippet": r["snippet"]} for r in results]