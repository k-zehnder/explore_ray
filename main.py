from classes import *

if __name__ == "__main__":
    # setup "analyzers"
    sim_analyzer = SimilarityAnalyzer()
    bw_analyzer= BlackWhiteThresholdAnalyzer()
    
    # collect image data
    scraper = Scraper.remote("/home/batman/Desktop/explore_ray/chromedriver")
    print(scraper.load_images_from_folder.remote())
    results = ray.get(scraper.get_images.remote())
    print(results)
    
    # img_urls = scraper.fetch_image_urls("cat", 5, 1)
    # TODO: scraper.persist_images(image_urls)
    
    # validate images
    """
    results = {}
    for analyzer in [sim, bw]:
        for path in image_paths:
            image = cv2.imread(path)
            bool_result = analyzer.isValidImage(image)
            results[(analyzer, path)] = boolResult
    return results
    """