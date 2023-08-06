import feapder

class Test(feapder.AirSpider):
    def start_requests(self):
        yield feapder.Request("https://www.baidu.com")

    def parse(self, request, response):
        print(response)
        1/0

    def failed_request(self, request, response):
        print(111111111)
        yield request

Test().start()