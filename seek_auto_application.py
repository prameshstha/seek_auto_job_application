from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Initializing the webdriver
path = "A:/python/Data20%Science/project/chromedriver.exe"
chrome_service = Service(path)
options = webdriver.ChromeOptions()
# options.add_argument("--incognito")
# Uncomment the line below if you'd like to scrape without a new Chrome window every time.
# options.add_argument('headless')

# Change the path to where chromedriver is in your home folder.
driver = webdriver.Chrome(service=chrome_service, options=options)
# driver.set_window_size(1120, 1000)
driver.maximize_window()
url = 'https://www.seek.com.au/jobs-in-information-communication-technology/in-All-Melbourne-VIC?sortmode=ListedDate' \
      '&subclassification=6287%2C6290%2C6302%2C6301%2C6286 '
driver.get(url)

jobs = []
job_desc_check = ['python', 'django', 'css', 'frontend', 'backend', 'software developer', 'react', 'javascript',
                  'sql', 'aws', 'flutter', 'dart', 'software engineer', 'fullstack', 'html',
                  'git', 'ci/cd', 'database', 'selenium', 'rest', 'reactjs', 'front-end', 'back-end']
job_desc_not = ['angular', 'ios', 'vue.js', 'wordpress', 'magento', 'oracle', ]

job_position = ['software developer', 'graduate', 'flutter', 'back end', 'backend', 'frontend', 'frond end',
                'web developer', 'software engineer', 'front end developer', 'entry level software developer',
                'java developer', 'entry level software engineer', 'junior web developer', 'sql developer',
                'junior developer', 'entry level web developer', 'python developer', 'programmer', 'data engineer',
                'front end web developer', 'entry level developer', 'computer programmer', 'full stack developer',
                'junior software developer', 'junior front end developer', 'new grad software engineer',
                'react developer', 'aws solutions architect', 'jr developer', 'javascript developer', 'javascript',
                'python', 'junior software engineer', 'entry level programmer', 'software', 'developer', 'entry',
                'graduate', 'data analyst', 'data sci']
no_job = ['lead', 'senior', 'mobile', 'angular', 'manager', 'trainee', 'support', 'head', 'salesforce', 'security',
          'citizenship', '.net', 'net', 'php', 'bi developer', 'embedded', 'java', 'servicenow', 'native', 'mulesoft',
          'oracle', 'snr', 'delphi', 'account', '365', 'drupal', 'sharepoint', 'platform', 'analyst', 'etl', 'analyt',
          'fiori', 'informatica', 'ios developer']


def get_cover_letter(applying_position):
    return 'Cover letter'


def search_and_apply(page):

    url_list = []
    print('funciton called')
    max_page = page + 10
    if page > 7:
        driver.get(f'https://www.seek.com.au/jobs-in-information-communication-technology/in-All-Melbourne-VIC?page={page}&sortmode=ListedDate&subclassification=6287%2C6290%2C6302%2C6301%2C6286')
 
    while page < max_page:
        print('page number', page)

        job_details = driver.find_elements(By.CSS_SELECTOR, 'article[data-automation="normalJob"]')
        # current_url = driver.current_url
        for job in job_details:
            try:
                job_title = job.find_element(By.CSS_SELECTOR, 'a[data-automation="jobTitle"]').text
                job_title_button = job.find_element(By.CSS_SELECTOR, 'a[data-automation="jobTitle"]')
                try:
                    # applied_job = driver.find_element(By.CSS_SELECTOR, 'div[data-automation="applied-job"]')
                    applied_job = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/section/div[2]/div/div[2]/div[1]/div/div/div[1]/div[3]/div/article/div[3]/div[2]/div/div/div/div/div[2]')
                    print('applied job found for ', job_title)
                except Exception as error:
                    print('applied-job not found')
                    if any(s in job_title.lower() for s in job_position) and not any(
                            n in job_title.lower() for n in no_job):
                        # print('yes job is here', job_title)
                        cover_letter = get_cover_letter(job_title)
                        job_title_button.send_keys(Keys.CONTROL + Keys.ENTER)  # to open link in new tab
                        driver.switch_to.window(driver.window_handles[1])  # to switch to recently opened tab
                        try:
                            try:
                                time.sleep(5)
                                aplied_status = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="job-status-badge"]')
                            except:
                                apply_button = driver.find_element(By.CSS_SELECTOR, 'a[data-automation="job-detail-apply"]')
                                target_attribute = apply_button.get_attribute('target')
                                print('apply button found-----------------------', target_attribute)
                                if target_attribute == '_self':
                                    job_description = driver.find_element(By.CSS_SELECTOR,
                                                                          'div[data-automation="jobAdDetails"]').text
                                    if any(desc in job_description.lower() for desc in job_desc_check):
                                        apply_button.click()
                                        time.sleep(5)
                                        # driver.find_element(By.ID, 'coverLetter_2').click()
                                        cover_letter_text_area = driver.find_element(By.XPATH,
                                                                                     '/html/body/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div/fieldset/div/div[3]/div/div[2]/div/div/textarea')
                                        cover_letter_text_area.click()
                                        time.sleep(2)
                                        cover_letter_text_area.clear()
                                        time.sleep(2)
                                        cover_letter_text_area.send_keys(cover_letter)
                                        time.sleep(2)
                                        # continue_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/div/div[1]/div/div[3]/div/div/div/button')
                                        # first continue button -- choose resume and cover letter
                                        continue_btn = driver.find_element(By.CSS_SELECTOR,
                                                                           'button[data-testid="continue-button"]')
                                        continue_btn.click()
                                        time.sleep(5)
                                        # second continue button
                                        current_url = driver.current_url
                                        if 'role-requirements' in current_url:
                                            try:
                                                question_btn = driver.find_element(By.CSS_SELECTOR,
                                                                                   'button[data-testid="continue-button"]')
                                                time.sleep(5)
                                                question_btn.click()
                                                time.sleep(1)
                                                new_url = driver.current_url
                                                if new_url == current_url:
                                                    url_list.append({'job_url': current_url})
                                            except Exception as e:
                                                print('no role-requirements button ')
                                        cont_btn = driver.find_element(By.CSS_SELECTOR,
                                                                       'button[data-testid="continue-button"]')
                                        cont_btn.click()
                                        time.sleep(5)
                                        submit_btn = driver.find_element(By.CSS_SELECTOR,
                                                                         'button[data-testid="review-submit-application"]')
                                        submit_btn.click()
                                        time.sleep(2)
                                else:
                                    apply_url = driver.current_url
                                    url_list.append({'job_url': apply_url})

                        except Exception as error:
                            print('apply_button not found')
                        time.sleep(2)
                        driver.close()
                        driver.switch_to.window(driver.window_handles[-1])  # focus the old tab element
                        time.sleep(2)
                    else:
                        print('no job', job_title)

            except Exception as e:
                print('error getting elements inside job', e)
                time.sleep(4)
        page += 1
        next_button = driver.find_element(By.CSS_SELECTOR, f'a[data-automation="page-{page}"]')
        next_button.click()
        print(url_list)
        time.sleep(10)
    return url_list


try:
    sign_in_button = driver.find_element(By.CSS_SELECTOR, 'a[data-automation="sign in"]')
    sign_in_button.click()
    time.sleep(5)
    email_text = driver.find_element(By.ID, 'emailAddress')
    password_text = driver.find_element(By.ID, 'password')
    auth_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    email_text.send_keys('your@email.com')
    password_text.send_keys('password.com')
    auth_button.click()
    time.sleep(1)

    job_url_list = search_and_apply(page=10)
    try:
        df_job = pd.read_csv('seek_self_apply.csv')
        jugs = []
        for a in job_url_list:
            if a['job_url'] in df_job['job_url'].values:
                print('it is here')
            else:
                print('not here')
                jugs.append({'job_url': a['job_url']})
        df_jugs = pd.DataFrame(jugs)
        df_out = df_job.drop(['Unnamed: 0'], axis=1)
        df3 = pd.concat([df_out, df_jugs], axis=0)
        dfg = pd.DataFrame(df3)
        dfg.to_csv('seek_self_apply.csv', index=False)
    except Exception as error:
        print('csv not found', error)
        df = pd.DataFrame(job_url_list)
        df.to_csv('seek_self_apply.csv')

    # time.sleep(2000)

except Exception as e:
    print('No sign in', e)
