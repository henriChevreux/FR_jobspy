from jobspy import scrape_jobs

def get_jobs():
    """
    Get jobs from the web.
    """
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "glassdoor", "google", "naukri"],
        search_term='AI (scientist OR engineer) intern -India -Senior',
        google_search_term="AI engineer internship jobs in France since last month",
        location="France",
        results_wanted=100,
        hours_old=730,
        country_indeed='France'
    )
    print(f"Found {len(jobs)} jobs")
    return jobs