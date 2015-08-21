# LaSer: The LaTex Search Engine
A search engine to search up LaTex formulae from academic articles and books.

Instructions
------------
Dataset
* Download dataset from http://www.cs.cornell.edu/projects/kddcup/datasets.html.
* Save all the zip files to ```../Dataset/```.
* Unzip using ```unzipdata.sh```. The unzipped files are saved to ```../Dataset/```.
* All intermediate results are being saved onto ```../Data/```

Formulae Extraction
* Run ```ExtractData/ExtractFormulae.py```. The extracted formulae will be stored in ```Data/Formulae```, one formula per line. The respective meta data for each formula would be stored in ```Data/Meta```.
* Formulae is ```cp1252``` encoded. Make sure to decode this properly while reading from the file. Read the wiki for info.


MathML Extraction
* Download latexxml by ```sudo apt-get install latexml```
* Run ```python GenMathML.py ../../Data/Formulae ../../Data/MathML```. The xml will be stored in ```Data/MathML```, one xml per line. The line number for the formulae for which error occurred while generating xml would be stored in ```Data/error.txt```.
 
Simplify MathML Extraction
* Download and install sympy package - ```sudo pip install sympy```
* Run ```python ExtractData/SimplifyEquations.py``` . The simplified MathMLs will be stored in ```Data/SimplifiedMathML``` and the expressions will be stored in ```Data/Expressions```.

Normalization
* Numerical Normalization : Run ```bash Normalize.sh``` in Normalization folder. The MathMLs will be stored in ```Data/NumberNormalizedMathML```.

