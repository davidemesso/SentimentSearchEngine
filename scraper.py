import scrapy
import json

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    i = 0
    titles = []
    
    def start_requests(self):
        urls = ['https://www.tripadvisor.it/Restaurants-g187804-Parma_Province_of_Parma_Emilia_Romagna.html']
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):
        location = response.css('.breadcrumb:last-child::text').get()
        if location is not None:
            if location not in BlogSpider.titles:
                BlogSpider.titles += [location]
                BlogSpider.i = 0
            for review in response.css('.rev_wrap'):
                if review is not None:
                    username = review.css('.member_info .info_text div::text').get()
                    reviewText = review.css('.quote + .prw_reviews_text_summary_hsx div p::text').get()
                    reviewTextPost = review.css('.quote + .prw_reviews_text_summary_hsx div p span.postSnippet::text').get()
                    title = review.css('.title .noQuotes::text').get()
                    date = review.css('.prw_reviews_stay_date_hsx::text').get()
                    if(reviewTextPost is not None):
                        reviewText = reviewText[:-3] + reviewTextPost
                    if(reviewText.endswith("...")):
                        continue
                    if reviewText is not None or len(reviewText) < 100:
                        documentBody = {'title': title, 'location': location, 'body': reviewText, 'username': username, 'date': date}
                        with open(f"Documents/{location}+{BlogSpider.i}.json", "w") as file:
                            file.write(json.dumps(documentBody))
                        BlogSpider.i = BlogSpider.i+1
                        yield documentBody
            
        for next_section in response.css('#EATERY_SEARCH_RESULTS a'):
            yield response.follow(next_section, self.parse)

        for next_section in response.css('a.next'):
            yield response.follow(next_section, self.parse)

            