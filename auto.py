import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class AILoginTest(unittest.TestCase):

    def setUp(self):
        # Use webdriver-manager to handle ChromeDriver automatically
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://the-internet.herokuapp.com/login") # Example site
        self.wait = WebDriverWait(self.driver, 10)

    def test_valid_login(self):
        """Test logging in with valid credentials."""
        driver = self.driver
        # AI might identify elements by their text, label, or visual context
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys("tomsmith")
        password_field.send_keys("SuperSecretPassword!")
        login_button.click()

        # Wait for and verify success message
        success_message = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
        )
        self.assertIn("You logged into a secure area!", success_message.text)

    def test_invalid_login(self):
        """Test logging in with invalid credentials."""
        driver = self.driver
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys("invalid_user")
        password_field.send_keys("wrong_password")
        login_button.click()

        # Wait for and verify failure message
        failure_message = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
        )
        self.assertIn("Your username is invalid!", failure_message.text)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()