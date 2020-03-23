class TourInfo:
    title = ''
    price = ''
    area  = ''
    link  = ''
    img   = ''
    contents = ''

    def __init__(self, title, price, area, link, img, contents=None ):
        self.title = title
        self.price = price
        self.area  = area
        self.link  = link
        self.img   = img
        self.contents = contents