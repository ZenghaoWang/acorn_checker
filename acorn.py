
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from rich.console import Console
from rich.table import Column, Table
from rich import print
from rich.progress import track

MARKS_URL: str = 'https://acorn.utoronto.ca/sws/#/history/academic'

FALL_MARKS_XPATH = '//*[@id="main-content"]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[3]/table/tbody/tr[2]/td/table/tbody'
WINTER_MARKS_XPATH = '//*[@id="main-content"]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[4]/table/tbody/tr[2]/td/table/tbody'
SUMMER_MARKS_XPATH = '//*[@id="main-content"]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[5]/table/tbody/tr/td/table/tbody'


def print_grades_helper(web_table, title: str) -> None:
    """Formats and prints a table.

    Args:
        web_table (WebElement): html table
    """
    console = Console()

    table = Table(show_header=True, header_style="blue", title=title)
    table.add_column("Course", style="dim")
    table.add_column("Mark")
    table.add_column("Grade")
    table.add_column("Credits")

    courses = web_table.find_elements_by_class_name('courses')
    for row in courses:
        cols = row.find_elements_by_tag_name('td')

        course, credit = cols[0].text, cols[2].text
        mark = cols[3].text if cols[3].text else "N/A"
        grade = "[red]IPR[/red]" if cols[4].text == "IPR" else f"[green]{cols[4].text}[/green]"

        table.add_row(course, mark, grade, credit)

    console.print(table)


def print_grades(browser: Chrome, fall: bool = False, winter: bool = False, summer: bool = False) -> None:
    print("[cyan]Getting grades[/cyan]...")
    browser.get(MARKS_URL)
    try:
        if fall:
            fall_table = browser.find_element_by_xpath(FALL_MARKS_XPATH)
            print_grades_helper(fall_table, "Fall Semester Grades")

        if winter:
            winter_table = browser.find_element_by_xpath(WINTER_MARKS_XPATH)
            print_grades_helper(winter_table, "Winter Semester Grades")

        if summer:
            summer_table = browser.find_element_by_xpath(SUMMER_MARKS_XPATH)
            print_grades_helper(summer_table, "Summer Semester Grades")

    except NoSuchElementException:
        print("An error occured. Please try again.")
        exit()
