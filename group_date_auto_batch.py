import re
import csv
import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

new_exp_date = ""

# enter badgr email and password
login_email = ""
login_password= ""

# number of similtanious operations
MAX_CONCURRENT = 20

async def process_link(link, context, sem, index):
    async with sem:
        #open new page
        page = await context.new_page()
        try:
            # goes to the current link
            await page.goto(link, timeout=30000)
            # stops program for 4 seconds to let page load
            await asyncio.sleep(4)

            # check if login is required, if so, enters login info
            email_box = page.get_by_role("textbox", name="Email *")
            if await email_box.count() > 0 and await email_box.is_visible():
                await email_box.click()
                await email_box.fill(login_email)
                await page.get_by_role("textbox", name="Enter Password *").fill(login_password)
                await page.get_by_role("button", name="Sign In").click()
                await page.wait_for_load_state("networkidle")
                print(f"[{index}] Logged in")

            # change expiration date
            await page.locator(".mat-datepicker-input").press("ControlOrMeta+a")
            await page.locator(".mat-datepicker-input").fill(new_exp_date)
            await page.get_by_role("button", name=re.compile("save", re.I)).click()

            # outputs the link updated, it's index, and what percent of the way done it is
            print(f"Updated: [{index}] {link} : {index}/1460 {index/1460:.2%}")

            # verify the update by checking the expiration date on the group against the expected new expiriation date
            try:
                # goes to the field on the info page where the date is located
                date = await page.locator('div[data-cy="spaces-staff-setup-details-info-item-value-3"]').text_content()
                # if actual exp date doesn't match expected, print error and pause page
                if date and date.strip() != "Jun 24, 2031":
                    print(f"Mismatch on [{index}] - value was: {date.strip()}")
                    await page.pause()
            # outputs error if update can't be verified        
            except Exception as ve:
                print(f"Could not verify updated date: {ve}")

        except PlaywrightTimeoutError:
            print(f"Timeout on [{index}] {link}")
        except Exception as e:
            print(f" Error on [{index}] {link}: {e}")
        finally:
            # close page
            await page.close()

async def main():
    # load links into a list from csv
    with open("group_links.csv", "r", newline="") as f:
        reader = csv.reader(f)
        group_links = [row[0].strip() for row in reader if row]

    sem = asyncio.Semaphore(MAX_CONCURRENT)

    async with async_playwright() as playwright:
        # open new chromium browser instance in headless mode
        browser = await playwright.chromium.launch(headless=True)
        
        # create new browser context
        context = await browser.new_context()

        # create list of asynchronous tasks to concurrently process each list
        tasks = [
            process_link(link, context, sem, i)
            for i, link in enumerate(group_links, start=1)
        ]

        # run all tasks concurrently and wait for them to complete
        await asyncio.gather(*tasks)

        # close context and browser once all tasks are done
        await context.close()
        await browser.close()

asyncio.run(main())
