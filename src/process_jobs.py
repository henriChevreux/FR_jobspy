import pandas as pd
import re

def get_company_logo_url(company_name: str) -> str:
    """
    Generate a company logo URL using Clearbit's Logo API.
    Falls back to a default image if company name is invalid.
    """
    if pd.isna(company_name) or not company_name.strip():
        return "https://via.placeholder.com/32x32?text=?"
    
    # Clean company name: remove common suffixes and special characters
    clean_name = re.sub(r'\b(Inc|LLC|Ltd|Corporation|Corp|Company|Co|Group|SA|SAS|SARL)\b', '', company_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'[^\w\s]', '', clean_name).strip()
    
    # Convert to domain-like format
    domain = clean_name.lower().replace(' ', '')
    
    if not domain:
        return "https://via.placeholder.com/32x32?text=?"
    
    # Use Clearbit Logo API - falls back gracefully if logo not found
    return f"https://logo.clearbit.com/{domain}.com"

def process_jobs(jobs: pd.DataFrame) -> str:
    """
    Process jobs.
    """
    # Calculate days since posted
    jobs = jobs.copy()
    jobs["age (d)"] = (pd.Timestamp.now() - pd.to_datetime(jobs["date_posted"])).dt.days
    # nan means 0 days
    jobs["age (d)"] = jobs["age (d)"].fillna(0).astype(int)

    # Filter for internship jobs only (case insensitive)
    internship_mask = jobs["title"].str.contains("intern|stage|stagiaire", case=False, na=False, regex=True)
    jobs = jobs[internship_mask]

    # Remove duplicate jobs with same title and company (case insensitive)
    jobs["title_lower"] = jobs["title"].str.lower()
    jobs["company_lower"] = jobs["company"].str.lower()
    jobs = jobs.drop_duplicates(subset=["title_lower", "company_lower"], keep="first")
    jobs = jobs.drop(columns=["title_lower", "company_lower"])

    # Add company logos
    jobs["logo"] = jobs["company"].apply(lambda company: f'<img src="{get_company_logo_url(company)}" width="32" height="32" alt="{company} logo">')

    # Replace job_url with GitHub-compatible button badges
    jobs["apply"] = jobs["job_url"].apply(
        lambda url: f'[![Apply](https://img.shields.io/badge/Apply-brightgreen)]({url})' 
        if pd.notna(url) else "N/A"
    )

    # Sort by days_since_posted with most recent first (ascending order)
    jobs = jobs.sort_values("age (d)", ascending=True)

    core_columns = ["logo", "title", "company", "location", "job_type", "apply", "age (d)"]
    md_table = jobs[core_columns].to_markdown(index=False, tablefmt="pipe")
    return md_table