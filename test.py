import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
import json
import random

import undetected_chromedriver as uc

def human_delay(min_delay=0.5, max_delay=1.2):
    time.sleep(random.uniform(min_delay, max_delay))

def fill_input(driver, by, locator, value, label=""):
    wait = WebDriverWait(driver, 15)
    try:
        print(f"🟢 Filling {label}...")
        element = wait.until(EC.element_to_be_clickable((by, locator)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        human_delay()
        element.click()
        human_delay()
        element.clear()
        human_delay()
        element.send_keys(value)
        human_delay()
        print(f"✅ {label} filled with: {value}")
    except Exception as e:
        print(f"❌ Failed to fill {label}: {e}")


def click_local_buy_button(driver, label="Nakupujte u místních"):
    wait = WebDriverWait(driver, 15)
    try:
        print(f"🟢 Waiting for '{label}' button...")
        button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//div[@role='button' and @aria-label='{label}']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        human_delay()
        button.click()
        human_delay(1, 2)
        print(f"✅ Clicked '{label}' button.")
    except Exception as e:
        print(f"❌ Failed to click '{label}': {e}")


def click_button_by_aria_label(driver, aria_label, timeout=15):
    wait = WebDriverWait(driver, timeout)
    try:
        print(f"🟢 Waiting for button '{aria_label}'...")
        button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//div[@role='button' and @aria-label='{aria_label}']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        human_delay()
        button.click()
        human_delay(1, 2)
        print(f"✅ Clicked '{aria_label}' button.")
    except Exception as e:
        print(f"❌ Failed to click '{aria_label}': {e}")

def click_background_to_dismiss(driver):
    try:
        print("🟢 Attempting to dismiss overlays by clicking background...")
        body = driver.find_element(By.TAG_NAME, "body")
        body.click()
        human_delay(0.5, 1)
        print("✅ Background clicked to dismiss overlays.")
    except Exception as e:
        print(f"❌ Failed to click background: {e}")


def dismiss_location_suggestion_if_present(driver):
    try:
        suggestions = driver.find_elements(By.XPATH, "//li[@role='option']")
        if suggestions:
            print("🟡 Suggestion popup found — attempting to click first option.")
            suggestions[0].click()
            human_delay()
            print("✅ Suggestion clicked.")
    except Exception as e:
        print(f"❌ Failed to handle suggestion popup: {e}")

# headline bull
def fill_by_label(driver, label_text, value, label=""):
    try:
        print(f"🟢 Filling field labeled '{label_text}'...")
        xpath = f"//span[text()='{label_text}']/ancestor::label//input[@dir='ltr']"
        fill_input(driver, By.XPATH, xpath, value, label)
    except Exception as e:
        print(f"❌ Failed to fill field '{label_text}': {e}")


# Dropdown Categories
def click_category_dropdown(driver):
    try:
        print("🟢 Clicking 'Kategorie' dropdown...")
        dropdown_xpath = "//span[text()='Kategorie']/ancestor::label[@role='combobox']"
        wait = WebDriverWait(driver, 15)
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", dropdown)
        human_delay()
        dropdown.click()
        human_delay(1, 2)
        print("✅ Clicked 'Kategorie' dropdown.")
    except Exception as e:
        print(f"❌ Failed to click 'Kategorie' dropdown: {e}")

# Condition dropdown
def click_condition_dropdown(driver):
    try:
        print("🟢 Clicking 'Stav' dropdown...")
        dropdown_xpath = "//span[text()='Stav']/ancestor::label[@role='combobox']"
        wait = WebDriverWait(driver, 15)
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", dropdown)
        human_delay()
        dropdown.click()
        human_delay(1, 2)
        print("✅ Clicked 'Stav' dropdown.")
    except Exception as e:
        print(f"❌ Failed to click 'Stav' dropdown: {e}")


def select_category_option(driver, category_name):
    try:
        print(f"🟢 Waiting for category dialog and selecting: '{category_name}'...")
        xpath = f"//div[@aria-label='Category selection menu for marketplace listing' and @role='dialog']//div[@role='button' and @tabindex='0']//span[text()='{category_name}']"
        wait = WebDriverWait(driver, 10)
        option = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", option)
        human_delay()
        option.click()
        human_delay()
        print(f"✅ Category selected: '{category_name}'")
    except Exception as e:
        print(f"❌ Failed to select category '{category_name}': {e}")



def select_condition(driver, condition_text, timeout=10):
    """
    Selects a condition from the Facebook Marketplace dropdown.

    :param driver: Selenium WebDriver instance
    :param condition_text: The visible text of the condition to select (e.g., "Nové")
    :param timeout: Maximum wait time for elements (default: 10 seconds)
    """
    wait = WebDriverWait(driver, timeout)

    try:
        # Step 1: Click the dropdown (label or span containing 'Stav')
        dropdown_trigger = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[contains(., 'Stav')] | //span[text()='Stav']")
        ))
        dropdown_trigger.click()

        # Step 2: Wait for the desired condition option and click it
        condition_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[@role='option']//span[contains(text(), '{condition_text}')]")
        ))
        condition_option.click()

        print(f"[✔] Selected condition: {condition_text}")

    except Exception as e:
        print(f"[✖] Failed to select condition '{condition_text}': {e}")

driver = uc.Chrome(headless=False)

driver.get('https://www.facebook.com/marketplace')


with open("cookies2.json", "r") as f:
    cookies = json.load(f)

# Step 3: Apply cookies to the driver
for cookie in cookies:
    # Remove 'sameSite' if it's not accepted by Selenium
    cookie.pop('sameSite', None)
    try:
        driver.add_cookie(cookie)
    except Exception as e:
        print(f"Failed to add cookie {cookie['name']}: {e}")

driver.refresh()

# 1. Navigate to Marketplace
driver.get("https://www.facebook.com/marketplace")
human_delay(1.5, 3)

# 2. Click "Create new listing"

# 3. Fill ZIP Code
fill_input(driver, By.XPATH, "//input[@aria-label='PSČ nebo město']", "Pardubice", label="ZIP Code")


# Dismiss options
dismiss_location_suggestion_if_present(driver)

# POP UP
# 3.5 Wait for and click "Nakupujte u místních"
# Wait and click "Nakupujte u místních"
click_local_buy_button(driver)


# confirm popUp
# click_button_by_aria_label(driver, "Aktualizovat")


try:
    wait = WebDriverWait(driver, 15)  # Define it before usage
    print("🟢 Clicking 'Create new listing'...")
    create_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//a[contains(@aria-label, 'Vytvořit nový inzerát')]"
    )))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", create_btn)
    human_delay()
    create_btn.click()
    human_delay(1, 2)
    print("✅ Clicked 'Create new listing'")
except Exception as e:
    print(f"❌ Failed to click 'Create new listing': {e}")

# logged in now

# 4. Fill Email
fill_input(driver, By.XPATH, "//input[@type='email']", "example@example.com", label="Email")

# 5. Upload Photos
try:
    print("🟢 Uploading photos...")
    photo_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
    photo_input.send_keys("/path/to/photo1.jpg\n/path/to/photo2.jpg")
    human_delay(2, 4)
    print("✅ Photos uploaded")
except Exception as e:
    print(f"❌ Failed to upload photos: {e}")


# Headline
fill_by_label(driver, "Název", "Bazarová sedačka", label="Headline")

# 6. Fill Price
fill_input(driver, By.XPATH, "//input[@inputmode='numeric']", "100", label="Price")

click_category_dropdown(driver)

select_category_option(driver,"Nářadí")

click_condition_dropdown(driver)


select_condition(driver, "Nové")
# select_condition(driver, "Použité, jako nové")


# 8. Fill Description
fill_input(driver, By.XPATH, "//textarea", "Brand new item, excellent condition.", label="Description")

# 9. Publish Listing
try:
    print("🟢 Clicking 'Publish'...")
    publish_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@aria-label, 'Publikovat')]")))
    driver.execute_script("arguments[0].click();", publish_btn)
    human_delay(2, 4)
    print("✅ Listing published")
except Exception as e:
    print(f"❌ Failed to publish listing: {e}")
