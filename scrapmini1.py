import requests
import pandas as pd

def fetch_remoteok_jobs():
    url = "https://remoteok.com/api"

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    jobs = []
    for item in data:
        # Skip metadata / non-job entries
        if not isinstance(item, dict) or "id" not in item:
            continue
        job = {
            "id": item.get("id"),
            "date": item.get("date"),
            "company": item.get("company"),
            "position": item.get("position"),
            "location": item.get("location"),
            "tags": ", ".join(item.get("tags", [])) if item.get("tags") else None,
            "url": item.get("url"),
            "salary": item.get("salary")
        }
        jobs.append(job)

    return jobs

if __name__ == "__main__":
    jobs_list = fetch_remoteok_jobs()
    if not jobs_list:
        print("No jobs fetched.")
    else:
        df = pd.DataFrame(jobs_list)
        # Make sure you have 'openpyxl' installed (or another Excel engine)
        output_path = "remoteok_jobs.xlsx"
        try:
            df.to_excel(output_path, index=False, engine='openpyxl')
            print(f"Saved {len(df)} job postings to {output_path}")
        except Exception as e:
            print("Error saving Excel file:", e)


