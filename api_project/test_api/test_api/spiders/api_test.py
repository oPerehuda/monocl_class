import scrapy
import json

class ApiTestSpider(scrapy.Spider):
    name = "api_test"
    allowed_domains = ["ebmt2023.planner.documedias.systems"]
    custom_settings = {"DOWNLOAD_DELAY": 1, "CONQURRENT_REQUEST": 1}
    start_urls = ["https://ebmt2023.planner.documedias.systems/api/program/days/1?program_mode=list&program_sort=date&filter_display_type=7,9&filter_group=is_not_child",
                "https://ebmt2023.planner.documedias.systems/api/program/days/2program_mode=list&program_sort=date&filter_display_type=7,9&filter_group=is_not_child",
                "https://ebmt2023.planner.documedias.systems/api/program/days/3?program_mode=list&program_sort=date&filter_display_type=7,9&filter_group=is_not_child",
                "https://ebmt2023.planner.documedias.systems/api/program/days/4?program_mode=list&program_sort=date&filter_display_type=7,9&filter_group=is_not_child",]

    def parse(self, response):
        sessions = response.json()
        for session in sessions[:6]:
            session_name = session["title"]
            session_id = session["id"]
            created_url = "https://ebmt2023.planner.documedias.systems/api/program/sessions/" + str(session_id)
            #created_url = "https://ebmt2023.abstractserver.com/program/#/details/sessions/" + str(session_id)
            #print(session_id,"---",session_name)
            yield scrapy.Request(created_url, callback=self.parse_sessions, dont_filter=True)


    def parse_sessions(self, response):
        print(response.url)
        session_info = response.json()
        session_name = session_info[0]['title']
        print(session_name)
        moderators = session_info[0]['persons']
        print(len(moderators), "found moderators")
        if len(moderators) > 0:
            for moderator in moderators:
                moderator_name = moderator["person"]["first_name"] + " " + moderator["person"]["last_name"] 
                moderator_aff = moderator["person"]["institution"] + ", " + moderator["person"]["country"]["name"]
                moderator_email = moderator["person"]["email"]
                print(f"{moderator_name}---{moderator_aff}---{moderator_email}")
        
        presentations = session_info[0]["presentations"]
        for presentation in presentations:
            presentation_title = presentation["presentation"]["title"]
            presentation_authors = presentation["presentation"]["persons"]
            print(f"{presentation_title:}")
            for presentation_author in presentation_authors:
                author_name = presentation_author["person"]["first_name"] + " " + presentation_author["person"]["last_name"]
                author_aff = str(presentation_author["person"]["institution"]) + ", " + presentation_author["person"]["country"]["name"]
                author_email = presentation_author["person"]["email"]
                print(f"{author_name}---{author_aff}---{author_email}")
                