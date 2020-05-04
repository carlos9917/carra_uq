# carra_uq

UQ calcs for CARRA
Scripts used to do the odb data extraction
and data processing for the uncertainty estimation of CARRA


- get_all_members: copy the  odb_stuff.tar files for all members in relevant dates. This can take several days depending on the load. Will fetch the tar balls and untar then. It also calls dcagen.

- get_logfiles.sh: copy the logfiles.tar files containing the "HM_Date*" files

- callodbsql_allmems.sh: call the odbsql commands for each member, using
  search_HM_Date.py for each date.
  The result from odbsql is stored under each YYYY/MM/DD/init/mbrXXX with name mbrXXX_Codetype_Obstype_Varno.dat

- search_HM_Date.py reads the HM_Date log files, identifies the relevant
pairs of Obstype/Codetype/Varno and calls the odbsql commands for each combination. A summary of the variables found is stored under YYYY/MM/DD/out_hm_search.txt. There is a also a list of the odbsql commands to be used.

- call_procodb.sh: call the script process_odb.py for all dates and Obstype/Codetype/Varno combinarion. It scans the 
  relevant file for each member and prints a summary for each init time under
YYYY/MM/DD/summary_Codetype_Obstype_Varno.txt


