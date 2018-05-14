from bs4 import BeautifulSoup
import shutil
import json
import numpy as np
import requests
from PIL import Image
from matplotlib import cm
from pytesseract import image_to_string, pytesseract

class Instagram:
    ITEMS_PER_PAGE = 10

    def __init__(self, username, hashtag):
        self.html = requests.get('https://www.instagram.com/{}'.format(username)).text
        self.json_data = json.loads(self.__getJSON())

        self.lastpost = self.__getLastPost(hashtag)

        self.timestamp = self.lastpost[2]
        self.image_link = self.lastpost[1]
        self.text = self.lastpost[0]

        self.title = self.__getTitle(self.__downloadImage(self.image_link))


    def __getJSON(self):
        # Create new BS Object
        soup = BeautifulSoup(self.html, 'html.parser')

        # Find all scripts and get third
        script = soup.findAll('script', {'type': 'text/javascript'})[2].text

        # Remove JavaScript's code
        script = list(script.replace('window._sharedData = ', ''))
        script.pop(len(script) - 1)

        # Put all list objects into one string
        temp = ""
        for i in script:
            temp += i

        # Return JSON String
        return temp

    def __getTitle(self, image):    #Enable show() only in debug
        # Tesseract dir
        pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

        # Original image
        image = Image.open(image)

        # Crop the original image to title's zone
        cropped = image.crop((0, 250, image.size[1], 750))
        # cropped.show()

        # Binarize the cropped image
        binarized = cropped.convert('L')
        # binarized.show()

        #Optimize image for OCR boosting
        data = np.asanyarray(binarized)
        boh = (data > 230) * 1.0

        backimage = Image.fromarray(cm.gist_earth(boh, bytes=True))
        # backimage.show()

        text = image_to_string(backimage, lang='ita')
        return text

    def __downloadImage(self, link):
        filename = link.split('/')[-1]
        r = requests.get(link, stream=True)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return filename

    def __getLastPost(self, hashtag):
        res = list(range(3))
        for i in range(self.ITEMS_PER_PAGE):
            text = self.json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
            timestamp = self.json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['taken_at_timestamp']
            imglink = self.json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['display_url']

            if hashtag in text:
                res[0] = text
                res[1] = imglink
                res[2] = timestamp
                return res

    def getAll(self):
        return [self.title, self.timestamp, self.image_link, self.text]