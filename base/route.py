#!/usr/bin/env python
# encoding: utf-8

class Route(object):
    """
    把每个URL与Handler的关系保存到一个元组中，然后追加到列表内，列表内包含了所有的Handler
    """

    def __init__(self):
        self.urls = list()

    def __call__(self, url, *args, **kwargs):
        def register(cls):
            self.urls.append((url, cls))
            return cls

        return register
