# LaSer: The LaTex Search Engine
A search engine to search up LaTex formulae from academic articles and books.

Instructions
------------
Dataset
* Download dataset from http://www.cs.cornell.edu/projects/kddcup/datasets.html.
* Save all the zip files to ```../Dataset/```.
* Unzip using ```unzipdata.sh```. The unzipped files are saved to ```../Dataset/```.

Formulae Extraction
* Run ```ExtractData/ExtractFormulae.py```. The extracted formulae will be stored in ```Data/Formulae```, one formula per line. The respective meta data for each formula would be stored in ```Data/Meta```.
* Formulae is ```cp1252``` encoded. Make sure to decode this properly while reading from the file.
