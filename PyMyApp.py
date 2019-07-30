import os

import service

def main():
    
    print_the_header()
    
    data = get_or_create_output_folder()

    print_func(data)


    download_videos(data['full_path'])

def print_the_header():
    print("----------------------------------")
    print("          CAT FACToRY")
    print("----------------------------------")

def get_or_create_output_folder():
    flag =  False
    text1 = 'Found folder {}'
    text2 = 'In processing...'
    text3 = ''
    text_list = [text1, text2, text3]
    
    base_folder = os.path.dirname(__file__)
    folder = input("Enter your directory ")
    full_path = os.path.join(base_folder, folder)
    text_list[0] = text1.format(full_path)

    if not os.path.exists(full_path) or \
        not os.path.isdir(full_path):
            text_list[2] = 'Creating new directory at {}'.format(full_path)
            os.mkdir(full_path)
            flag = True

    return {'full_path' : full_path, 'flag' : flag, 'text_list' : text_list}

def print_func(data):
    print(data['text_list'][0] if not data['flag'] else data['text_list'][2])
    print(data['text_list'][1])
    print()

def download_videos(folder):
    html = service.get_html_from_web()
    data = service.get_data_from_html(html)
    service.save_movie(folder, data)

if __name__ == '__main__':
    print('App launch from main file')
    main()

