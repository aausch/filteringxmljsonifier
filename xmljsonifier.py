import sys
import csv
import json
import io

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from copy import deepcopy
from collections import namedtuple
from lxml import etree

Filter = namedtuple("Filter", "XPath jsonattr type force_array")

parser = ArgumentParser(description='''Filters contents of large xml data sources and produces json-ified results''', formatter_class = RawTextHelpFormatter)

parser.add_argument('root', help='''
root XPath element name, used to interpret the filter file against
''')
parser.add_argument('filter', help='''
filter file name, containing column separated filter and map definitions like so: 
[XPath], [target json attribute name], [type], [force array]
(see sample formatting file included with the source)
''')
parser.add_argument('source', help='''
source xml formatted file
''')
parser.add_argument('--destination', required=False, nargs=1, help='''
file name to store the generated json into; if ommited, will output to stdout
''')


args = parser.parse_args()

# read filter definitions
filters = []
with open(args.filter, 'rb') as csvfile:
    filterreader = csv.reader(csvfile, delimiter='|')
    for row in filterreader:
        result = Filter(
            XPath = row[0].strip(), 
            jsonattr=row[1].strip(), 
            type=row[2].strip(), 
            force_array=len(row) > 3)
        filters.append(result)


def fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
    del context

#attempts to guess at (and convert into) a builtin type based on a string
def convert_type(value, type_):
    import importlib
    #assuming built in type
    module = importlib.import_module('__builtin__')
    cls = getattr(module, type_)
    return cls(value)

def json_serialize(elem, outstream):
    result = {}
    for f in filters:
        xp = etree.XPath(f.XPath) 
        children = xp(elem)
        attr_val = []
        for c in children:
            raw_val =  c.text if (type(c) is etree._Element)  else c
            attr_val.append (convert_type(raw_val, f.type))
        if not f.force_array and len(children) < 2 and len(attr_val) > 0:
            attr_val = attr_val[0]
        elif len(attr_val) == 0:
            attr_val = None
        result[f.jsonattr] = attr_val
    if result is not None and len(result) > 0:
        outstream.write(unicode(json.dumps(result)))
        outstream.write(u'\n') #easier on the eyes


context = etree.iterparse(args.source, events=('end',), tag=args.root)

if args.destination is not None:
    with io.open(args.destination[0], 'w') as file:
        fast_iter(context, 
            lambda elem:
                json_serialize(elem, file))
else:
    fast_iter(context, 
       lambda elem:
           json_serialize(elem, sys.stdout))


