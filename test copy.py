from selenium import  webdriver
driver = webdriver.Chrome()
# driver allready started:)


from selenium_profiles.webdriver import profiles as profile_manager
from selenium_profiles.profiles import profiles

profile = profiles.Android() # or .Android()
driver.profiles = profile_manager(driver=driver, profile=profile)
driver.profiles.apply(profile)

driver.get('https://hmaker.github.io/selenium-detector/')  # test fingerprint

input("Press ENTER to exit")
driver.quit()  # Execute on the End!