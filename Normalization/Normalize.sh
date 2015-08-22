python NumericalNormalization.py
echo "Normalizing Unicodes. Output will be stored in ../../Data/UnicodeNormalizedMathML"
rm ../../Data/UnicodeNormalizedMathML
touch ../../Data/UnicodeNormalizedMathML
python unicode_normalization.py ../../Data/NumberNormalizedMathML > ../../Data/UnicodeNormalizedMathML

