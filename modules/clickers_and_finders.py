'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

version:    24.12.29.12.30
'''

from config.settings import click_gap, smooth_scroll
from modules.helpers import buffer, print_lg, sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

# Click Functions
def wait_span_click(driver: WebDriver, text: str, time: float=5.0, click: bool=True, scroll: bool=True, scrollTop: bool=False) -> WebElement | bool:
    '''
    Finds the span element with the given `text`.
    - Returns `WebElement` if found, else `False` if not found.
    - Clicks on it if `click = True`.
    - Will spend a max of `time` seconds in searching for each element.
    - Will scroll to the element if `scroll = True`.
    - Will scroll to the top if `scrollTop = True`.
    '''
    if text:
        try:
            button = WebDriverWait(driver,time).until(EC.presence_of_element_located((By.XPATH, './/span[normalize-space(.)="'+text+'"]')))
            if scroll:  scroll_to_view(driver, button, scrollTop)
            if click:
                button.click()
                buffer(click_gap)
            return button
        except Exception as e:
            print_lg("Click Failed! Didn't find '"+text+"'")
            # print_lg(e)
            return False

def multi_sel(driver: WebDriver, texts: list, time: float=5.0) -> None:
    '''
    - For each text in the `texts`, tries to find and click `span` element with that text.
    - Will spend a max of `time` seconds in searching for each element.
    '''
    for text in texts:
        ##> ------ Dheeraj Deshwal : dheeraj20194@iiitd.ac.in/dheerajdeshwal9811@gmail.com - Bug fix ------
        wait_span_click(driver, text, time, False)
        ##<
        try:
            button = WebDriverWait(driver,time).until(EC.presence_of_element_located((By.XPATH, './/span[normalize-space(.)="'+text+'"]')))
            scroll_to_view(driver, button)
            button.click()
            buffer(click_gap)
        except Exception as e:
            print_lg("Click Failed! Didn't find '"+text+"'")
            # print_lg(e)

def multi_sel_noWait(driver: WebDriver, texts: list, actions: ActionChains = None) -> None:
    '''
    - For each text in the `texts`, tries to find and click `span` element with that class.
    - If `actions` is provided, bot tries to search and Add the `text` to this filters list section.
    - Won't wait to search for each element, assumes that element is rendered.
    '''
    for text in texts:
        try:
            button = driver.find_element(By.XPATH, './/span[normalize-space(.)="'+text+'"]')
            scroll_to_view(driver, button)
            button.click()
            buffer(click_gap)
        except Exception as e:
            if actions: company_search_click(driver,actions,text)
            else:   print_lg("Click Failed! Didn't find '"+text+"'")
            # print_lg(e)

def boolean_button_click(driver: WebDriver, actions: ActionChains, text: str) -> None:
    '''
    Tries to click on the boolean button with the given `text` text.
    '''
    try:
        list_container = driver.find_element(By.XPATH, './/h3[normalize-space()="'+text+'"]/ancestor::fieldset')
        button = list_container.find_element(By.XPATH, './/input[@role="switch"]')
        scroll_to_view(driver, button)
        actions.move_to_element(button).click().perform()
        buffer(click_gap)
    except Exception as e:
        print_lg("Click Failed! Didn't find '"+text+"'")
        # print_lg(e)

# Find functions
def find_by_class(driver: WebDriver, class_name: str, time: float=5.0) -> WebElement | Exception:
    '''
    Waits for a max of `time` seconds for element to be found, and returns `WebElement` if found, else `Exception` if not found.
    '''
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

# Scroll functions
def scroll_to_view(
    driver: WebDriver,
    element: WebElement,
    top: bool = False,
    smooth_scroll: bool = smooth_scroll,
    offset: int = 0,
) -> None:
    '''
    Scrolls the `element` into view and adjusts for sticky headers.
    - `smooth_scroll` will scroll with smooth behavior.
    - `top` will scroll the element to the top of the view.
    - `offset` nudges the scroll position upward by given pixels.
    '''
    if top:
        driver.execute_script('arguments[0].scrollIntoView();', element)
    else:
        behavior = "smooth" if smooth_scroll else "instant"
        driver.execute_script('arguments[0].scrollIntoView({block: "center", behavior: "'+behavior+'" });', element)
    if offset:
        driver.execute_script(f'window.scrollBy(0, -{offset});')
    return None

##> ------ OpenAI : codex - Feature ------
def click_element(driver: WebDriver, by: By, locator: str, timeout: int = 5) -> WebElement:
    '''
    Waits for an element to be clickable and clicks it.
    Falls back to JavaScript click on failure.
    '''
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator)))
    try:
        element.click()
    except Exception:
        driver.execute_script('arguments[0].click();', element)
    return element
##<

# Enter input text functions
def text_input_by_ID(driver: WebDriver, id: str, value: str, time: float=5.0) -> None | Exception:
    '''
    Enters `value` into the input field with the given `id` if found, else throws NotFoundException.
    - `time` is the max time to wait for the element to be found.
    '''
    username_field = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, id)))
    username_field.send_keys(Keys.CONTROL + "a")
    username_field.send_keys(value)

def try_xp(driver: WebDriver, xpath: str, click: bool=True) -> WebElement | bool:
    try:
        if click:
            driver.find_element(By.XPATH, xpath).click()
            return True
        else:
            return driver.find_element(By.XPATH, xpath)
    except: return False

def try_linkText(driver: WebDriver, linkText: str) -> WebElement | bool:
    try:    return driver.find_element(By.LINK_TEXT, linkText)
    except:  return False

def try_find_by_classes(driver: WebDriver, classes: list[str]) -> WebElement | ValueError:
    for cla in classes:
        try:    return driver.find_element(By.CLASS_NAME, cla)
        except: pass
    raise ValueError("Failed to find an element with given classes")

def company_search_click(driver: WebDriver, actions: ActionChains, companyName: str) -> None:
    '''
    Tries to search and Add the company to company filters list.
    '''
    wait_span_click(driver,"Add a company",1)
    search = driver.find_element(By.XPATH,"(.//input[@placeholder='Add a company'])[1]")
    search.send_keys(Keys.CONTROL + "a")
    search.send_keys(companyName)
    buffer(3)
    actions.send_keys(Keys.DOWN).perform()
    actions.send_keys(Keys.ENTER).perform()
    print_lg(f'Tried searching and adding "{companyName}"')

def text_input(actions: ActionChains, textInputEle: WebElement | bool, value: str, textFieldName: str = "Text") -> None | Exception:
    if textInputEle:
        sleep(1)
        # actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        textInputEle.clear()
        textInputEle.send_keys(value.strip())
        sleep(2)
        actions.send_keys(Keys.ENTER).perform()
    else:
        print_lg(f'{textFieldName} input was not given!')

# Utility to locate the Easy Apply button even if LinkedIn updates the
# underlying HTML structure. Tries multiple XPath selectors and
# returns the first match or ``False`` if none are found.
def find_easy_apply_button(driver: WebDriver) -> WebElement | bool:
    xpaths = [
        ".//button[contains(@class,'jobs-apply-button') and contains(@class, 'artdeco-button--3') and contains(@aria-label, 'Easy')]",
        ".//button[contains(@id,'jobs-apply-button') and contains(@aria-label, 'Easy')]",
        ".//button[@data-live-test-job-apply-button]",
        ".//button[contains(., 'Easy Apply')]",
    ]
    for xp in xpaths:
        btn = try_xp(driver, xp, False)
        if btn:
            scroll_to_view(driver, btn, True, offset=80)
            return btn
    return False


def click_easy_apply(driver: WebDriver, pagination_element: WebElement | None,
                     application_link: str, tabs_count: int) -> tuple[bool, str, int]:
    """Click the external application button and switch to the new tab."""
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    ".//button[contains(@class,'jobs-apply-button') and contains(@class, 'artdeco-button--3')]",
                )
            )
        ).click()
        wait_span_click(driver, "Continue", 1, True, False)
        windows = driver.window_handles
        tabs_count = len(windows)
        driver.switch_to.window(windows[-1])
        application_link = driver.current_url
        print_lg(f'Got the external application link "{application_link}"')
        return False, application_link, tabs_count
    except (TimeoutException, ElementClickInterceptedException):
        if pagination_element is not None:
            return True, application_link, tabs_count
        return True, application_link, tabs_count
