import firefox_cookies
import firefox_finder
import chrome_cookies

def get_cookie_jar():
    firefox_path = firefox_finder.get_profile_dir()
    if None != firefox_path:
        return firefox_cookies.get_cookie_jar()

    chrome_path = chrome_cookies.get_cookie_file()
    if None != chrome_path:
        return chrome_cookies.get_cookie_jar()

    return None

