import requests
from bs4 import BeautifulSoup

class Go4QuizQuestionGetter:
    url = ''
    data = {
    }

    def __init__(self, url, title):
        self.url = url
        self.data['url'] = url
        self.data['title'] = title

    def main(self):
        """" this is the main method of this class all necessary steps taken in this method. Or it is the main entry
        of this class.
        """
        soup = BeautifulSoup(self.get_content(), 'html.parser')
        divs = self.get_main_div(soup)
        for div in divs:
            length = len(self.data) - 2
            answers = self.get_answers(div)
            self.data[length] = [{'question': div.text}, {'answers': answers}]

    def get_content(self):
        """
         it returns the content (html file) from the given url.
        """
        content = requests.get(self.url).content
        return content

    def get_main_div(self, suop):
        """
        it returns the html tags the contain the given class name.
        """
        return suop.find_all('div', class_="rq_panel")

    def get_answers(self, div):
        """
        get all answer of a specific question
        """
        div_lists = self.get_lists(div)
        answers = {}
        for li in div_lists:
            try:
                li.attrs["data-correct"]
                correct = True
            except KeyError:
                correct = False
            label = li.find_all('label')
            if label:
                answer = label[0].text
                answers[len(answers)] = {'answer': answer, 'correct': correct}
        return answers

    def get_lists(self, div):
        """
        get all list of tags that contain answer of a specific question.
        """
        return div.find_all('li')


