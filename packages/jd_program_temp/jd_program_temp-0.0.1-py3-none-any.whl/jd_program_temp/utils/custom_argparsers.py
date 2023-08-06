# -*- coding: utf-8 -*-

import argparse


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        self.functions = {}

        super(ArgumentParser, self).__init__(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        function = kwargs.pop("function") if "function" in kwargs else None
        key = self._get_optional_kwargs(*args, **kwargs).get("dest")
        print('key:%s'%key)
        self.functions[key] = function

        return super(ArgumentParser, self).add_argument(*args, **kwargs)

    def start(self, args=None, namespace=None):
        args = self.parse_args(args=args, namespace=namespace)
        for key, value in vars(args).items():
            if value not in (None, False):
                if callable(self.functions[key]):
                    if value != True:
                        if isinstance(value, list) and len(value) == 1:
                            value = value[0]
                        self.functions[key](value)
                    else:
                        self.functions[key]()

    def run(self, args, values=None):
        if args in self.functions:
            if values:
                self.functions[args](values)
            else:
                self.functions[args]()

        else:
            raise Exception(f"无此方法: {args}")



