import re
import csv
from playwright.sync_api import Playwright, sync_playwright

# enter badgr email and password
login_email = ""
login_password = ""

# enter the name of the csv file you want to put the group links in
csv_name = "group_links.csv"

with sync_playwright() as playwright:
    # open new browser in headless mode, then open new context and page
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    # login using previously entered email and password
    page.goto("https://msowc.badgr.com/")
    page.goto("https://msowc.badgr.com/auth/login")
    page.get_by_label("Email *").click()
    page.get_by_label("Email *").fill(login_email)
    page.get_by_label("Enter Password *").click()
    page.get_by_label("Enter Password *").fill(login_password)
    page.get_by_role("button", name="Sign In").click()
    
    # navigate to groups page
    page.get_by_role("link", name="Issuers").click()
    page.get_by_role("link", name="View Online Workforce College").click()
    page.get_by_role("tab", name="Groups").click()
    
    # wait for groups page to load
    page.wait_for_timeout(60000) 
    # set results per page to 100 for faster execution
    page.get_by_label("Results Per Page").select_option("100")
    
    # initailize list to put links into
    link_list = []
    aria_label = page.locator('button[ngdatacy="pagination-next-button"]').get_attribute("aria-label")
    match = re.search(r'of\s*(\d+)', aria_label)
    if match:
        total_pages = int(match.group(1))
        print(f"Total pages: {total_pages}")
    
    
    # iterate through each page and get the group links
    for i in range(total_pages):
        # get the group links on the page
        links = page.get_by_role("link")
        
        # get the number of group links
        link_count = links.count()
        # iterate through each link
        for i in range(link_count):
            # get each link, strip it, and get the hyperlink associated with it
            link = links.nth(i)
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            
            # get just the hyperlinks leading to groups and not including the issuers group page
            if "/issuers/" not in href and "/groups/" in href:
                # add the necessary elements to make it lead to that groups editn page
                full_link = "https://msowc.badgr.com" + href + "/setup/edit"
                link_list.append(full_link)
                
        # find if there is a next button and if so, click it
        next_button = page.get_by_role("button", name=re.compile("Show next page:"))
        if next_button.is_visible():
            next_button.click()
        
    # output all the links to a csv file then close said csv file
    csvfile = csvfile = open(csv_name, 'w', newline='')
    writer = csv.writer(csvfile)
    for full_link in link_list:
        writer.writerow([full_link])
    csvfile.close
    
    # clean up by closing the context then the file
    context.close()
    browser.close()
