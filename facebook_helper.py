import requests
import re
import settings
import bs4


class FB:

    def __init__(self, username, password):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': settings.user_agent})
        self.user_id = 0
        self.fb_dtsg = ''
        self.login(username, password)

    def login(self, username, password):
        print '[+] Loging in...'

        if not username or not password:
            print '[!] No email or password given'
            return

        response = self.session.get('http://facebook.com/')
        url, datas = self.__getLoginForms(response.content)

        if datas:
            datas['email'] = username
            datas['pass'] = password

            response = self.session.post(url, data=datas)
            self.user_id = self.__findUserId(response.content)
            self.fb_dtsg = self.__findFbDtsg(response.content)

            print '[+] Welcome {0}'.format(self.user_id)
        else:
            print '[!] Login error'

    def __getLoginForms(self, content):
        '''Get the post parameter and the url from the login page.'''

        soup = bs4.BeautifulSoup(content)

        # Get the login form
        form = soup.find('form', id='login_form')
        if form:
            fields = {}

            # Find action url
            url = form.get('action')

            # Find the fields
            for input in form.find_all('input'):
                name = input.get('name')
                value = input.get('value')
                fields[name] = value
            return url, fields
        return None

    def __findUserId(self, content):
        '''Find the user id inside the head tag'''

        user_id = 0
        for line in content.split('\n'):
            if '<head>' in line:
                id_match = re.search('\"user\":\"(\d+)\"', line)
                if id_match:
                    user_id = id_match.group(1)
                break
        return user_id

    def __findFbDtsg(self, content):
        '''Find the fb_dtsg parameter in the source'''
        dtsg = ''

        dtsg_match = re.search(r'name="fb_dtsg" value="(.*?)"', content)
        if dtsg_match:
            dtsg = dtsg_match.group(1)
        return dtsg

    def getStickers(self):
        '''Get the sticker info from the store.'''

        url = 'https://www.facebook.com/stickers/state/store/'
        datas = {'__user': self.user_id,
                 '__a': '1',
                 '__dyn': '7n8ahyj35CCzpQ9UmWOGUGy1m9ACUpxa',
                 '__req': '14',
                 'fb_dtsg': self.fb_dtsg,
                 'ttstamp': '',
                 }
        response = self.session.post(url, data=datas)
        stickers = self.__parseStickerInfo(response.content)
        return stickers

    def __parseStickerInfo(self, content):
        '''Parse informations from the javascript content'''

        stickers = []

        names = re.findall('\"name\":\"(.*?)\"', content)
        names = [name.decode('unicode_escape', name).encode('utf-8')
                 for name in names]

        thumbnails = re.findall('\"thumbnail\":\"(.*?)\"', content)
        thumbnails = [re.sub(r'\\', '', thumbnail) for thumbnail in thumbnails]

        if len(names) == len(thumbnails):
            for i in range(len(names)):
                stickers.append({'name': names[i],
                                 'thumbnail': thumbnails[i]})
            return stickers
        return None
