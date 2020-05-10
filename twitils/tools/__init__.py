browser = None


def start_session(driver):
    global browser
    browser = driver


def stop_session():
    browser.close()


def get_session():
    return browser
