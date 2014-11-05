from argparse import ArgumentParser
from argparse import RawTextHelpFormatter


parser = ArgumentParser(description='''Filters contents of large xml data sources and produces json-ified results''', formatter_class = RawTextHelpFormatter)

parser.add_argument('root', help='''
root XPath element name, used to interpret the filter file against
''')
parser.add_argument('filter', help='''
filter file name, containing column separated filter and map definitions like so:
[XPath], [target json attribute name], [string|int], [force array]
(see sample formatting file included with the source)
''')
parser.add_argument('source', help='''
source xml formatted file
''')
parser.add_argument('--destination', required=False, nargs=1, help='''
file name to store the generated json into; if ommited, will output to stdout
''')

parser.add_argument('--split', required=False, help='''
split the xml file into valid xml files containing elements at root
leaves the split documents in a directory named: [source][timestamp]
performs the json conversion using a mrjob job, running on the split xml
''')

parser.add_argument('--split_root', required=False, help='''
root node to split the xml on, if different from the root node to use when filtering
''')

