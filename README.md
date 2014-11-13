filteringxmljsonifier
=====================
* convert xml document to json
* filter for specific xpaths
* define a specifc target json schema 
* optionally split the xml document into smaller chunks first, and process the chunks in parallel
* very fast; very memory efficient; should be able to quickly handle gb to tb sized files

tested exclusively on osx

installation/configuration
===========================

script depends on lxml library - make sure it's available:

* brew install libxml2
* brew install libxslt
* pip install -r requirements.txt 

sample run
===========
serial processing:
* edit test/test_ClinVarFullRelease_2014_corrected.sh - uncomment the curl and gunzip commands
* `cd test`
* `./test_ClinVarFullRelease_2014_corrected.sh`

parallel processing using mrjob:
* edit test/test_ClinVarFullRelease_2014_split.sh - uncomment the curl and gunzip commands
* `cd test`
* `./test_ClinVarFullRelease_2014_corrected.sh`

usage:
======
bash> python xmljsonifier.py -h
```
usage: xmljsonifier.py [-h] [--destination DESTINATION] [--split SPLIT]
                       [--split_root SPLIT_ROOT]
                       root filter source

Filters contents of large xml data sources and produces json-ified results

positional arguments:
  root                  
                        root XPath element name, used to interpret the filter file against
  filter                
                        filter file name, containing column separated filter and map definitions like so:
                        [XPath], [target json attribute name], [string|int], [force array]
                        (see sample formatting file included with the source)
  source                
                        source xml formatted file

optional arguments:
  -h, --help            show this help message and exit
  --destination DESTINATION
                        
                        file name to store the generated json into; if ommited, will output to stdout
  --split SPLIT         
                        split the xml file into valid xml files containing elements at root
                        leaves the split documents in a directory named: [source][timestamp]
                        performs the json conversion using a mrjob job, running on the split xml
  --split_root SPLIT_ROOT
                        
                        root node to split the xml on, if different from the root node to use when filtering 
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
TODO:
=====
* fix TODO's in the source
* add error handling/make the system more robust
* allow reuse of the split xml source instead of regenerating it on each run
* clearer/more detailed documentation
* separate filtering xml and from writing out
* experiment with extending the configuration and language - allow, for example, collection of several xpaths into one json list
