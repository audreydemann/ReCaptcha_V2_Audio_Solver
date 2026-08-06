import os
import time
import random
import requests
import traceback
from faster_whisper import WhisperModel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AudioCaptchaSolver:
    def __init__(self, driver, model_size="tiny", download_root=None):
        self.driver = driver
        self.model_size = model_size
        self.model = None
        
        if download_root is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.download_root = os.path.join(base_dir, "models")
        else:
            self.download_root = download_root
        os.makedirs(self.download_root, exist_ok=True)

    def _load_model(self):
        if self.model is None:
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8", download_root=self.download_root)

    def solve(self):
        try:
            checkbox_frame = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'reCAPTCHA') and not(contains(@title, 'challenge'))]"))
            )
            self.driver.switch_to.frame(checkbox_frame)
            
            checkbox = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
            )
            checkbox.click()
            self.driver.switch_to.default_content()
            
            time.sleep(2)
            
        except Exception:
            self.driver.switch_to.default_content()
            return False

        try:
            self.driver.switch_to.frame(checkbox_frame)
            is_checked = self.driver.find_elements(By.CLASS_NAME, "recaptcha-checkbox-checked")
            if is_checked and "true" in is_checked[0].get_attribute("aria-checked"):
                self.driver.switch_to.default_content()
                return True
            self.driver.switch_to.default_content()
        except:
            self.driver.switch_to.default_content()

        return self._handle_audio_challenge()

    def _handle_audio_challenge(self):
        try:
            challenge_frame = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'challenge')]"))
            )
            self.driver.switch_to.frame(challenge_frame)
            
            MAX_ATTEMPTS = 5
            for attempt in range(MAX_ATTEMPTS):
                try:
                    audio_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))
                    )
                    audio_btn.click()
                except:
                    if len(self.driver.find_elements(By.ID, "recaptcha-reload-button")) == 0:
                        pass
                
                time.sleep(2)
                
                if len(self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Try again later')]")) > 0:
                    self.driver.switch_to.default_content()
                    return False

                try:
                    audio_source = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.ID, "audio-source"))
                    )
                    src_url = audio_source.get_attribute("src")
                except:
                    break

                mp3_path = f"captcha_{random.randint(1000,9999)}.mp3"
                try:
                    r = requests.get(src_url)
                    with open(mp3_path, 'wb') as f:
                        f.write(r.content)
                        
                    self._load_model()
                    
                    segments, info = self.model.transcribe(mp3_path, beam_size=5)
                    text = " ".join([segment.text for segment in segments]).strip()
                finally:
                    if os.path.exists(mp3_path):
                        os.remove(mp3_path)
                
                try:
                    input_box = self.driver.find_element(By.ID, "audio-response")
                    input_box.clear()
                    input_box.send_keys(text.lower())
                except:
                    pass

                try:
                    verify_btn = self.driver.find_element(By.ID, "recaptcha-verify-button")
                    verify_btn.click()
                except:
                     pass
                
                time.sleep(2)
                
                error_msgs = self.driver.find_elements(By.CLASS_NAME, "rc-audiochallenge-error-message")
                retry_needed = False
                if error_msgs and error_msgs[0].is_displayed() and error_msgs[0].text.strip():
                    err_text = error_msgs[0].text
                    if "multiple correct" in err_text.lower():
                        retry_needed = True
                        time.sleep(2)
                    else:
                        try:
                            reload_btn = self.driver.find_element(By.ID, "recaptcha-reload-button")
                            reload_btn.click()
                            time.sleep(2)
                        except:
                            pass
                        continue
                
                if not retry_needed:
                    self.driver.switch_to.default_content()
                    
                    try:
                        checkbox_frame = self.driver.find_element(By.XPATH, "//iframe[contains(@title, 'reCAPTCHA') and not(contains(@title, 'challenge'))]")
                        self.driver.switch_to.frame(checkbox_frame)
                        is_checked = self.driver.find_elements(By.CLASS_NAME, "recaptcha-checkbox-checked")
                        if is_checked and "true" in is_checked[0].get_attribute("aria-checked"):
                            self.driver.switch_to.default_content()
                            return True
                    except:
                        pass
                    
                    try:
                        self.driver.switch_to.default_content()
                        challenge_frame = WebDriverWait(self.driver, 2).until(
                             EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'challenge')]"))
                        )
                        self.driver.switch_to.frame(challenge_frame)
                        continue 
                    except:
                        return True

            self.driver.switch_to.default_content()
            return False

        except Exception:
            self.driver.switch_to.default_content()
            return False
