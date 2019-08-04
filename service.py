import requests
import shutil
import os
import bs4
import re
import sys

def get_html_from_web():
    url = input("Enter your url (Working only with coursehunter.net) : ")
    try:
        url1 = url.replace("https://coursehunters.net", "https://coursehunter.net")
        url2 = url1.replace("https://coursehunter.net", "https://dev.coursehunters.net")
        response1 = requests.get(url1)
        response2 = requests.get(url2)
        responses = response1.text, response2.text
    except requests.exceptions.MissingSchema:
        print("Your URL is wrong. Please check it")
        os.system('pause')
        sys.exit()
    return responses

def get_data_from_html(html):
    """
    Get movie links and movie names
    Need to add exceptions and conditions
    """
    html1 = html[0]
    html2 = html[1]
    try:
        soup1 = bs4.BeautifulSoup(html1, 'html.parser')
        soup2 = bs4.BeautifulSoup(html2, 'html.parser')
        lessons1 = soup1.find("div", {"class" : "course-wrap-side-right"})
        lessons2 = soup2.find("div", {"class" : "course-wrap-side-right"})
        les1 = str(lessons1) #lessons1(str)
        les2 = str(lessons2)
        les1 = re.search("value\">([0-9]+)\sВидео", les1)
        les2 = re.search("value\">([0-9]+)\sВидео", les2)
        count1, count2 = "", ""
        count1 = les1.group(1)
        if count1 == "":
            raise AttributeError

        count2 = les2.group(1)
        if count2 == "":
            raise AttributeError
        #работаем с count1 и с count2
    except AttributeError:
        if count1 == "":
            try:
                count2 = les2.group(1) 
                return FindLinks(soup2) #работаем с count2
            except:
                if count2 == "":
                    pass #exit
        elif count2 == "":
            return FindLinks(soup1) #работаем с count1
    if(int(count1) > int(count2)):
        return FindLinks(soup1, 1, soup2) #работаем с count1, если нельзя, то с count2
    elif(int(count1) <= int(count2)):
        return FindLinks(soup2, 1, soup1) #работаем с count2, если нельзя, то с count1

def FindLinks(soup, flag = 0, extra_soup = None):
    try:
        lessons = soup.find_all("li", {"class" : "lessons-item"})
        if(lessons == [] or lessons == None):
            raise AttributeError
        my_list = []
        for lesson in lessons:
            text = str(lesson)
            result_link = re.search("https://vs(.+)mp4", text)
            result_name = re.search("\"lessons-name\">(.+)</div>", text)
            my_map = {"link" : result_link.group(), "name" : result_name.group(1)}
            my_list.append(my_map)
    except AttributeError:
        if(flag == 0):
            print("Program cannot download this course.")
            print("He's paid anyway.")
            print("Better try to find this course in Google :-)")
            os.system('pause')
            sys.exit()
        elif(flag == 1):
            my_list = FindLinks(extra_soup)
    return my_list

def save_movie(folder, data):
    for i in range(len(data)):
        my_data = get_data_from_url(data[i]['link'])
        print('Downloading lesson {}'.format(i + 1))

        new_data = data[i]['name']
        new_data = re.sub('[^a-zA-Z0-9а-яА-Я \n\.]','_',new_data)
        file_name = os.path.join(folder, (str)(i + 1) + '_' + new_data + '.mp4')
        with open(file_name, 'wb') as fout:
            shutil.copyfileobj(my_data, fout)
    print('done!')


def get_data_from_url(url):
    responce  = requests.get(url, stream = True)
    return responce.raw
        
