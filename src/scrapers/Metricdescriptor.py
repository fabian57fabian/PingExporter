class Metricdescriptor(object):

    def __init__(self, _id: str, _desc: str):
        self.id: str = _id
        self.description: str = _desc
        self.metric_prometheus = None
