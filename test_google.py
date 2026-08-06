import time
import os
import sys

# Force CWD for imports
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from driver.chrome_driver import create_driver
from solver import AudioCaptchaSolver

def test():
    driver = create_driver()
    
    try:
        driver.get("https://www.google.com/recaptcha/api2/demo")
        time.sleep(3)
        
        solver = AudioCaptchaSolver(driver)
        result = solver.solve()
        
        print(f"FINAL RESULT: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    test()
