import openpyxl
from openpyxl import Workbook
import re
from matching import join_authors_affs

# creating output excel file
wb = Workbook()
ws = wb.active
abstractUrl = ''
role0 = 'Abstract author'
email = ''
session_description = ''

# creating table headers
table_title = [
    'Name (incl. titles)', 
    'Affiliation/Organisation and location', 
    'Role', 
    'Email', 
    'Session Name', 
    'Session Description', 
    'Presentation Title', 
    'Presentation Abstract', 
    'Abstract URL', 
    'Video URL',
    ]
ws.append(table_title)

def check_aff_list(number, affList):
    """ Function check if index of the last element equal to the lenght of the aff list"""
    for count, value in enumerate(affList, start=1):
        index1 = len(str(count))
        index2 = value[:(index1)]
        if str(count) != index2:
            print(f"{number}--{count}--{index2}--{value}")
            print('---------------check last aff list value --------------------')

file = open('/Users/oleh.perehuda/Documents/03 SCRAPY/projects/scrapers_class/pdf_processing/monocl_class/ab_raw.txt', 'r', encoding="UTF-8")

text = []
lines = []
posters = []

def check_empty_lists(poster_index, header_list, poster_text_list):
    """Function checks empty lists & provided args"""
    if header_list == [] or poster_text_list == []:
        print(f"{poster_index} error in dividing header")

for line in file:
    if re.search("5th World Psoriasis & Psoriatic Arthritis Conference 2018", line.strip()):
        pass
    elif re.match(r"^(P\d{3})", line.strip()):
        posters.append(text)
        text = [line.strip()]
    else:
        if line.strip != "":
            text.append(line.strip())

posters.append(text)

for poster in posters[1:]:
    abstract_flag = False
    header = []
    poster_text = []
    for element in poster:
        if re.match(r"(Introduction|Background|Objective|£)", element):
            abstract_flag = True
        if abstract_flag:
            poster_text.append(element)
        else:
            header.append(element)

    # check_empty_lists(poster[0], header, poster_text)    
    affiliation_flag = False
    title_and_authors = []
    affiliations_raw = []
    
    if len(header) == 4:
        title_and_authors = header[1:3]
        title = header[1]
        authors = header[2].split(",")
        affiliations = header[-1]
        for ind_author in authors:
            ws.append([ind_author, affiliations, role0, email, "", "", title, "".join(poster_text),"","",])
            
    else:        
        for item in header:
            if re.match(r"^1(?=[A-Z]*[a-z]*)", item):
                affiliation_flag = True
            if affiliation_flag:
                affiliations_raw.append(item)
            else:
                title_and_authors.append(item)
        
        affiliations_0 = " ".join(affiliations_raw)        
        affiliations = re.split(r"\,\s(?=\d)", affiliations_0)
        check_aff_list(header[0], affiliations)
        title = []
        raw_authors = []
        authors_flag = False
        for character in title_and_authors:
            if not character.isupper():
                authors_flag = True
            if authors_flag:
                raw_authors.append(character)
            else:
                title.append(character)

        check_empty_lists(header[0], title, raw_authors)
        
        authors = re.split(r"(?<=\d),", "".join(raw_authors))
        
    
    
file.close()
wb.save('TEST_00.xlsx')