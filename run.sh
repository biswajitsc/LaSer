head -$1 ../Data/MathMLMeta.xml > ../Data/smallMathMLMeta.xml
head -$1 ../Data/MathML.xml > ../Data/smallMathML.xml
#cd ExtractData
#python SimplifyEquations.py ../../Data/smallMathML.xml ../../Data/smallMathMLMeta.xml
#cd ../Normalization
#python Normalization.py
#cd ../FeatureExtraction
#python extractExpressionFeatures.py ../../Data/NormalizedMathML.xml
#python extractContextFeatures.py ../../Data/equation_context.txt
