from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import argparse

''' 
This is my backend program called ilmobotti. Ilmobotti is created in desire to be the number 1 rageilmooja in every event in prodekos ilmokilke.
The program can be used via CMD and be given three parameters: event countdown, desired event, and quota number. Ilmobotti uses Python's Selenium
library and chromedriver to navigate in ilmokilke.  ArgParse is used for taking commands from CMD.

'''


'''

This function effectively makes me able to run the program from command prompt in a way that I can give the program parameters.
--signup-countdown is the time in seconds to event sign-up; it can be as big as you need but I like to adjust it according to my needs.
--event argument is the event name copied straight from Prodeko event page.
--quota argument is the 'index' of the quota button from top to bottom starting from index 0.

Example CMD line:

C: FILE PATH> python ilmobotti.py --signup-countdown 200 --event "World Academic Kyykkä Championship 2025" --quota 0



'''
def parse_args():
    parser = argparse.ArgumentParser(description="Automate sign-up for events")
    parser.add_argument('--signup-countdown', type=int, help='Time until the signup time (In seconds).', default = 300)
    parser.add_argument('--event', type=str, help='Name of the event you want to be registered in.', required=True)
    parser.add_argument('--quota', type=int, help='Index of the quota button.', default=0)
    return parser.parse_args()


# This function sets up the webdriver that controls chrome.
def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get('https://ilmo.prodeko.org/en')
    return driver


# This function extracts events from the open signup page in ilmokilke. It returns a dictionary of the form  {Name : Link}

def extract_events(event_container):
    events = event_container.find_elements(By.TAG_NAME, 'a')
    event_dict = {}
    for event in events:
        name = event.text.strip()
        link = event.get_attribute('href')
        event_dict[name] = link
    return event_dict
            

# This function uses extract events function to find all open events. Could be merged.

def find_events(driver):
    try:
        event_container = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-cy="homepage-signup-open-events"]'))
        )
        events = extract_events(event_container)
    except Exception as e:
        print(f"Error: {e}")    
    
    return events


# This function returns the corresponding link for the event.

def choose_event(events: dict, event_name: str):
    desired_event_link = events[event_name]
    return desired_event_link


# This function finds the sign-up button on the event page and waits till it is visible.

def find_signup_button(driver, quota_index: int, time) :
    datacy = 'eventpage-quotas-link-' + str(quota_index)
    signup_button =WebDriverWait(driver, time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-cy="{datacy}"]')))
    return signup_button


# This function handles the sign-up process using given sign-up info. It can only handle general sign-up data like email, name and tg.
# Dietary restrictions and tickboxes out of scope for now.

def sign_up(driver, sign_up_info = {'firstName' : '', 'lastName' : '', 'email' : ''}):
    event_container = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'form'))
        )
    input_fields = event_container.find_elements(By.TAG_NAME, 'input')
    for element in input_fields:
        field = element.get_attribute('id')
        if field in sign_up_info.keys():
            element.send_keys(sign_up_info[field])


# Reads the parsed arguments and returns them as variables.
        
def read_cmd():
    args = parse_args()
    time = args.signup_countdown
    event = args.event
    quota_index = args.quota
    return time, event, quota_index

# Main loop that handles the sign-up process.

def main():
    driver = setup_driver()
    time, event_name, quota_index = read_cmd()

    #Finds all events on the current open sign up page. Returns a dictionary consisting of name : link pairs.
    events = find_events(driver)

    #User can input the desired event and function returns its link.
    desired_event_link = choose_event(events, event_name)

    #Driver navigates to the new page as per the link.
    driver.get(desired_event_link)

    #Funtion takes quota number, quotas are numbered from top to bottom, starting from index 0. Returns the sign-up button element.
    signup_button = find_signup_button(driver, quota_index, time)

    #Driver navigates to the page, to which the sign-up button leads.
    signup_button.click()

    #This function handles sign-up form filling. It leaves the event-specific queries for the user to fill.
    sign_up(driver)



    # Waits a predetermined amount of time. Can be changed depending on how much you need time to fill the form out.
    WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.ID, 'desired-element'))
    )


main()


''' Thank you for checking out my project <3'''
