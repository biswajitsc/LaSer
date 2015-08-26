python NumericalNormalization.py
echo "Operator Grouping. Output will be stored in ../../Data/OperatorGroupedMathML"
rm ../../Data/OperatorGroupedMathML
python operator_grouping.py ../../Data/NumberNormalizedMathML > ../../Data/OperatorGroupedMathML
echo "Normalizing Unicodes. Output will be stored in ../../Data/UnicodeNormalizedMathML"
rm ../../Data/UnicodeNormalizedMathML
python unicode_normalization.py ../../Data/OperatorGroupedMathML > ../../Data/UnicodeNormalizedMathML

