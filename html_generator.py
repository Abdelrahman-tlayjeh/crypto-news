def generate_head(title:str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
    """

def add_style(style:str) -> str:
    return f"""<style>
    {style}
    </style>
    """

def generate_body(body_code:str) -> str:
    return f"""<body>
    {body_code}
    </body>
    """

def generate_header(normal_word, bold_word, date) -> str:
    return f"""<header>
        <h1>{normal_word}<span id="news-decor">{bold_word}</span></h1>
        <h3 id="generation-date">{date}</h3>
    </header>"""

def generate_navigator(titles:'list|tuple') -> str:
    html = """<div class="navigator">\n<ul>\n"""
    for t in titles:
        t2 = t.lower()
        html += f"<li><a href='#{'-'.join(t2.split())}'>{t}</a></li>\n"
    html += "</ul>\n</div>"
    return html

def generate_top_news_section(news:list[dict]) -> str:
    """
    news: list of dict, each dict must have 'title', 'description', 'author', 'date', and 'link'
    """
    html = """<section id="top-news">
        <h2 class="section-title">Top News</h2>"""
    for n in news:
        html += f"""
        <div class='new-container'>
            <h3 class='title'>{n["title"]}<span class="link"><a target="_blank" href="{n["link"]}">→</a></span></h3>
            <h5 class='description'>{n['description']}</h5>
            <div class='author-and-date'>
                <span class='author'>{n['author']}</span>
                <span class='date'>{n['date']}</span>
            </div>
        </div>
        \n
        """
    html += "</section>"
    return html

def generate_trending_news(topic:str, news:list[dict]) -> str:
    """
    topic: little string (only one word) about the topic(like bitcoin, ethereum, etc...) 
    news: list of dict, each dict must have 'title', 'date', 'tags', and 'link'
    """
    html = f"""<div id='{topic.lower()}'>
    <h2><u>{topic}</u><span class="link"><a href="#top-news">↑</a></span></h2>"""
    for n in news:
        tags = ""
        if n["tags"]:
            for t in ["#"+tag for tag in n["tags"]]:
                tags += f"<span class='tag'>{t}</span>\n"
            # tags = " ".join(["#"+tag for tag in n["tags"]])
        html += f"""
        <div class='new-container'>
            <h3 class='title'>{n["title"]}<span class="link"><a target="_blank" href="{n["link"]}">→</a></span></h3>
            <div class='date-and-tags'>
                <p class='date'>{n['date']}</p>
                <p class='tags'>
                    {tags}
                </p>
            </div>
        </div>
        \n
        """
    html += "</div>\n"
    return html

def generate_trending_news_section(navigator_code:str, inner_code:str) -> str:
    html = """<section id="trending-news">
        <h2 class="section-title">Trending News</h2>"""
    html += navigator_code
    html += inner_code + "\n</section>"
    return html

def generate_prices_section(table_code):
    return f"""<section id="crypto-prices">
    <h2 class="section-title">Crypto Info<h2>
    {table_code}
    </section>
    """

def generate_footer(date_time):
    return f"""<footer>
        <h4>Generated in {date_time} by crypto-news-generator script <a href="https://github.com/Abdelrahman-tlayjeh">https://github.com/Abdelrahman-tlayjeh</a></h4>
    </footer>"""
