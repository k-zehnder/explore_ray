import os
import cv2
from abc import ABC, abstractmethod

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class ImageValidator(ABC):
    @abstractmethod
    def isValidImage(self):
        pass

class SimilarityAnalyzer(ImageValidator):
    def isValidImage(self):
        pass
    
class BlackWhiteThresholdAnalyzer(ImageValidator):
    def isValidImage(self):
        pass
    
class Scraper:
    def __init__(self, chrome_driver_path):
        self.chrome_driver_path = chrome_driver_path
        self.ser = Service(self.chrome_driver_path)
        self.op = webdriver.ChromeOptions()
        self.wd = webdriver.Chrome(service=self.ser, options=self.op)
    
    def fetch_image_urls(self, query:str, max_links_to_fetch:int,sleep_between_interactions:int=1):
        # build the google query
        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        # load the page
        self.wd.get(search_url.format(q=query))

        image_urls = set()
        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            thumbnail_results = self.wd.find_elements_by_css_selector("img.Q4LuWd")
            number_results = len(thumbnail_results)


            for img in thumbnail_results[results_start:number_results]:
                # try to click every thumbnail such that we can get the real image behind it
                try:
                    img.click()
                    time.sleep(sleep_between_interactions)
                except Exception:
                    continue

            #     # extract image urls    
                actual_images = self.wd.find_elements_by_css_selector('img.n3VNCb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        image_urls.add(actual_image.get_attribute('src'))

                image_count = len(image_urls)
                print(f'image count: {image_count}')
                if len(image_urls) >= max_links_to_fetch:
                    print(f"Found: {len(image_urls)} image links, done!")
                    break
                else:
                    print("Found:", len(image_urls), "image links, looking for more ...")
                # time.sleep(30)
            #     #return
                load_more_button = self.wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    self.wd.execute_script("document.querySelector('.mye4qd').click();")

                # move the result startpoint further down
                results_start = len(thumbnail_results)

        return image_urls
    

if __name__ == "__main__":
    # 
    sim_analyzer = SimilarityAnalyzer()
    bw_analyzer= BlackWhiteThresholdAnalyzer()
    
    scraper = Scraper("/home/batman/Desktop/py/automate_boring_stuff/ray/chromedriver")
    img_urls = scraper.fetch_image_urls("cat", 5, 1)
    
    """
    results = {}
    for analyzer in [sim, bw]:
        for path in image_paths:
            image = cv2.imread(path)
            bool_result = analyzer.isValidImage(image)
            results[path] = boolResult
    return results
    """
    
    # NOTE: like adrian...
    # sp = SimpleImagePreprocessor(sim_analyer, bw_analyzer)