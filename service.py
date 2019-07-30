import requests
import shutil
import os
import bs4
import re

def get_html_from_web():
    url = input("Enter your url (Working only with coursehunter.net) : ")
    url = url.replace("https://coursehunters.net", "https://dev.coursehunters.net")
    responce = requests.get(url)
    return responce.text

def get_data_from_html(html):
    """
    Get movie links and movie names
    Need to add exceptions and conditions
    """
    soup = bs4.BeautifulSoup(html, 'html.parser')
    lessons = soup.find_all("li", {"class" : "lessons-item"})
    my_list = []
    for lesson in lessons:
        text = str(lesson)
        result_link = re.search("https://vs1(.+)mp4", text)
        result_name = re.search("\"lessons-name\">(.+)</div>", text)
        my_map = {"link" : result_link.group(), "name" : result_name.group(1)}
        my_list.append(my_map)

    return my_list

def save_movie(folder, data):
    for i in range(len(data)):
        my_data = get_data_from_url(data[i]['link'])
        print('Downloading lesson {}'.format(i + 1))

        new_data = data[i]['name']
        new_data = re.sub('[^a-zA-Z0-9 \n\.]','_',new_data)
        file_name = os.path.join(folder, (str)(i + 1) + '_' + new_data + '.mp4')
        with open(file_name, 'wb') as fout:
            shutil.copyfileobj(my_data, fout)
    print('done!')


def get_data_from_url(url):
    responce  = requests.get(url, stream = True)
    return responce.raw
        
