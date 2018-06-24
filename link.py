class Link(object):
    def __init__(self, link, visited):
        self.link = link
        self.visited = visited

    def __str__(self):
        return f'Link: {self.link}; visited: {self.visited}'
