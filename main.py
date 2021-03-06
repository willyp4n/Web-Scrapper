import argparse
import logging
import new_page_objects as news  #se le da el alias news
import re

from requests.exceptions import HTTPError
from urllib3.exceptions  import MaxRetryError

logging.basicConfig(level=logging.INFO)
is_well_formed_link = re.compile(r"^https?://.+/.+$") #https://example.com/hello  ^ = inicializa  $ = indica que termina
is_root_path = re.compile(r"^/.+$") # /some-text   .+ = que tenga una o mas letras 

from common import config

logger = logging.getLogger(__name__)

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return "{}{}".format(host, link) #retorne el host y el link 
    else:
        return "{host} / {uri}".format(host=host, uri= link) # otra forma de escribirlo

def _fetch_article(news_site_uid, host, link):
    logger.info("Start fetching article at{}".format(link))

    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning("Error while fetching the article", exc_info=False)
    
    if article and not article.body:
        logger.warning("invalid article. There is no body")
        return None
    
    return article

def _news_scraper(news_site_uid):
    host = config()["news_sites"][news_site_uid]["url"]

    logging.info("Beginning scraper for {}".format(host))
    homepage = news.HomePage(news_site_uid, host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)
        
        if article:
            logger.info("Article fetched!!")
            articles.append(article)
            print(article.title)

    print(len(article))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    news_site_choices = list(config()["news_sites"].keys())
    parser.add_argument("news_site",
                        help="The news site that you want to scrape",
                        type= str,
                        choices= news_site_choices)
    
    args = parser.parse_args()
    _news_scraper(args.news_site)
