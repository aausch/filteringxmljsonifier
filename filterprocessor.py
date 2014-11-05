import csv
import io
import os

from collections import namedtuple

Filter = namedtuple("Filter", "XPath jsonattr type force_array")



def load_filters(filterFileName):
  with open(filterFileName, 'rb') as csvfile:
    filters = []
    filterreader = csv.reader(csvfile, delimiter='|')
    for row in filterreader:
        result = Filter(
            XPath = row[0].strip(),
            jsonattr=row[1].strip(),
            type=row[2].strip(),
            force_array=len(row) > 3)
        filters.append(result)
    return filters
