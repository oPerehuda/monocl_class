import re

def join_authors_affs(authors, affs, poster_number):
    """    this function join authors and their affiliations together    """
    print(f"Poster---{poster_number}")
    print(f"Auth-----{len(authors)}--{type(authors)}{authors}")
    print(f"Affs-----{len(affs)}--{type(affs)}{affs}")
    print("*********************************************************")
    row = []

    for auth in authors:
        pass
        #print('--fn--', auth)

        if auth.count(',') < 1:
            pass
            print('====IND  FN  ITEM----', auth.strip())
            index02 = auth.strip()[-2:]
            index01 = auth.strip()[-1]
            if index02.isdigit():                                
                #print(index02, '--index02--', auth[:-2].strip(), '---', affs[(int(index02)-1)].strip()[2:].strip())
                row.append([auth[:-2].strip(), affs[(int(index02)-1)].strip()[2:].strip()])

                # if index02 != affs[(int(index02)-1)].strip()[:2] and poster_number not in row:
                #     #print('COUNTER2----', index02, affs[(int(index02)-1)].strip()[:2])
                #     row.insert(0, (poster_number))
                #     row.insert(0, ('Two---'))

            elif index01.isdigit():
                #print(index01, '--index01--', auth.strip()[:-1].strip(), '---', affs[(int(index01)-1)].strip()[1:].strip())
                row.append([auth.strip()[:-1].strip(), affs[(int(index01)-1)].strip()[1:].strip()])

                if index01 != affs[(int(index01)-1)].strip()[:1] and poster_number not in row:
                    #print('COUNTER1----', index01, affs[(int(index01)-1)].strip()[:1])
                    row.insert(0, (poster_number))
                    row.insert(0, ('One---'))

            else:
                print('WRONG INDEX NUMBER!!!!!-----', auth.strip(), '-- no individual affiliations --')
                row.append([auth.strip(), ''])
                # if poster_number not in row:
                #     row.insert(0, (poster_number))
                #     row.insert(0, ('Zero---'))

        else:
            print(f"+++ MULT  FN  AFF +++{auth.count(',')}--{auth}")
            multiple_aff = []
            multiple_aff_splitter = '\,'

            for ind_item in re.split(multiple_aff_splitter, auth.strip()):
                #print('==========IND ITEM----', ind_item)

                index22 = ind_item.strip()[-2:]
                index21 = ind_item.strip()[-1:]

                if len(ind_item.strip()) > 1:
                    if index22.isdigit():
                        multiple_aff.append(affs[(int(index22)-1)].strip()[2:].strip())
                        if index22 != affs[(int(index22)-1)].strip()[:2].strip() and poster_number not in row:
                            row.insert(0, ('Multiple---' + poster_number))
                    elif index21.isdigit():
                        multiple_aff.append(affs[(int(index21)-1)].strip()[1:].strip())
                        if index21 != affs[(int(index21)-1)].strip()[:1].strip() and poster_number not in row:
                            row.insert(0, ('Multiple---' + poster_number))
                elif len(ind_item.strip()) == 1:
                    if index21.isdigit():
                        multiple_aff.append(affs[(int(index21)-1)].strip()[1:].strip())#
                        if index21 != affs[(int(index21)-1)].strip()[:1].strip() and poster_number not in row:
                            row.insert(0, ('Multiple---' + poster_number))
                else:
                    print('WRONG MULTIPLE INDEX ---')
                    # time.sleep(2)
                    # row.insert(0, (poster_number))
                    # row.insert(0, ('Multiple---'))

            #print(re.split('\,', auth.strip())[0].strip()[:-1].strip().strip('1').strip('2').strip('3').strip(), '%%%%%%%%%%%%%%4444444%%%%%%%%%%%%%', ' ___ '.join(multiple_aff))#.strip('1').strip('2').strip('3').replace('*', '')
            row.append([re.split('\,', auth.strip())[0].strip()[:-1].strip().strip('1').strip('2').strip('3').strip(), ' ___ '.join(multiple_aff)])#.strip('1').strip('2').strip('3').replace('*', '')

        #print("-----------------------------------------------------------")

    return row