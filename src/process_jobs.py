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

    # Replace job_url with actual HTML buttons
    jobs["apply"] = jobs["job_url"].apply(
        lambda url: f'<a href="{url}" target="_blank"><button style="background-color: #4CAF50; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">Apply</button></a>' 
        if pd.notna(url) else "N/A"
    )

    core_columns = ["title", "company", "location", "job_type", "apply", "days_since_posted"]
    md_table = jobs[core_columns].to_markdown(index=False)
    return md_table