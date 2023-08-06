from genius_lite.core.genius_lite import GeniusLite


class TestSpider(GeniusLite):
    log_config = {'output': r'D:\PythonProjects\genius-lite\tests\logs'}

    def start_requests(self):
        yield self.crawl(
            url='http://poetries1.gitee.io/img-repo/2020/01/23.png',
            parser=self.parse,
        )

    def parse(self, response):
        ...


if __name__ == '__main__':
    spider = TestSpider()
    spider.run()
