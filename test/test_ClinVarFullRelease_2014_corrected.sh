#!/bin/bash -v

#curl "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/ClinVarFullRelease_2014-08.xml.gz" -o ClinVarFullRelease_2014-08.xml.gz
#gunzip ClinVarFullRelease_2014-08.xml.gz

STARTTIME=$(date +%s)
python ../xmljsonifier.py "ClinVarSet" clinvar_filter_corrected.txt ClinVarFullRelease_2014-08.xml --destination=output.xml 
ENDTIME=$(date +%s)
echo "$(($ENDTIME - $STARTTIME)) seconds to complete jsonifying..."

grep -o -w "<ReferenceClinVarAssertion" ClinVarFullRelease_2014-08.xml| wc -w
wc -l output.xml 
