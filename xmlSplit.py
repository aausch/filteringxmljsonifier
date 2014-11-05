import io
import os
import time

from lxml import etree
from lxml.etree import tostring

def create_and_set_output_dir (name):
    output_directory = name + time.strftime("%Y%m%d-%H%M%S")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return output_directory

def fast_iter(context, batch_size, output_directory, func):
    batch = 0
    count = 0

    for event, elem in context:
        if count == 0:
            with io.open(os.path.join(output_directory, str(batch)), 'a') as outstream:
                outstream.write(u'<split_root>\n')
        func(elem, batch)
        elem.clear()
        count = count + 1
        if count == batch_size:
            with io.open(os.path.join(output_directory, str(batch)), 'a') as outstream:
                outstream.write(u'\n</split_root>')
            batch = batch + 1
            count = 0
    if count > 0:
      with io.open(os.path.join(output_directory, str(batch)), 'a') as outstream:
                outstream.write(u'\n</split_root>')
    del context

def dump_to_file(elem, output_directory, batch):
    with io.open(os.path.join(output_directory, str(batch)), 'a') as outstream:
        outstream.write(unicode(tostring(elem, with_tail=False)))

def xmlSplit(xmlFileName, root, batch_size):
    output_directory = create_and_set_output_dir(xmlFileName)
    context = etree.iterparse(xmlFileName, events=('end',), tag=root)
    fast_iter(context, batch_size, output_directory,
            lambda elem, count:
                dump_to_file(elem, output_directory, count))
    return output_directory
