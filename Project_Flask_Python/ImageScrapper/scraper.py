import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from datetime import datetime


class ImageScraper:
    def __init__(self, driver_path, target_path="./images", mongo_uri="mongodb://localhost:27017/"):
        self.driver_path = driver_path
        self.target_path = target_path

        # MongoDB connection
        self.client = MongoClient(mongo_uri)
        self.db = self.client["image_scraper_db"]
        self.collection = self.db["images"]

    def fetch_image_urls(self, query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
        def scroll_to_end(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_between_interactions)

        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
        wd.get(search_url.format(q=query))

        image_urls = set()
        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            scroll_to_end(wd)

            thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")
            number_results = len(thumbnail_results)

            print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

            for img in thumbnail_results[results_start:number_results]:
                try:
                    img.click()
                    time.sleep(sleep_between_interactions)
                except Exception:
                    continue

                actual_images = wd.find_elements(By.CSS_SELECTOR, 'img.sFlh5c.FyHeAf.iPVvYb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        image_urls.add(actual_image.get_attribute('src'))

                image_count = len(image_urls)

                if len(image_urls) >= max_links_to_fetch:
                    print(f"Found: {len(image_urls)} image links, done!")
                    break
            else:
                print("Found:", len(image_urls), "image links, looking for more ...")
                time.sleep(30)
                try:
                    load_more_button = wd.find_element(By.CSS_SELECTOR, ".mye4qd")
                    if load_more_button:
                        wd.execute_script("document.querySelector('.mye4qd').click();")
                except Exception:
                    pass

            results_start = len(thumbnail_results)

        return image_urls

    def save_to_db(self, query, image_name, image_content):
        """Save image binary into MongoDB"""
        self.collection.insert_one({
            "query": query,
            "image_name": image_name,
            "image_data": image_content,
            "timestamp": datetime.now()
        })

    def get_images_from_db(self, query):
        """Fetch images for a query from MongoDB"""
        return list(self.collection.find({"query": query}))

    def persist_image(self, folder_path: str, url: str, counter, query: str):
        try:
            image_content = requests.get(url).content
        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")
            return

        try:
            file_name = 'jpg' + "_" + str(counter) + ".jpg"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'wb') as f:
                f.write(image_content)
            print(f"SUCCESS - saved {url} - as {file_path}")

            # save in DB
            self.save_to_db(query, file_name, image_content)

        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")

    def search_and_download(self, search_term: str, number_images=10):
        """Main method: checks DB first, then scrapes if needed"""
        # Step 1: Check DB first
        db_results = self.get_images_from_db(search_term)
        if db_results:
            print(f"✅ Found {len(db_results)} images in DB for '{search_term}', skipping scrape.")
            return db_results

        # Step 2: If not in DB, scrape
        print(f"❌ No images in DB for '{search_term}', scraping now...")
        target_folder = os.path.join(self.target_path, '_'.join(search_term.lower().split(' ')))
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        service = Service(self.driver_path)
        with webdriver.Chrome(service=service) as wd:
            res = self.fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=1.5)

        counter = 0
        for elem in res:
            self.persist_image(target_folder, elem, counter, search_term)
            counter += 1

        return self.get_images_from_db(search_term)

    def fetch_images_by_name(self, query):
        """Fetch images by name from MongoDB and save locally"""
        results = self.get_images_from_db(query)
        if not results:
            print(f"No images found in DB for '{query}'")
            return []

        folder = os.path.join(self.target_path, query)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i, doc in enumerate(results):
            file_path = os.path.join(folder, doc["image_name"])
            with open(file_path, "wb") as f:
                f.write(doc["image_data"])
        print(f"✅ {len(results)} images fetched from DB and saved to {folder}")
        return results


# Example usage
if __name__ == "__main__":
    DRIVER_PATH = r'D:\Data_Science\Project_Flask_Python\ImageScrapper\chromedriver.exe'
    scraper = ImageScraper(driver_path=DRIVER_PATH)

    # First run: Scrape and save in DB
    scraper.search_and_download("karbala", number_images=10)

    # Next run: Directly fetch from DB
    scraper.fetch_images_by_name("karbala")
