import pandas as pd

def process_jobs(jobs: pd.DataFrame) -> str:
    """
    Process jobs.
    """
    # Calculate days since posted
    jobs = jobs.copy()
    jobs["days_since_posted"] = (pd.Timestamp.now() - pd.to_datetime(jobs["date_posted"])).dt.days
    # nan means 0 days
    jobs["days_since_posted"] = jobs["days_since_posted"].fillna(0).astype(int)

    # Filter for internship jobs only (case insensitive)
    internship_mask = jobs["title"].str.contains("intern|stage|stagiaire", case=False, na=False, regex=True)
    jobs = jobs[internship_mask]

    # Remove duplicate jobs with same title and company (case insensitive)
    jobs["title_lower"] = jobs["title"].str.lower()
    jobs["company_lower"] = jobs["company"].str.lower()
    jobs = jobs.drop_duplicates(subset=["title_lower", "company_lower"], keep="first")
    jobs = jobs.drop(columns=["title_lower", "company_lower"])

    # Replace job_url with GitHub-compatible button badges
    jobs["apply"] = jobs["job_url"].apply(
        lambda url: f'[![Apply](https://img.shields.io/badge/Apply-brightgreen)]({url})' 
        if pd.notna(url) else "N/A"
    )

    # Sort by days_since_posted with most recent first (ascending order)
    jobs = jobs.sort_values("days_since_posted", ascending=True)

    core_columns = ["title", "company", "location", "job_type", "apply", "days_since_posted"]
    md_table = jobs[core_columns].to_markdown(index=False)
    return md_table