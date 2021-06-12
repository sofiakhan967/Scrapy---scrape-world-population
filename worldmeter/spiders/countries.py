import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']
    
    def parse(self, response):
        #first we grab the country name and its links 
        countries=response.xpath("//td/a")
        for country in countries:
            country_name=country.xpath(".//text()").get()
            link=country.xpath(".//@href").get()
            #absolute_url=f"https://worldometers.info{Link}"
           # absolute=response.urljoin(link)
           #then we use response.follow or absolute url method to concenate realtive url 
           #use callback method to pass response url to another method so we can parse each url 
            yield response.follow(url=link , callback=self.parse_country,meta={'Name':country_name})
# take url and parse it 
    def parse_country(self,response):
        #here we take country name from above function after passing its values to response .follow in meta 
        country_name=response.request.meta['Name']
        #logging.info(response.url) # for checking that we got absolute url or not
        rows=response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for row in rows:
            year=row.xpath(".//td[1]/text()").get()
            population=row.xpath(".//td[2]/strong/text()").get()

            yield{
                'Name':country_name,
                'Year':year,
                'Population':population
            }

