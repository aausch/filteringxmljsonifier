filteringxmljsonifier
=====================

python script for filtering a set of xpaths out of an xml document, and producing json data for them

installation/configuration
===========================

script depends on lxml library - make sure it's available:

* brew install libxml2
* brew install libxslt
* pip install -r requirements.txt 


usage:
======
```
usage: xmljsonifier.py [-h] [--destination DESTINATION] root filter source

Filters contents of large xml data sources and produces json-ified results

positional arguments:
  root                  
                        root XPath element name, used to interpret the filter file against
  filter                
                        filter file name, containing column separated filter and map definitions like so: 
                        [XPath], [target json attribute name], [type], [force array]
                        (see sample formatting file included with the source)
  source                
                        source xml formatted file

optional arguments:
  -h, --help            show this help message and exit
  --destination DESTINATION
                        
                        file name to store the generated json into; if ommited, will output to stdout
                        
```

filter file format
===================
  (look at the test directory for examples)
  
  filter files contain csv data as follows:

  `[Source XPath], [destination property name], [type], <optional: force_array flag>`
  
  ```
  [Source XPath]: 
          an xpath formatted string, used to filter data in the source xml document. if the path is missing or produces no data, contents of the destination property are set to null.

  [destination property name]:
          destination to store the contents of the XPath into, on the produced json object
  [type]:
          any of the builtin python types, to be used when parsing the source data (eg, int, unicode, str)
  <force_array>:
          an optional 4th column. if present, it indicates that the script should present the contents of the xpath as an array - an empty array if there is no data available. note that the script will always produce an array if the XPath resolves to more than one destination.
  ```
