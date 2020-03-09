# carra_uq

UQ calcs for CARRA
Scripts used to do the odb data extraction
and data processing for the uncertainty estimation of CARRA

- get_logfiles.sh: copy the logfiles.tar files containing the "HM_Date*" files

- get_all_members: copy the  odb_stuff.tar files for all members in relevant dates. This can take a long time....

- callodbsql_allmems.sh: call the odbsql commands for each member. Also a relatively slow process
