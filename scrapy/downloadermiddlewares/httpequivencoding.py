from scrapy.exceptions import NotConfigured


class HttpEquivEncodingMiddleware:
    """
    Obey a ``http-equiv`` header for ``Content-Type`` encoding when the HTTP
    header states another encoding.
    """

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPEQUIVENCODING_ENABLED'):
            raise NotConfigured
        return cls()

    def process_response(self, request, response, spider):
        print("----- PROCESSING RESPONSE!!! -----\n")
        return response
