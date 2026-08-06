import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

def create_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    
    driver = uc.Chrome(options=options)
    
    driver.set_window_size(1920, 1080)
    try:
        driver.maximize_window()
    except:
        pass
        
    return driver
