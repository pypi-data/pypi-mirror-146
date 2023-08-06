from genius_lite.core.genius_lite import GeniusLite


class TestSpider(GeniusLite):
    log_config = {'output': r'D:\PythonProjects\genius-lite\tests\logs'}

    def start_requests(self):
        yield self.crawl(
            url='https://www.baidu.com',
            parser=self.parse,
            params={'foo': 1, 'bar': 2},
            timeout=3,
        )
        yield self.crawl(
            url='https://www.baidu.com',
            parser=self.parse,
            params={'bar': 2, 'foo': 1},
            timeout=3,
        )

    def parse(self, response):
        self.logger.debug('response')
        self.logger.warning('response')
        self.logger.error('response')
        # for i in range(3, 5):
        #     yield self.crawl(
        #         url='https://www.baidu.com',
        #         parser=self.parse2,
        #         params={'foo': i},
        #         timeout=3,
        #     )

    def parse2(self, response):
        # self.logger.debug(response.payload)
        pass


if __name__ == '__main__':
    spider = TestSpider()
    spider.run()
