import json
import importlib

from lxml import etree

def fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
    del context

def convert_type(value, type_):
    #assuming built in type
    module = importlib.import_module('__builtin__')
    cls = getattr(module, type_)
    return cls(value)


def inner_json_serialize(elem, filters, outstream):
    result = {}
    for f in filters:
        xp = etree.XPath(f.XPath)
        children = xp(elem)
        attr_val = []
        for c in children:
            raw_val =  c.text if (type(c) is etree._Element)  else c
            attr_val.append ( convert_type(raw_val, f.type) )
        if not f.force_array and len(children) < 2 and len(attr_val) > 0:
            attr_val = attr_val[0]
        elif len(attr_val) == 0:
            attr_val = None
        result[f.jsonattr] = attr_val
    if result is not None and len(result) > 0:
        outstream.write(unicode(json.dumps(result)))
        outstream.write(u'\n')


def json_serialize(context,filters,outstream):
  fast_iter(context,
    lambda elem:
      inner_json_serialize(elem, filters, outstream))
