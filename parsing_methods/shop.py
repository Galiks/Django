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
