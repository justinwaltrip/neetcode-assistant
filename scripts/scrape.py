"""Scrape problems from NeetCode website."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import json
from tqdm import tqdm

BASE_URL = "https://neetcode.io/practice"
DATA_PATH = Path("data/raw/problems.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

driver = webdriver.Chrome()
driver.get(BASE_URL)

# navigate to the NeetCode 150 page
neetcode_150_tab = driver.find_element(
    By.XPATH, "/html/body/app-root/app-pattern-table-list/div/div[2]/div[3]/ul/li[3]/a"
)
neetcode_150_tab.click()

# ensure list view
list_view_button = driver.find_element(
    By.XPATH,
    "/html/body/app-root/app-pattern-table-list/div/div[2]/div[5]/div/button[1]",
)
list_view_button.click()

# get problems table
table = driver.find_element(
    By.XPATH,
    "/html/body/app-root/app-pattern-table-list/div/div[2]/div[6]/app-table/div/table",
)

# get all rows
rows = table.find_elements(By.TAG_NAME, "tr")

problem_rows = rows[1:]

problems = {}
for row in tqdm(problem_rows):
    # get problem name
    name = row.find_element(By.TAG_NAME, "a").text

    # get problem difficulty
    diff_col = row.find_element(By.CLASS_NAME, "diff-col")
    difficulty = diff_col.text

    # click on video solution
    video_solution_col = row.find_element(By.XPATH, "td[5]")
    button = video_solution_col.find_element(By.TAG_NAME, "button")
    button.click()

    # get video solution link
    video_link = driver.find_element(
        By.XPATH,
        "/html/body/app-root/app-pattern-table-list/div/div[2]/div[6]/app-table/app-modal[2]/div/div[2]/header/h1/a",
    ).get_attribute("href")

    # close video solution modal
    close_button = driver.find_element(
        By.XPATH,
        "/html/body/app-root/app-pattern-table-list/div/div[2]/div[6]/app-table/app-modal[2]/div/div[2]/footer/button",
    )
    close_button.click()

    problems.append(
        {
            "name": name,
            "difficulty": difficulty,
            "video_link": video_link,
        }
    )

# save problems to file
with open(DATA_PATH, "w") as f:
    json.dump(problems, f, indent=4)

driver.quit()
