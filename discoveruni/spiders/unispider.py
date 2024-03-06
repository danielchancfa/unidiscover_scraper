import scrapy
from scrapy import FormRequest
from scrapy.shell import inspect_response
import re


class UnispiderSpider(scrapy.Spider):
    name = 'unispider'
    # allowed_domains = ['www.discoveruni.gov.uk']
    start_urls = ['https://www.discoveruni.gov.uk/course-finder/results/']
    base_url = 'https://www.discoveruni.gov.uk/course-finder/results/'
    course_url = 'https://www.discoveruni.gov.uk/'

    payload = {
        'count': '20',
        'sort_by_subject': 'false',
        'course_query': '',
        'location_radio': 'region',
    }

    def parse(self, response):

        if not response.css('.comparison-course-area'):
            return

        for course in response.css('.comparison-course-area'):
            course_dict = {
                'courseidentifier': course.xpath('@data-courseidentifier').get(),
                'uniname': course.xpath('@data-uniname').get(),
                'uniid': course.xpath('@data-uniid').get(),
                'coursename': course.xpath('@data-coursename').get(),
                'link': course.xpath('a/@href').get()
            }
            detail_url = self.course_url + course_dict['link']
            yield response.follow(detail_url, callback=self.parse_details, meta={'item':course_dict})

        next_page_num = response.meta.get("page", 1) + 1
        self.payload['csrfmiddlewaretoken'] = response.css('[name="csrfmiddlewaretoken"]::attr(value)').get()
        self.payload['page'] = str(next_page_num)
        if next_page_num <= 40:
        # if next page is clickable:
            yield scrapy.FormRequest(
                self.base_url,
                method='POST',
                formdata=self.payload,
                callback=self.parse,
                meta={"page": next_page_num}
            )

    def parse_details(self, response):
        #testing site: 'https://www.discoveruni.gov.uk/course-details/10007783/NL41/Full-time/'

        course_name = response.xpath('//h1[@class="course-detail__course-name col-md-7"]/text()').get()
        item = response.meta['item']
        item['course_name'] = re.sub(r'\n', '', course_name)

        #Course details 5/6 pair information (Study mode, Length, Distance learning, Placement year, Year abroad..)


        for div in response.xpath('//div[@class="d-block d-md-none w-100"]/div/div/div'):
            kp_list = div.xpath('p/text()').getall()
            kp_list = [re.sub(r'\n', '', x) for x in kp_list]
            item[kp_list[0]] = kp_list[-1]

        item['earning'] = []
        item['employment'] = []
        item['occuption'] = []

        # Get how many tab (majors) in earning after the course
        earning_tab = response.xpath('//a[starts-with(@id, "earnings-after-course")]')
        if len(earning_tab) > 0:
            for i, tab in enumerate(earning_tab):
                # economics / accounting
                tab_name = tab.xpath('text()').get().strip("\n")

                # 3 type of information need to scrap: earning, employment, occupation
                earning_dict = {
                    tab_name: {}
                }

                employment_dict = {
                    tab_name: {}
                }

                occupation_dict = {
                    tab_name: {}
                }
                tag_id = response.xpath('//ul[@id="earnings-after-course-tab"]/li/a/@id').getall()[i]
                # _id > economics / accounting
                div = response.xpath(f'//div[@aria-labelledby="{tag_id}"]')

                ##earning data
                # col > After 15 months / After 3 years / After 5 years
                for col in div.xpath('div/div/div[@class="discover-uni-container"]/div/div'):
                    duration = col.xpath('h3/text()').get().strip("\n")
                    average_salary = col.xpath('div/div/h2/text()').get()
                    salary_range = col.xpath('div/div/p[1]/text()').get()
                    data_from = col.xpath('div/div/text()[4]').get()
                    graduating = col.xpath('div/div/p[last()-1]/text()').get()
                    col_stat = {
                        duration:
                        {
                            'average_salary': average_salary,
                            'salary_range': salary_range,
                            'data_from': data_from,
                            'graduating': graduating
                        }
                    }
                    earning_dict[tab_name].update(col_stat)
                item['earning'].append(earning_dict)

                ##employment data
                employment_div = response.xpath('//div[@id="employment-after-course-1"]//div[@class="employment-after-course__data-point"]/div/div')

                if len(employment_div) > 0:
                    employment_data = {}
                    for div in employment_div:
                        k = div.xpath('@data-label').get()
                        v = div.xpath('@data-value').get()
                        employment_data[k] = v
                employment_dict[tab_name].update(employment_data)
                item['employment'].append(employment_dict)

                #Occupation data
                occupation_div = response.xpath(f'//div[@id="occupation-types-{i+1}"]')
                occup_list = occupation_div.xpath('div/div/div[@class="discover-uni-container"]/div/div//li/text()').getall()
                occup_data = {}
                for x in occup_list:
                    if '%' in x:
                        k = x.split('%')[1]
                        v = x.split('%')[0] + '%'
                        occup_data[k] = v
                    else:
                        occup_data['other'] = x
                occupation_dict[tab_name].update(occup_data)
                item['occuption'].append(occup_data)

        yield item



