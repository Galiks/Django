from parsing_methods.scrapyParsing.scrapyParsing.spiders.arcady_spider import MainClassForScrapy


class Shop:
    name = ''
    discount = ''
    label = ''
    url = ''
    image = ''

    def __init__(self):
        pass

    def __init__(self, name, discount, label, url, image):
        self.name = name
        self.discount = discount
        self.label = label
        self.url = url
        self.image = image

    def __str__(self):
        return '({}, {}{}, {}, {})'.format(self.name, self.discount, self.label, self.image, self.url)


if __name__ == '__main__':
    method = MainClassForScrapy()
    items = method.get_data_from_json()
    for item in items:
        print(item["name"])