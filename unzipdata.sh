
files=../Dataset/*

for file in $files
do
	tar -xzf $file -C ../Dataset
done