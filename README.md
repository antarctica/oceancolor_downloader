oceancolour-downloader
======================

##On-going dev notes

The plugin is making progress! I have restructured the downloaders (with orangemug's help). I've written a downloader for CHL-a from NASA Oceancolour which for now working with annual, monthly and daily. Still lots to do!!

##What is it

QGIS plugin to allow easy download and use of earth observation datasets with QGIS. 

##Currently...

Access CHL-a concentrations from NASA Oceancolour. Download annual datasets given a date range. Unzip them and convert to Geotiff. 

##The plan

1. Choice of SST or CHL-a
2. Choice of monthly, annual, daily or 8day

##Implementation

1. make the functions into a class. __DONE__
2. think about how to split into individual functions a bit more. __DONE__
3. add functionality for monthly range __DONE - also done daily. Now do 8day before moving on__
4. add dataset type to the interface, and a box to say feedback to user for the valid time period. __DONE__
5. some way to stop users selecting dates outside the time period.
6. add another optional dataset - SST
7. create a file in download directory containing reference and license information.
8. any ref/license information in user interface? Option to download as a file?

##Future plans

Make a donwloader for NSIDC sea ice concentration. 
