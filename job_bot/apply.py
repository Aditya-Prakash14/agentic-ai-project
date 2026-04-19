"""
Stage 4: Automated job application submission via Playwright
This module handles filling out and submitting Easy Apply forms on LinkedIn and other platforms.

⚠️ WARNING: Use responsibly. Always review the cover letter before submission.
Terms of Service may prohibit automated submission. User assumes all risks.
"""

from playwright.sync_api import sync_playwright, expect
import time
import logging

logger = logging.getLogger(__name__)

def apply_to_job(job_url: str, cover_letter: str, candidate_name: str = None, candidate_email: str = None) -> bool:
    """
    Attempt to apply to a job using Playwright browser automation.
    
    Args:
        job_url: URL of the job posting
        cover_letter: Cover letter text to submit
        candidate_name: Name for form submission
        candidate_email: Email for form submission
    
    Returns:
        bool: True if submission successful, False otherwise
    """
    
    try:
        with sync_playwright() as p:
            # Launch browser (visible for debugging)
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            logger.info(f"Opening job URL: {job_url}")
            page.goto(job_url, wait_until="networkidle")
            time.sleep(2)
            
            # Look for "Easy Apply" button
            easy_apply_btn = page.query_selector("[aria-label*='Easy Apply'], [data-test-react-button-primary][aria-label*='Apply']")
            
            if not easy_apply_btn:
                logger.warning("Easy Apply button not found. Job may require manual application.")
                browser.close()
                return False
            
            logger.info("Found Easy Apply button, clicking...")
            page.click("[aria-label*='Easy Apply'], [data-test-react-button-primary][aria-label*='Apply']")
            time.sleep(1)
            
            # Fill form fields
            # Note: LinkedIn form structure varies; this is a template
            
            # Look for text areas for cover letter
            text_areas = page.query_selector_all("textarea")
            for ta in text_areas:
                placeholder = ta.get_attribute("placeholder") or ""
                label = ta.get_attribute("aria-label") or ""
                
                if any(word in placeholder.lower() or word in label.lower() 
                       for word in ["cover", "letter", "message", "additional"]):
                    logger.info("Found cover letter field, filling...")
                    ta.click()
                    ta.fill(cover_letter)
                    time.sleep(0.5)
            
            # Look for submit button
            submit_btn = page.query_selector("[data-test-react-button-primary], button:has-text('Submit'), button:has-text('Apply')")
            
            if submit_btn:
                logger.info("Found submit button, submitting application...")
                submit_btn.click()
                time.sleep(2)
                
                # Check for success message
                success = page.query_selector("[data-test-modal-header]:has-text('Application sent')")
                if success:
                    logger.info("✅ Application submitted successfully!")
                    browser.close()
                    return True
            
            logger.warning("Could not submit application. Form may have changed.")
            browser.close()
            return False
    
    except Exception as e:
        logger.error(f"Error during application submission: {e}")
        return False


def batch_apply(job_data: list, interactive: bool = True) -> dict:
    """
    Apply to multiple jobs with user confirmation.
    
    Args:
        job_data: List of dicts with 'url', 'title', 'cover_letter'
        interactive: If True, ask user before each application
    
    Returns:
        dict: Summary of applications submitted
    """
    results = {
        'submitted': 0,
        'skipped': 0,
        'failed': 0,
        'details': []
    }
    
    for i, job in enumerate(job_data, 1):
        title = job.get('title', 'Unknown')
        url = job.get('url', '')
        cover_letter = job.get('cover_letter', '')
        
        print(f"\n[{i}/{len(job_data)}] {title}")
        print(f"URL: {url}")
        
        if interactive:
            response = input("Apply to this job? (y/n/skip): ").strip().lower()
            if response == 'skip':
                results['skipped'] += 1
                results['details'].append({'title': title, 'status': 'skipped'})
                continue
            elif response != 'y':
                results['skipped'] += 1
                results['details'].append({'title': title, 'status': 'declined'})
                continue
        
        # Attempt application
        success = apply_to_job(url, cover_letter)
        
        if success:
            results['submitted'] += 1
            results['details'].append({'title': title, 'status': 'submitted'})
            print(f"✅ Applied to {title}")
        else:
            results['failed'] += 1
            results['details'].append({'title': title, 'status': 'failed'})
            print(f"❌ Failed to apply to {title}")
        
        # Rate limiting
        time.sleep(3)
    
    return results
