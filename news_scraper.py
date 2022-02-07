from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

URL = "https://www.coindesk.com/"
CHROME_DRIVER = "chromedriver\chromedriver.exe"

print("Initializing a virtual Automated browser...")
options = Options()
options.headless = True
user_agent =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")
# options.add_argument("--dns-prefetch-disable")
# options.add_argument("--ignore-certificate-errors")
# options.add_argument("--ignore-ssl-errors")
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument("disable-infobars")
options.add_experimental_option('excludeSwitches', ['enable-logging'])      #hide Chrome console output
prefs = {"profile.default_content_setting_values":{
    "images": 2     #block images
}}
options.experimental_options["prefs"] = prefs

driver = webdriver.Chrome(CHROME_DRIVER, options=options)

print("Getting web page (this may take time!)...")
try:
    driver.get(URL)
except TimeoutException as e:
    print("Yalla Henet...")
    driver.refresh()

print("Saving page source code...")
source_code = driver.page_source
driver.quit()

    
def get_optional_data(func):
    """scrape elements that can/or not exist"""
    try:
        return func()
    except AttributeError:
        return ""

def get_top_news(soup):
    top_news_containers = [cont.find("div", class_="article-cardstyles__AcTitle-q1x8lc-1 bwXBTf") for cont in soup.find_all("div", class_="article-cardstyles__Block-q1x8lc-3 JbQgO")]
    top_news = []
    for c in top_news_containers:
        #headline and link
        title = c.find("a", class_="headline")
        link = URL + title["href"]
        title = title.text
        #description
        description = get_optional_data(lambda: c.find("p", class_="typography__StyledTypography-owin6q-0 lkUGSO").find("span").text)
        #author and publish date
        author = get_optional_data(lambda: c.find("div", class_="ac-authors").find("span", class_="typography__StyledTypography-owin6q-0 cwwpzS").text)
        date = c.find("div", class_="timing-data").find("span", class_="typography__StyledTypography-owin6q-0 dHSCiD").text
        #collect data
        top_news.append({"title": title, "description": description, "author": author, "date": date, "link": link})
    return top_news

#get trending news
def get_trend_tab_news(soup):
    containers = soup.find_all("div", class_="article-cardstyles__AcTitle-q1x8lc-1 bwXBTf")
    trend_news = []
    for c in containers:
        #headline and link
        title = c.find("a", class_="headline")
        link = URL + title["href"]
        title = title.text
        #publish date
        date = c.find("div", class_="timing-data").find("span").text
        #tags
        try:
            tags = [t.find("span", class_="ac-tag").text for t in c.find("div", class_="ac-tags").find_all("span", class_="article-cardstyles__TagLink-q1x8lc-5 hdoCjT")]
        except AttributeError:
            tags = []
        #collect data
        trend_news.append({"title": title, "date": date, "tags": tags, "link": link})
    return trend_news

all_trends = []
def get_all_trends(soup:BeautifulSoup):
    global all_trends
    domain = ["BTC", "ETH", "Investing", "Industry", "Trading"]
    for i in range(5):
        tab = soup.find("div", attrs={"role": "tabpanel", "value": str(i)})
        all_trends.append({domain[i]: get_trend_tab_news(tab)})
    return all_trends

def scrape_news() -> dict[str, list]:
    """return:
    {'top news': [
        {'title': '\\\', 'description': '\\\', 'author': optional('\\\'), 'date': '\\\', 'link': '\\\'}.
        ...
    ],
    'trending news': [
        {'BTC': [
            {'title': '\\\', 'date': '\\\', tags: optional([\\, \\ ,\\, ...]), 'link': '\\\'},
            ...
        ]},
        {'ETH': [
            {'title': '\\\', 'date': '\\\', tags: optional([\\, \\ ,\\, ...]), 'link': '\\\'},
            ...
        ]},
        {'Investing': [
            {'title': '\\\', 'date': '\\\', tags: optional([\\, \\ ,\\, ...]), 'link': '\\\'},
            ...
        ]},
        {'Industry': [
            {'title': '\\\', 'date': '\\\', tags: optional([\\, \\ ,\\, ...]), 'link': '\\\'},
            ...
        ]},
        {'Trading': [
            {'title': '\\\', 'date': '\\\', tags: optional([\\, \\ ,\\, ...]), 'link': '\\\'},
            ...
        ]}
    ]}
    """
    print("Scraping data...")
    soup = BeautifulSoup(source_code, "lxml")
    return {"top news": get_top_news(soup), "trending news": get_all_trends(soup)}


if __name__ == "__main__":
    print(scrape_news())