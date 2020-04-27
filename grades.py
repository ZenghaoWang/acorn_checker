from selenium.webdriver import Chrome, ChromeOptions

USERNAME = 'wangzen6'
PASSWORD = 'DaddyDwight69'

options = ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=3')
browser = Chrome(options=options)
browser.get('https://acorn.utoronto.ca')

# Logging in
username_input = browser.find_element_by_id('username')
password_input = browser.find_element_by_id('password')
login_button = browser.find_elements_by_name('_eventId_proceed')[0]

username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
login_button.click()

# Printing winter session marks
browser.get('https://acorn.utoronto.ca/sws/#/history/academic')
course_table = browser.find_element_by_xpath(
    '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/history-academic/div/div[2]/div/div[4]/table/tbody/tr/td/table/tbody')
for row in course_table.find_elements_by_class_name('courses'):
    cols = row.find_elements_by_tag_name('td')
    print(f'{cols[0].text}: {cols[3].text}')

browser.close()
