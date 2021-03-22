docker build -t test_msconvert .

mkdir MZML
for DIR in data/Batch1_Germany_slim/NR160118/*
do
	cd $DIR
	FOL=$(basename "$DIR")
	docker run -it --rm -e WINEDEBUG=-all -v $PWD:/data:rw test_msconvert wine msconvert *.d -o $FOL
	mv $FOL ../../../../MZML/
	cd ../../../..
done