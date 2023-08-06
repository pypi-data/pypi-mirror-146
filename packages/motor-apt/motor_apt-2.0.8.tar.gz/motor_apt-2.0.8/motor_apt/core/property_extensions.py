# -*- coding: utf-8 -*-
"""
Created on 22.07.15

Copyright 2015, Alpes Lasers SA, Neuchatel, Switzerland

@author: juraj
"""
class classproperty(property):
    def __get__(self, obj, objtype=None):
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return classmethod(self.fget).__get__(None, objtype)()


class abstractclassproperty(classproperty):
    __slots__ = ()
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        super(abstractclassproperty, self).__init__(fget, fset, fdel, doc)
        if fget is not None:
            fget.__isabstractmethod__ = True
        if fset is not None:
            fset.__isabstractmethod__ = True
        if fdel is not None:
            fdel.__isabstractmethod__ = True
        if doc is not None:
            doc.__isabstractmethod__ = True
    __isabstractmethod__ = True


class staticproperty(property):
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return staticmethod(self.fget).__get__(None, objtype)()


class abstractstaticproperty(staticproperty):
    __slots__ = ()
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        super(abstractstaticproperty, self).__init__(fget, fset, fdel, doc)
        if fget is not None:
            fget.__isabstractmethod__ = True
        if fset is not None:
            fset.__isabstractmethod__ = True
        if fdel is not None:
            fdel.__isabstractmethod__ = True
        if doc is not None:
            doc.__isabstractmethod__ = True
    __isabstractmethod__ = True
