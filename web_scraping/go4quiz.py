import json
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
from web_scraping.url import Url
from web_scraping.go4quiz_question_getter import Go4QuizQuestionGetter


class Go4Quiz:
    base_url = ''
    sub_urls = []

    def __init__(self, url):
        self.base_url = url

    def main(self):
        """
        this method execute all necessary methods to get all questions from the go4quiz.com page
        """
        self.get_sub_urls()

    def get_sub_urls(self, ):
        """
        get all sub urls of base url.
        :return:
        """

        for value in self.find_urls(self.base_url, class_="sub-menu"):
            self.sub_urls.append(value)

        for url in self.sub_urls:
            temp_urls = self.find_urls(url.url, id='lcp_instance_0')
            for value in temp_urls:
                url.sub_urls.append(value)
        self.get_question_answer()

    def find_urls(self, url, class_=None, id=None):
        """
        get all url and title from a given class or id. And return a list of Url class object.
        :param url:
        :param class_:
        :param id:
        :return map:
        """
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        map = []
        if class_ is not None:
            ul = soup.find('ul', class_=class_)
            for li in ul:
                a = li.find('a')
                if a.has_attr('href'):
                    map.append(Url(a['href'], a.text))
            return map
        elif id is not None:
            ul = soup.find(id=id)
            for li in ul:
                a = li.find('a')
                if a.has_attr('href'):
                    map.append(Url(a['href'], a.text))
            return map
        else:
            return None

    def get_question_answer(self):
        """
        get all question and answer from each url and create a file and store the question and answer in json format
        :return:
        """
        for url in self.sub_urls:
            data = {'url': url.url, 'title': url.title, 'data': []}
            for sub_url in url.sub_urls:
                go4 = Go4QuizQuestionGetter(sub_url.url, sub_url.title)
                go4.main()
                data['data'].append(go4.data)
                print("question scrapped from " + sub_url.url + " done.")
            self.write_to_file(data, url.url)
            print('question scrapped form ' + url.url + " done.")

    def write_to_file(self, data, url):
        """
        write the given data into a file by creating the file and by converting the data into json format
        :param url:
        :param data:
        """
        file_name = self.generate_file_name(url)
        with open(file_name + '.txt', 'w') as json_file:
            json.dump(data, json_file)

    def generate_file_name(self, url):
        """
        generate file name from url and current date by converting it to unix date format
        :param url:
        :return:
        """
        temp = url.split('/')
        date_time = date.today()
        unix = time.mktime(date_time.timetuple())
        if temp[len(temp) - 1]:
            return temp[len(temp) - 1] + "-" + str(unix)
        elif temp[len(temp) - 2]:
            return temp[len(temp) - 2] + "-" + str(unix)
        else:
            return str(unix)
