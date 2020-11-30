# Scrapy settings for lesson5 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lesson5'

SPIDER_MODULES = ['lesson5.spiders']
NEWSPIDER_MODULE = 'lesson5.spiders'


USER_AGENT = 'lesson5 (+https://parsemachine.com)'
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1
