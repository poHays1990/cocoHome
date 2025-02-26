import scrapy

class HousespiderSpider(scrapy.Spider):
    name = "housespider"
    allowed_domains = ["rentapartmentsaigon.vn"]
    start_urls = ["https://rentapartmentsaigon.vn/page/1/?post_type=property"]

    def __init__(self, *args, **kwargs):
        super(HousespiderSpider, self).__init__(*args, **kwargs)
        self.page_count = 0  # Compteur de pages visitées
        
    def parse(self, response):
        if self.page_count >= 3:  # Arrêter après 3 pages
            return
        
        self.page_count += 1  # Incrémenter le compteur
        
        
        houses = response.css("article[class^='post-']")
        for house in houses: 
            relative_page = house.css('div.item-title a::attr(href)').get()
        
            if relative_page is not None:
                yield response.follow(relative_page, callback=self.parse_house_page)
        
        next_page = response.css('li a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_house_page(self, response):
        labels = [label.rstrip(':') for label in response.xpath("//ul[@class='list-3-cols list-unstyled']//li//strong/text()").getall()]
        values = response.xpath("//ul[@class='list-3-cols list-unstyled']//li//span/text()").getall()
        utilities = response.xpath("//div[@id='property-features-wrap']//li/text()").getall()
        dict_final = dict(zip(labels, values))
        #print(dict_final)
        yield {
            'id': dict_final['Property ID'],
            'title': response.css('.page-title h1::text').get(),
            'price': dict_final['Price'],
            'area': dict_final['Area'],
            'utilities': utilities
        }
    

        


# Fonction pour récupérer les données des pages avec tous les résumés et filtres
"""
    def parse(self, response):
        houses = response.css("article[class^='post-']")
        
        for house in houses: 
            yield {
                'adresse': house.css('div p.item-address::text').get(),
                'price': house.css('div p.item-price::text').get(),
                'url': house.css('div a.btn::attr(href)').get(),
                
            }
        
        next_page = response.css('li a.next::attr(href)').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
"""