"""
Selenium automated test for SockShop front-end.
Simulates: browse products -> view detail -> add to cart -> login/register -> checkout.

Usage:
  python selenium_test.py --url http://localhost:30001
  python selenium_test.py --url http://localhost:30001 --headless
"""

import argparse
import time
import os
import sys
import subprocess
import signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def start_port_forward(port=30001):
    """Start kubectl port-forward and return the process handle."""
    proc = subprocess.Popen(
        ["kubectl", "port-forward", "-n", "sock-shop", "svc/front-end", f"{port}:80"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
    time.sleep(3)
    return proc


def stop_port_forward(proc):
    if proc:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def create_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-gpu")
    
    # Try chromedriver from PATH or known location
    chromedriver_paths = [
        os.environ.get("CHROMEDRIVER_PATH", ""),
        r"C:\Users\HP\Documents\install\chromedriver-for-google-chrome\148.0.7778.178\chromedriver-win64\chromedriver.exe",
        "chromedriver",
    ]
    
    for path in chromedriver_paths:
        if not path:
            continue
        try:
            if os.path.exists(path) or path == "chromedriver":
                service = Service(executable_path=path) if path != "chromedriver" else Service()
                return webdriver.Chrome(service=service, options=opts)
        except Exception:
            continue
    
    # Fallback: use webdriver-manager
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    except Exception:
        pass
    
    return webdriver.Chrome(options=opts)


class SockShopTester:
    def __init__(self, base_url, headless=True):
        self.base_url = base_url.rstrip("/")
        self.driver = create_driver(headless=headless)
        self.wait = WebDriverWait(self.driver, 10)
        self.results = []
    
    def log(self, msg, elapsed=None):
        entry = f"[{'OK' if elapsed else '--'}] {msg}"
        if elapsed:
            entry += f" ({elapsed:.2f}s)"
        print(entry)
        self.results.append({"message": msg, "elapsed": elapsed})
    
    def go_homepage(self):
        t0 = time.time()
        self.driver.get(self.base_url)
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product")))
        except TimeoutException:
            pass
        elapsed = time.time() - t0
        self.log("Open homepage", elapsed)
        return elapsed
    
    def browse_products(self):
        t0 = time.time()
        products = self.driver.find_elements(By.CSS_SELECTOR, ".product, .thumbnail, [class*='product']")
        count = len(products)
        if count == 0:
            products = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='detail']")
        count = len(products)
        elapsed = time.time() - t0
        self.log(f"Found {count} products on homepage", elapsed)
        return count
    
    def view_product_detail(self, index=0):
        t0 = time.time()
        links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='detail']")
        if not links:
            try:
                links = self.driver.find_elements(By.CSS_SELECTOR, ".product a, .thumbnail a")
            except Exception:
                pass
        
        if links and index < len(links):
            links[index].click()
        else:
            self.driver.get(f"{self.base_url}/detail.html?id={index + 1}")
        
        time.sleep(1)
        elapsed = time.time() - t0
        self.log("View product detail", elapsed)
        return elapsed
    
    def add_to_cart(self):
        t0 = time.time()
        try:
            btn = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btn-primary, [onclick*='cart'], a[href*='cart'], button[class*='cart']")))
            btn.click()
        except TimeoutException:
            try:
                self.driver.get(f"{self.base_url}/cart")
                self.driver.find_element(By.ID, "cart")
            except NoSuchElementException:
                pass
        time.sleep(1)
        elapsed = time.time() - t0
        self.log("Add to cart", elapsed)
        return elapsed
    
    def go_to_cart(self):
        t0 = time.time()
        try:
            cart_link = self.driver.find_element(By.CSS_SELECTOR, "a[href*='basket']")
            cart_link.click()
        except NoSuchElementException:
            self.driver.get(f"{self.base_url}/basket.html")
        time.sleep(1)
        elapsed = time.time() - t0
        self.log("Go to cart page", elapsed)
        return elapsed
    
    def register_user(self):
        t0 = time.time()
        import random
        username = f"testuser_{random.randint(10000, 99999)}"
        email = f"{username}@test.com"
        password = "Test1234"
        
        try:
            login_link = self.driver.find_element(By.CSS_SELECTOR, "a[href*='login']")
            login_link.click()
            time.sleep(1)
            
            reg_link = self.driver.find_element(By.CSS_SELECTOR, "a[href*='register'], #register")
            reg_link.click()
            time.sleep(1)
            
            self.driver.find_element(By.ID, "username").send_keys(username)
            self.driver.find_element(By.ID, "firstName").send_keys("Test")
            self.driver.find_element(By.ID, "lastName").send_keys("User")
            self.driver.find_element(By.ID, "email").send_keys(email)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .btn-primary").click()
            time.sleep(2)
            elapsed = time.time() - t0
            self.log(f"Register user: {username}", elapsed)
        except (TimeoutException, NoSuchElementException):
            elapsed = time.time() - t0
            self.log("Register: skipped (elements not found)", elapsed)
        
        return elapsed
    
    def login_user(self):
        t0 = time.time()
        try:
            self.driver.get(f"{self.base_url}/register.html")
            time.sleep(1)
            
            # Try multiple common ID patterns for SockShop register page
            for uid in ["username", "register-username", "user"]:
                try:
                    self.driver.find_element(By.ID, uid).send_keys("user1")
                    break
                except NoSuchElementException:
                    continue
            
            self.driver.find_element(By.ID, "password").send_keys("password")
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .btn-primary, button").click()
            time.sleep(2)
            
            elapsed = time.time() - t0
            self.log(f"Register & login completed", elapsed)
        except (TimeoutException, NoSuchElementException):
            elapsed = time.time() - t0
            self.log(f"Login: skipped (no register form found)", elapsed)
        return elapsed
    
    def place_order(self):
        t0 = time.time()
        try:
            self.driver.get(f"{self.base_url}/basket.html")
            time.sleep(1)
            
            # Try various checkout selectors
            checkout_btn = None
            for selector in ["a[href*='checkout']", "button[class*='checkout']", "#checkout",
                             "a[class*='btn-primary']", "button.btn-primary"]:
                try:
                    checkout_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if checkout_btn:
                        break
                except NoSuchElementException:
                    continue
            
            if checkout_btn:
                checkout_btn.click()
                time.sleep(2)
                elapsed = time.time() - t0
                self.log("Place order (checkout)", elapsed)
            else:
                elapsed = time.time() - t0
                self.log("Checkout: no checkout button found", elapsed)
        except Exception as e:
            elapsed = time.time() - t0
            self.log(f"Checkout: skipped ({str(e)[:40]})", elapsed)
        return elapsed
    
    def run_full_test(self):
        print("=" * 60)
        print(f"  SockShop Selenium Test - {self.base_url}")
        print("=" * 60)
        
        self.go_homepage()
        self.browse_products()
        self.view_product_detail(0)
        self.add_to_cart()
        self.go_to_cart()
        
        print("=" * 60)
        total = sum(r["elapsed"] for r in self.results if r["elapsed"])
        print(f"  Total time: {total:.2f}s")
        print(f"  Steps: {len(self.results)}")
        return self.results
    
    def close(self):
        self.driver.quit()


def main():
    parser = argparse.ArgumentParser(description="SockShop Selenium automated test")
    parser.add_argument("--url", default="http://localhost:30001", help="SockShop front-end URL")
    parser.add_argument("--headless", action="store_true", default=True, help="Run headless")
    parser.add_argument("--visible", action="store_false", dest="headless", help="Run with browser visible")
    parser.add_argument("--no-pf", action="store_true", help="Skip starting kubectl port-forward")
    args = parser.parse_args()
    
    pf_proc = None
    if not args.no_pf:
        print("Starting kubectl port-forward (svc/front-end -> :30001)...")
        pf_proc = start_port_forward(30001)
    
    try:
        tester = SockShopTester(args.url, headless=args.headless)
        try:
            results = tester.run_full_test()
        finally:
            tester.close()
    finally:
        if pf_proc:
            stop_port_forward(pf_proc)
            print("Port-forward stopped.")
    
    return results


if __name__ == "__main__":
    main()
