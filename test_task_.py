import re

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
    else:        
        for item in header:
            if re.match(r"^1(?=[A-Z]*[a-z]*)", item):
                affiliation_flag = True
            if affiliation_flag:
                affiliations_raw.append(item)
            else:
                title_and_authors.append(item)
                
        affiliations = re.split(r",(?=\d)", "".join(affiliations_raw))
        title = []
        authors = []
        authors_flag = False
        for character in title_and_authors:
            if not character.isupper():
                authors_flag = True
            if authors_flag:
                authors.append(character)
            else:
                title.append(character)

        check_empty_lists(header[0], title, authors)
    
    
file.close()
