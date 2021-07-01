import urllib.request


class Connection:
    @staticmethod
    def active_connection():
        try:
            urllib.request.urlopen('http://google.com')
            return True
        except:
            return False
