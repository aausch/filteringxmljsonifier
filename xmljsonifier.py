import sys
import json
import os
import io

from lxml import etree

from xmlSplit import xmlSplit
from jsonserialize import json_serialize
from argumentparser import parser
from filterprocessor import load_filters
from mrjobxmljsonifier import MrJobXMLJSONifier


cargs = parser.parse_args()


if (cargs.split is not None):
    root_elem = cargs.root if cargs.split_root is None else cargs.split_root

    splitfilesdirectory = xmlSplit(cargs.source, root_elem, 5000)
    with open("splitfiles.tmp", "w") as split_file_list:
      for path, subdirs, files in os.walk(splitfilesdirectory):
        for filename in files:
          f = os.path.join(path, filename)
          split_file_list.write(os.path.join(os.getcwd(), str(f)) + os.linesep)
          #'-r', 'local',
    mr_jsonifier= MrJobXMLJSONifier(
      args=[ '-r', 'local',
             '--jobconf', 'settings.root=' + cargs.root,
             '--jobconf', 'settings.filter=' + cargs.filter,
             '--jobconf', 'settings.destination=' + cargs.destination[0],
             'splitfiles.tmp'])
    with mr_jsonifier.make_runner() as runner:
      runner.run()
    os.remove("splitfiles.tmp")
    sys.exit(0)


# read filter definitions
filters = load_filters(cargs.filter)




#attempts to guess at (and convert into) a builtin type based on a string


context = etree.iterparse(cargs.source, events=('end',), tag=cargs.root)

if cargs.destination is not None:
    with io.open(cargs.destination[0], 'w') as file:
      json_serialize(context,filters,file)
else:
  json_serialize(context, filters, sys.stdout)


