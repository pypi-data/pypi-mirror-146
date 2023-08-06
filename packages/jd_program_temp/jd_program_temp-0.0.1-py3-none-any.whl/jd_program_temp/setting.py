import os


class BaseUrlSource(object):

    def init_setting_source(self):

        pass

    def parse_setting_url(self):

        pass

    @property
    def name(self):
        return self.__class__.__name__

    def close(self):
        pass

############# 导入用户自定义的url_source #############
try:
    print('load_sourc++++++e')
    from url_source import *

except:
    print('__init_error')