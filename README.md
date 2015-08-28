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
* Run ```python GenMathML.py```. The xml will be stored in ```Data/MathML.xml```, one xml per line and the meta information for the equations in ```Data/MathML.xml``` will be generated in ```Data/MathMLMeta.xml```. The line number for the formulae for which error occurred while generating xml would be stored in ```Data/error.txt```.
 
Simplify MathML Extraction
* Download and install sympy package - ```sudo pip install sympy```
* Run ```python ExtractData/SimplifyEquations.py``` . The simplified MathMLs will be stored in ```Data/SimplifiedMathML``` and the expressions will be stored in ```Data/Expressions```.

Normalization
* Unicode, Operator and Numerical Normalization : Run ```python Normalize.py filename >> ../../Data/NormalizedMathML``` in Normalization folder. The normalized MathML will be stored in ```../../Data/NormalizedMathML```.

Feature Extraction
* Run ```python extractExpressionFeatures.py ../../Data/NormalizedMathML```. The unigram, bigram and trigram features will be stored in ```Data/UnigramFeatures```, ```Data/BigramFeatures``` and ```Data/TrigramFeatures``` respectively. The idf scores for each feature will be stored in ```Data/IDF-Scores```

FrontEnd prerequisites 
* Install ```apache server```
* Install ```php5```,```php5-curl```

Structural Properties
* Just a basic structural generation
* Run ```python genTreeStructure.py``` and the different variations will be generated in ```../../Data/StructureMathML.xml``` in line separated way and their metapath will be generated in ```../../Data/StructureMathMLMeta.xml``` in line separated way. 
* Also the equations in ```../../Data/StructureMathML.xml``` will be in this format ```<line number of the original equation> <space> <xml of the variation>```
