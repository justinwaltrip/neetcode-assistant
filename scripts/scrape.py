"""Scrape problems from NeetCode website."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import json
from tqdm import tqdm
from time import sleep

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

# wait for page to load
driver.implicitly_wait(5)

# get all tables
tables = driver.find_elements(By.TAG_NAME, "table")

problem_rows = []
for table in tables:
    # get all rows
    problem_rows.extend(table.find_elements(By.TAG_NAME, "tr")[1:])

if DATA_PATH.exists():
    problems = json.loads(DATA_PATH.read_text())
else:
    problems = []

for row in tqdm(problem_rows):
    # get problem name
    problem_col = row.find_element(By.TAG_NAME, "a")
    name = problem_col.text

    # skip if problem already exists
    if any(problem["name"] == name for problem in problems):
        continue

    # get problem page link
    page_link = problem_col.get_attribute("href")

    # go to problem page
    driver.get(page_link)

    # configure local storage
    driver.execute_script(
        "window.localStorage.setItem('dynamicIdeLayoutGuide', 'true');"
    )

    # wait for page to load
    driver.implicitly_wait(5)

    try:
        description = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[4]/div/div[1]/div[3]",
        ).text
    except Exception:
        # just wait a little longer
        sleep(3)
        description = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[4]/div/div[1]/div[3]",
        ).text

    # if description is empty, skip problem
    if not description:
        continue

    # go back to problems list
    driver.back()

    # get problem difficulty
    difficulty = row.find_element(By.CLASS_NAME, "diff-col").text

    # click on video solution
    video_solution_col = row.find_element(By.XPATH, "td[5]")
    button = video_solution_col.find_element(By.TAG_NAME, "button")
    try:
        button.click()
    except Exception:
        # wait for human to manually close the solution modal
        input("Press enter to continue...")
        button.click()

    # get video solution link
    for i in range(1, 20):
        video_link = driver.find_element(
            By.XPATH,
            (
                f"/html/body/app-root/app-pattern-table-list/div/div[2]/div[6]/app-table[{i}]/app-modal[2]/div/div[2]/header/h1/a"
                if i > 1
                else "/html/body/app-root/app-pattern-table-list/div/div[2]/div[6]/app-table/app-modal[2]/div/div[2]/header/h1/a"
            ),
        ).get_attribute("href")
        if video_link != "https://www.youtube.com/watch?v=":
            break

    # close video solution modal
    for i in range(2, 20):
        try:
            close_button = driver.find_element(
                By.XPATH,
                f"/html/body/app-root/app-pattern-table-list/div/div[2]/div[6]/app-table[{i}]/app-modal[2]/div/div[2]/footer/button",
            )
            if not close_button.is_displayed():
                continue
            close_button.click()
            break
        except Exception:
            pass

    # click on code solution
    code_solution_col = row.find_element(By.XPATH, "td[6]")
    button = code_solution_col.find_element(By.TAG_NAME, "button")
    try:
        button.click()
    except Exception:
        # wait for human to manually close the video solution modal
        input("Press enter to continue...")
        button.click()

    # get solution
    solution = driver.find_element(
        By.XPATH,
        "/html/body/app-root/app-pattern-table-list/div/div[2]/div[6]/app-table/app-modal[1]/div/div[2]/section/app-code/div/div/pre/code",
    ).text

    # close code solution modal
    for i in range(2, 20):
        try:
            close_button = driver.find_element(
                By.XPATH,
                f"/html/body/app-root/app-pattern-table-list/div/div[2]/div[6]/app-table[{i}]/app-modal[1]/div/div[2]/footer/button",
            )
            if not close_button.is_displayed():
                continue
            close_button.click()
            break
        except Exception:
            pass

    problems.append(
        {
            "name": name,
            "page_link": page_link,
            "description": description,
            "difficulty": difficulty,
            "video_link": video_link,
            "solution": solution,
        }
    )

    # save problems to file after each problem
    with open(DATA_PATH, "w") as f:
        json.dump(problems, f, indent=4)

driver.quit()
