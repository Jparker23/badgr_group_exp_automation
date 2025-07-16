import re
import csv
import sys
from playwright.sync_api import Playwright, sync_playwright, TimeoutError as PlaywrightTimeoutError

# enter what experation date to set each group too
new_exp_date = ""

# enter badgr email and password
login_email = ""
login_password= ""

with sync_playwright() as playwright:
    # launch new browser in headless mode
    browser = playwright.chromium.launch(headless=False)
    
    # launch new context
    context = browser.new_context()
    
    #launch new page to load each link in
    page = context.new_page()
    
    # load group links from csv file into a list
    with open('group_links.csv', 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        group_links = [row[0] for row in reader if row]
    

    i=1

    # initialize first_time to detectnthe first run of the loop
    
    first_time = True
    
    # iterate through each link
    for row in group_links:
        # detect empty rows
        if not row:  
            continue
        
        # strip white space from link 
        link = row[0].strip()  
        try:
            # navigate to the link
            page.goto(link)
            
            # login only on the first link
            if first_time == True:
                # fill out login page and sign in to continue to the group editor
                page.get_by_role("textbox", name="Email *").click()
                page.get_by_role("textbox", name="Email *").fill("jparker1004@jcjc.edu")
                page.get_by_role("textbox", name="Enter Password *").click()
                page.get_by_role("textbox", name="Enter Password *").fill("JAPA9191#")
                page.get_by_role("button", name="Sign In").click()
                first_time = False

            # wait for date input field to appear and fill it with the new expiration date
            page.wait_for_selector(".mat-datepicker-input")
            page.locator(".mat-datepicker-input").press("ControlOrMeta+a")
            page.locator(".mat-datepicker-input").fill(new_exp_date)
            page.get_by_role("button", name=re.compile("save", re.I)).click()
        
            # output that the link was updated and what percent of the way through the links the program is
            print(f"Updated date on: [{i}] {link} : {i}/1460 {i/1460:.2%}")
            
            # get the updated experation date
            text = page.locator('div[data-cy="spaces-staff-setup-details-info-item-value-3"]').text_content()
            
            # check the actual group experation date against the expected updated date to make sure both match
            if text.strip() != "Jun 24, 2031":
                print("Paused")
                page.pause()
            
            i += 1
        
        # exit if a page takes more than 10 seconds to load link
        except PlaywrightTimeoutError:
            error_msg = f"Timeout on link {i}: {link}"
            print(f"{error_msg}")
            errors.append(error_msg)
            continue
        # exit if a link has different error
        except Exception as e:
            error_msg = f"Error on link {i}: {link} - {e}"
            print(f"{error_msg}")
            errors.append(error_msg)
            continue
        
    # clean up by closing browser and context
    context.close()
    browser.close()
