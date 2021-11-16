import os
from io import StringIO

import yaml

__author__ = 'alea'


class DictGetter(object):
    """
    Convenience wrapper for dict / list
    or any object that has __getitem__ implemented

    More or less translates __getattr__ to __getitem__
    And __setattr__ to __setitem__

    """
    wrapable_types = [dict, list]

    def __init__(self, dval):
        self.dictv = dval

    def __setitem__(self, key, value):
        self.dictv[key] = value

    def __setattr__(self, key, value):
        # temp fix
        if key == 'dictv':
            self.__dict__[key] = value
        else:
            self.dictv[key] = value

    def __getattr__(self, item):
        if item in self.dictv:
            if type(self.dictv[item]) in self.wrapable_types:
                return DictGetter(self.dictv[item])
            else:
                return self.dictv[item]
        return None

    def __iter__(self):
        for k, v in self.dictv.iteritems():
            yield (k, getattr(self, k))

    def __contains__(self, item):
        return item in self.dictv

    def get(self):
        return self.dictv


class YamlFileConfiguration(DictGetter):

    def __init__(self, cpath):
        with open(cpath, 'r') as fp:
            super(YamlFileConfiguration, self).__init__(yaml.load(fp, yaml.FullLoader))


class YamlConfiguration(DictGetter):
    def __init__(self, str):
        super(YamlConfiguration, self).__init__(yaml.load(StringIO(str)))


def get_root_dir(depth, path=__file__):
    rdir = os.path.dirname(os.path.realpath(path))
    for i in range(depth):
        rdir = os.path.dirname(rdir)
    return rdir


def load_dir(path):
    if not os.path.exists(path):
        raise Exception("Can't find config directory - {0} !".format(path))
    ret = {}
    # Config loader
    for fullname in os.listdir(path):
        fname, ext = os.path.splitext(fullname)
        if ext == ".yaml":
            # print("Loading {0} configuration file ...".format(fullname))
            ret[fname] = YamlFileConfiguration(path + fullname)
    return DictGetter(ret)


CONFIG = load_dir(get_root_dir(1) + '/storage/config/')
CONF = config = CONFIG
