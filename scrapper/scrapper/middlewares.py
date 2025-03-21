# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ScrapperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScrapperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)




from urllib.parse import urlencode
from random import randint
import requests
from scrapy import signals
from urllib.parse import urlencode
from random import randint
import requests

# Middleware pour gérer les interactions avec le spider
class ScrapperSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        """Initialisation du middleware via Scrapy."""
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """Traite chaque réponse avant d'entrer dans le spider."""
        return None

    def process_spider_output(self, response, result, spider):
        """Traite les résultats renvoyés par le spider."""
        for i in result:
            yield i

    def process_start_requests(self, start_requests, spider):
        """Traite les requêtes initiales du spider."""
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        """Affiche un message lorsque le spider démarre."""
        spider.logger.info("Spider opened: %s" % spider.name)

# Middleware pour gérer les interactions avec le downloader
class ScrapperDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """Traite chaque requête avant qu'elle ne soit envoyée."""
        return None

    def process_response(self, request, response, spider):
        """Traite chaque réponse avant qu'elle ne soit transmise au spider."""
        return response

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

# Middleware pour simuler des user-agents aléatoires
class ScrapeOpsFakeUserAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT', 'https://headers.scrapeops.io/v1/user-agents')
        self.scrapeops_fake_user_agents_active = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_headers = []
        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()

    def _get_user_agents_list(self):
        """Récupère une liste de user-agents depuis ScrapeOps."""
        if self.scrapeops_api_key:
            response = requests.get(self.scrapeops_endpoint, params={'api_key': self.scrapeops_api_key})
            if response.status_code == 200:
                self.scrapeops_headers = response.json().get('result', [])
                
    def _scrapeops_fake_user_agents_enabled(self):
        """Active ou désactive l'utilisation des User-Agents ScrapeOps en fonction des paramètres."""
        if not self.scrapeops_api_key:  
            self.scrapeops_fake_user_agents_active = False  # Désactive si pas de clé API
        
        if self.scrapeops_fake_user_agents_active and not self.scrapeops_headers:
            print("⚠️ Aucune User-Agent récupérée. Désactivation du middleware.")
            self.scrapeops_fake_user_agents_active = False  # Désactive si aucune User-Agent récupérée

    def _get_random_user_agent(self):
        """Retourne un user-agent aléatoire."""
        if self.scrapeops_headers:
            return self.scrapeops_headers[randint(0, len(self.scrapeops_headers) - 1)]
        return None

    def process_request(self, request, spider):
        """Modifie l'en-tête User-Agent de chaque requête."""
        if self.scrapeops_fake_user_agents_active:
            user_agent = self._get_random_user_agent()
            if user_agent:
                request.headers['User-Agent'] = user_agent.get('user_agent')
            
        print("********** USER AGENT **********", flush=True)
        print(request.headers.get('User-Agent', 'No User-Agent Set'))

# Middleware pour simuler des en-têtes HTTP aléatoires
class ScrapeOpsFakeHeadersMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_HEADER_ENDPOINT', 'https://headers.scrapeops.io/v1/browser-headers')
        self.scrapeops_fake_headers_active = settings.get('SCRAPEOPS_FAKE_HEADER_ENABLED', True)
        self.scrapeops_headers = []
        self._get_headers_list()
        self._scrapeops_fake_headers_enabled()

    def _get_headers_list(self):
        """Récupère une liste d'en-têtes HTTP depuis ScrapeOps."""
        if self.scrapeops_api_key:
            response = requests.get(self.scrapeops_endpoint, params={'api_key': self.scrapeops_api_key})
            if response.status_code == 200:
                self.scrapeops_headers = response.json().get('result', [])
    
    def _scrapeops_fake_headers_enabled(self):
        """Active ou désactive l'utilisation des headers ScrapeOps en fonction des paramètres."""
        if not self.scrapeops_api_key:  
            self.scrapeops_fake_headers_active = False  # Désactive si pas de clé API
        
        if self.scrapeops_fake_headers_active and not self.scrapeops_headers:
            print("⚠️ Aucune en-tête récupérée. Désactivation du middleware.")
            self.scrapeops_fake_headers_active = False  # Désactive si aucune en-tête récupérée



    def _get_random_headers(self):
        """Retourne un ensemble d'en-têtes HTTP aléatoire."""
        if self.scrapeops_headers:
            return self.scrapeops_headers[randint(0, len(self.scrapeops_headers) - 1)]
        return None

    def process_request(self, request, spider):
        """Ajoute des en-têtes HTTP aléatoires à chaque requête."""
        random_browser_header = self._get_random_headers()
        
        request.headers['accept-language'] = random_browser_header['accept-language']
        if random_browser_header.get('sec-fetch-user'):
            request.headers['sec-fetch-user'] = random_browser_header['sec-fetch-user']
        if random_browser_header.get('sec-fetch-mod'):
            request.headers['sec-fetch-mod'] = random_browser_header['sec-fetch-mod']
        if random_browser_header.get('sec-fetch-site'):
            request.headers['sec-fetch-site'] = random_browser_header['sec-fetch-site']
        if random_browser_header.get('sec-ch-ua-platform'):
            request.headers['sec-ch-ua-platform'] = random_browser_header['sec-ch-ua-platform']
        if random_browser_header.get('sec-ch-ua-mobile'):
            request.headers['sec-ch-ua-mobile'] = random_browser_header['sec-ch-ua-mobile']
        if random_browser_header.get('sec-fetch-site'):
            request.headers['sec-fetch-site'] = random_browser_header['sec-fetch-site']
        if random_browser_header.get('sec-ch-ua'):
            request.headers['sec-ch-ua'] = random_browser_header['sec-ch-ua']
        request.headers['accept'] = random_browser_header['accept'] 
        request.headers['user-agent'] = random_browser_header['user-agent'] 
        request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests')
    

        print("************ NEW HEADER ATTACHED *******")
        print(request.headers)