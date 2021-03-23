
docker build -t test_msconvert .

mkdir MZML

folders=$(echo $1 | tr "/" "\n")
myarray=($folders)
length=${#myarray[@]}
VAR1=$(printf "../"'%.0s' $(eval "echo {1.."$(($length+1))"}") )

for DIR in ${1}/*
do
	echo $DIR
	echo $PWD
	cd $DIR
	echo $PWD
	FOL=$(basename "$PWD")
	echo $FOL
	docker run -it --rm -e WINEDEBUG=-all -v $PWD:/data:rw test_msconvert wine msconvert *.d -o $FOL
	mv $FOL "${VAR1}MZML"
	cd $VAR1
	echo $PWD
done



