from news_scraper import scrape_news
from crypto_prices_scraper import get_crypto_info
from html_generator import *
from datetime import datetime, date

#-----Scrape News(from coindesk)-------->
news = scrape_news()

#-------Scrape top 25 Crypto info(coinmarkercap)---------->
info = get_crypto_info(25)

#------generate Web Page(html)-------------->
#Get style(CSS)
with open("css_style.css", "r") as f:
    style = f.read()
#var that will contain all the source code
html_code = ""
print("Generating the News Web Page...")
#head
html_code += generate_head(f"Crypto news {datetime.now()}")
#add style
html_code += add_style(style)
#header and navigation section
html_code += generate_header("Crypto", "News", str(date.today()))
html_code += generate_navigator(["Top News", "Trending News", "Crypto Prices"])
#top news section
html_code += generate_top_news_section(news["top news"])
#trending news section
trend_code = ""
for n in news["trending news"]:
    topic = list(n.keys())[0]
    trend_code += generate_trending_news(topic, n[topic])
html_code += generate_trending_news_section(generate_navigator(["BTC", "ETH", "Investing", "Industry", "Trading"]), trend_code)
#crypto info section
html_code += generate_prices_section(info)
#footer
html_code += generate_footer(datetime.now())
#saving html page
with open(f"News\\{date.today()}_news.html", "w", encoding="utf-8") as f:
    f.write(html_code)
print("Web page Successfully generated!")