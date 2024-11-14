import scrapy
import json
import re
from .matching import join_authors_affs
from fuzzywuzzy import fuzz

class ApiTestSpider(scrapy.Spider):
    name = "api_test_posters"
    allowed_domains = ["ebmt2023.planner.documedias.systems"]
    custom_settings = {"DOWNLOAD_DELAY": 1, "CONQURRENT_REQUEST": 1}
    start_urls = [
        "https://ebmt2023.planner.documedias.systems/api/program/sessions/286,287,285,293,273,306,307,302,298,299,300,301,303,304,305,283,272,294,267,271,274,270,278,275,276,277,279,280,281,282,284,288,289,290,291,292,295,296,297",
        ]

    def parse(self, response):
        sessions = response.json()
        for session in sessions[:1]:
            session_name = session["title"]
            print("session ---", session_name)
            posters = session["presentations"]
            for poster in posters[:4]:
                poster_id = poster["presentation_id"]
                abstract_id = poster["presentation"]["abstract_id"]
                poster_url_table = "https://ebmt2023.abstractserver.com/program/#/details/presentations/" + str(poster_id)
                poster_url_spider = "https://ebmt2023.abstract.documedias.systems/api/v1/manager/abstract/multi/html/id/" + str(abstract_id) + "/template/planner_preview"
                poster_title = poster["presentation"]["title"]
                try:
                    poster_presenter = poster["presentation"]["persons"][0]["person"]["first_name"] + " " + poster["presentation"]["persons"][0]["person"]["last_name"]
                    presenter_email = poster["presentation"]["persons"][0]["person"]["email"]
                except (KeyError, IndexError):
                    poster_presenter = ""
                    presenter_email = ""
                print(f"{poster_title} --- {poster_presenter} --- {presenter_email}")

                yield scrapy.Request(poster_url_spider, callback=self.parse_abstracts, dont_filter=True, 
                                    meta={'session_name': session_name, "abstract_url": poster_url_table, "title": poster_title, "author": poster_presenter, "email": presenter_email, "abstract_id": abstract_id})
    
    @staticmethod
    def cleanhtml(raw_html):
        CLEANR = re.compile('<.*?>')
        cleantext = re.sub(CLEANR, '', raw_html)
        return cleantext
    
    def check_empty_lists(poster_index, header_list, poster_text_list):
        """Function checks empty lists & provided args"""
        if header_list == [] or poster_text_list == []:
            print(f"{poster_index} error in dividing header")
            
    def check_aff_list(self, number, affList):
        """ Function check if index of the last element equal to the lenght of the aff list"""
        for count, value in enumerate(affList, start=1):
            index1 = len(str(count))
            index2 = value[:(index1)]
            if str(count) != index2:
                print(f"{number}--{count}--{index2}--{value}")
                print('---------------check last aff list value --------------------')
    

    def parse_abstracts(self, response):
        #print(response.url, response.meta)
        abstract_id = response.meta["abstract_id"]
        abstracts = response.json()
    
        # print(type(abstracts), abstracts)
        raw_abstracts = abstracts[str(abstract_id)]
        raw_authors = re.split(r"Background", raw_abstracts)[0]
        raw_auth = self.cleanhtml(raw_authors)
        raw_abstracts = re.split(r"Background", raw_abstracts)[1]
        raw_abs = self.cleanhtml(raw_abstracts)
        pattern = re.split(r"(?=\n\d+)", raw_auth)
        
        divided_authors = re.split(", ", pattern[0].strip())
        divided_affiliations = re.split(", (?=\d)", pattern[1].strip())
        #print(f"{divided_authors}---{divided_affiliations}")
        
        #self.check_aff_list(abstract_id, divided_affiliations)
        print(response.meta["author"])
        combination = join_authors_affs(divided_authors, divided_affiliations, abstract_id)
        
        for element in combination:
            percentage = fuzz.ratio(response.meta["author"], element[0])
            
            role = "Poster Presenter" if percentage > 90 else "Abstract Author"
            email = response.meta["email"] if role == "Poster Presenter" else ""
            #print(role, "---", element)
            poster_results = {
                    "name": element[0],
                    "affiliation": element[1],
                    "role": role,
                    "email": email,
                    "session_name": response.meta["session_name"],
                    "session_description": "",
                    "presentation_title": response.meta["title"],
                    "presentation_abstract": raw_abs,
                    "URL": response.meta["abstract_url"],
                    "Video URL": "",
                        }
            
            yield (poster_results)

        
        
        
        
        
        #print(check)
        #for raw_abstract in raw_abstracts:
        
            
            
            
            
            # poster_id = poster["id"]
            # created_url = "https://ebmt2023.planner.documedias.systems/api/program/presentations/" + str(poster_id)
            # #created_url = "https://ebmt2023.abstractserver.com/program/#/details/sessions/" + str(session_id)
            # print(created_url)
            # yield scrapy.Request(created_url, callback=self.parse_posters, dont_filter=True)


    # def parse_posters(self, response):
    #     print(response.url)
    #     poster_info = response.json()
    #     #poster_session = poster_info[0]['title']
    #     #print("session---", poster_session)
    #     posters = poster_info["presentations"]
    #     for poster in posters:
    #         poster_id = poster["presentation_id"]
    #         poster_url_table = "https://ebmt2023.abstractserver.com/program/#/details/presentations/" + str(poster_id)
    #         poster_url_spider = "https://ebmt2023.planner.documedias.systems/api/program/presentations/" + str(poster_id)
    #         poster_title = poster["presentation"]["title"]
    #         poster_presenter = poster["presentation"]["persons"][0]["person"]["first_name"] + " " + poster["presentation"]["persons"][0]["person"]["last_name"]
    #         presenter_email = poster["presentation"]["persons"][0]["person"]["email"]
    #         print(f"{poster_title} --- {poster_presenter} --- {presenter_email}")
            
            
            
        # poster_url = "https://ebmt2023.planner.documedias.systems/api/program/presentations/" + poster_id
        # poster_
        # print(poster_info)
        # presenters = poster_info[0]['persons']
        # print(len(presenters), "found presenters")
    #     if len(moderators) > 0:
    #         for moderator in moderators:
    #             moderator_name = moderator["person"]["first_name"] + " " + moderator["person"]["last_name"] 
    #             moderator_aff = moderator["person"]["institution"] + ", " + moderator["person"]["country"]["name"]
    #             moderator_email = moderator["person"]["email"]
    #             print(f"{moderator_name}---{moderator_aff}---{moderator_email}")
    #             moderator_results = {
    #                 "name": moderator_name,
    #                 "affiliation": moderator_aff,
    #                 "role": "Moderator",
    #                 "email": moderator_email,
    #                 "session_name": session_name,
    #                 "session_description": "",
    #                 "presentation_title": "",
    #                 "presentation_abstract": "",
    #                 "URL": session_url,
    #                 "Video URL": "",
    #                     }
    #             yield moderator_results
                
                
    #     print("----------------------------------")
        
    #     presentations = session_info[0]["presentations"]
    #     for presentation in presentations:
    #         presentation_title = presentation["presentation"]["title"]
    #         presentation_authors = presentation["presentation"]["persons"]
    #         print(f"{presentation_title:}")
    #         for presentation_author in presentation_authors:
    #             author_name = presentation_author["person"]["first_name"] + " " + presentation_author["person"]["last_name"]
    #             author_aff = str(presentation_author["person"]["institution"]) + ", " + presentation_author["person"]["country"]["name"]
    #             author_email = presentation_author["person"]["email"]
    #             print(f"{author_name}---{author_aff}---{author_email}")
    #             presenter_results = {
    #                 "name": author_name,
    #                 "affiliation": author_aff,
    #                 "role": "Speaker",
    #                 "email": author_email,
    #                 "session_name": session_name,
    #                 "session_description": "",
    #                 "presentation_title": presentation_title,
    #                 "presentation_abstract": "",
    #                 "URL": session_url,
    #                 "Video URL": "",
    #                     }
    #             yield presenter_results