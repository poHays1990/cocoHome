import scrapy
from scrapper.items import HouseItem
import random

class HouseSpider(scrapy.Spider):
    """
    Classe Scrapy permettant de scraper des annonces immobilières depuis le site rentapartmentsaigon.vn.
    Elle commence par récupérer les liens des annonces à partir des pages listant les propriétés,
    puis suit ces liens pour extraire les informations détaillées de chaque bien.
    Le scraping est limité à trois pages pour éviter une surcharge inutile.
    """
    name = "housespider"  # Nom unique de l'araignée Scrapy
    allowed_domains = ["rentapartmentsaigon.vn"]  # Domaines autorisés pour éviter de scraper d'autres sites
    start_urls = ["https://rentapartmentsaigon.vn/page/1/?post_type=property"]  # URL de départ pour le scraping
    
    custom_settings = {
        'FEEDS': {
            'housedata.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
                'overwrite': True
            }
        }
    }
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    ]

    def __init__(self, *args, **kwargs):
        super(HouseSpider, self).__init__(*args, **kwargs)
        self.page_count = 0  # Compteur pour limiter le nombre de pages analysées
        
    def parse(self, response):
        """
        Fonction de parsing de la page principale.
        Récupère les liens des annonces et les suit.
        """
        if self.page_count >= 1:  # Arrêter après avoir analysé 3 pages
            return
        
        self.page_count += 1  # Incrémenter le compteur de pages traitées
        
        # Sélectionner les articles contenant les annonces immobilières
        houses = response.css("article[class^='post-']")
        for house in houses: 
            relative_page = house.css('div.item-title a::attr(href)').get()  # Récupérer le lien de la page de détail
        
            if relative_page is not None:
                yield response.follow(relative_page, callback=self.parse_house_page)  # Suivre le lien pour scraper la page de l'annonce
        
        # Vérifier s'il y a une page suivante et continuer le scraping si c'est le cas
        next_page = response.css('li a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_house_page(self, response):
        """
        Fonction pour récupérer les détails d'une annonce immobilière.
        """
        # Récupérer les labels et les valeurs associés (ex: 'Price' -> '1500$/mois')
        labels = [label.rstrip(':') for label in response.xpath("//ul[@class='list-3-cols list-unstyled']//li//strong/text()").getall()]
        values = response.xpath("//ul[@class='list-3-cols list-unstyled']//li//span/text()").getall()
        adresse = response.xpath("//div[@class='col-12 header-content pb-3']//p[@class='item-address']/text()").getall()
        utilities = response.xpath("//div[@id='property-features-wrap']//li/text()").getall()  # Liste des équipements
        
        dict_final = dict(zip(labels, values))  # Créer un dictionnaire associant chaque label à sa valeur
        house_item = HouseItem()
        
        # Retourner les données sous forme de dictionnaire
        house_item['id'] = dict_final.get('Property ID', 'N/A')  # ID de l'annonce
        house_item['title'] = response.css('.page-title h1::text').get()  # Titre de l'annonce
        house_item['price'] = dict_final.get('Price', 'N/A')  # Prix du bien
        house_item['area'] = dict_final.get('Area', 'N/A')  # Superficie
        house_item['adresse'] = adresse[0]
        house_item['utilities'] = utilities  # Liste des équipements fournis

        yield house_item

# Ancienne fonction de scraping qui récupérait uniquement les résumés
"""
    def parse(self, response):
        houses = response.css("article[class^='post-']")
        
        for house in houses: 
            yield {
                'adresse': house.css('div p.item-address::text').get(),  # Adresse de l'appartement
                'price': house.css('div p.item-price::text').get(),  # Prix
                'url': house.css('div a.btn::attr(href)').get(),  # Lien de l'annonce
            }
        
        next_page = response.css('li a.next::attr(href)').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
"""
