from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapper.scrapper.spiders.housespider import HousespiderSpider  # Vérifie le bon chemin

def run_spider():
    settings = get_project_settings()
    settings.update({
        "FEEDS": {
            "houseData.csv": {"format": "csv", "encoding": "utf8", "overwrite": True},
            # Tu peux aussi stocker en JSON :
            # "houseData.json": {"format": "json", "encoding": "utf8", "overwrite": True},
        }
    })

    process = CrawlerProcess(settings)
    process.crawl(HousespiderSpider)
    process.start()

if __name__ == "__main__":
    # run_spider()
    pass
