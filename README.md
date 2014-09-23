oceancolour-downloader
======================

##On-going dev notes

The plugin is making progress! I have restructured the downloaders (with orangemug's help). I've written a downloader for CHL-a from NASA Oceancolour which for now is hard wired to only work with annual datasets. Lots to do!!

##What is it

QGIS plugin to allow easy download and use of earth observation datasets with QGIS. 

##Currently...

Access CHL-a concentrations from NASA Oceancolour. Download annual datasets given a date range. Unzip them and convert to Geotiff. 

##The plan

1. Choice of SST or CHL-a
2. Choice of monthly or annual

##Implementation

1. make the functions into a class. __DONE__
2. think about how to split into individual functions a bit more. __DONE__
3. add functionality for monthly range __Do this next__
4. add dataset type to the interface, and a box to say feedback to user for the valid time period. 
5. some way to stop users selecting dates outside the time period.
6. add another optional dataset - SST


How to add monthly range functionality? No idea yet. 

