#!/usr/bin/env python3
"""
Main script to scrape jobs and update README.
"""
import os
import sys
from datetime import datetime

# Add src to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from get_jobs import get_jobs
from process_jobs import process_jobs


def update_readme(jobs_table: str):
    """Update README.md with the new jobs table."""
    readme_content = f"""# AI Job Scraper

This repository automatically scrapes AI internship and engineer positions from multiple job boards and updates this README with the latest opportunities.

## Latest Job Opportunities

*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*

{jobs_table}

## How it works

This project uses GitHub Actions to:
1. Scrape jobs from Indeed, LinkedIn, Glassdoor, Google, and Naukri
2. Filter for AI scientist/engineer internships near Paris, France  
3. Process and format the results
4. Update this README automatically

The scraping runs on a schedule and is powered by the [jobspy](https://github.com/Bunsly/JobSpy) library.
"""
    
    # Get the path to README.md (one level up from src/)
    readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("README.md updated successfully!")


def main():
    """Main function to orchestrate the job scraping and README update."""
    try:
        print("Starting job scraping...")
        jobs_df = get_jobs()
        
        if len(jobs_df) == 0:
            print("No jobs found. Skipping README update.")
            return
        
        print("Processing jobs...")
        jobs_table = process_jobs(jobs_df)
        
        print("Updating README...")
        update_readme(jobs_table)
        
        print("Process completed successfully!")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 