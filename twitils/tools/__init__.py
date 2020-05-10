from selenium import webdriver


class BrowserSession:
    def __init__(self, given_browser="firefox"):
        self.browser = given_browser
        self.session = None

    def start(self):
        if self.browser == "safari":
            self.session = webdriver.Safari()
        elif self.browser == "chrome":
            self.session = webdriver.Chrome()
        else:
            self.session = webdriver.Firefox()

    def stop(self):
        self.session.close()

    def current(self):
        return self.session

    def update_browser(self, new_browser):
        self.browser = new_browser


session = BrowserSession()
