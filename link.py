class Link(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return str(dir(self))
        #for attr in Zir(self):
        #return f'Link: {self.link}; visited: {self.visited}; {self.test}'
