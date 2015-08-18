import os
import random

from scrapy.conf import settings

class RandomUserAgentMiddleware(object):
    def process_request(self, request,spider):
        userAgent = random.choice(settings.get('USER_AGENT_LIST'))
        if userAgent:
            request.headers.setdefault("User-Agent", userAgent)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get("HTTP_PROXY")

