import io
import os

from lxml import etree
from mrjob.job import MRJob
from mrjob.compat import get_jobconf_value

from jsonserialize import json_serialize
from filterprocessor import load_filters

class MrJobXMLJSONifier(MRJob):
  def mapper(self, _, line):
    filters = load_filters(get_jobconf_value("settings.filter"))
    context = etree.iterparse(line, events=('end',), tag=get_jobconf_value("settings.root"))
    result_file = line + ".mapped"
    with io.open(result_file, 'w') as file:
      json_serialize(context,filters,file)
    yield("key", result_file)

  def reducer(self, key, file_iterator):
    files = list(file_iterator)

    result_file = get_jobconf_value("settings.destination")
    if result_file is not None:
      with open(result_file, "wb") as outfile:
        for f in files:
          with open(f, "rb") as infile:
              outfile.write(infile.read())
          os.remove(f)
      yield key, result_file
    else:
      for f in files:
        with open(f, "rb") as infile:
          sys.stdout.write(infile.read())




  def steps(self):
    return [self.mr(mapper=self.mapper,reducer=self.reducer)]



if __name__ == "__main__":
    MrJobXMLJSONifier.run()
