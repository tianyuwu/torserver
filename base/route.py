#!/usr/bin/env python
# encoding: utf-8

class Route(object):
    """
    把每个URL与Handler的关系保存到一个元组中，然后追加到列表内，列表内包含了所有的Handler
    """

    def __init__(self, prefix=None):
        self.prefix = prefix
        self.urls = list()

    def __call__(self, url, *args, **kwargs):
        def register(cls):
            if self.prefix:
                if url == "/":
                    combine_url = r"/{}".format(self.prefix)
                else:
                    combine_url = r"/{0}{1}".format(self.prefix, url)
            else:
                combine_url = url
            self.urls.append((combine_url, cls))
            return cls

        return register
