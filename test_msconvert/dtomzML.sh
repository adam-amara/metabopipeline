
docker build -t test_msconvert .

mkdir mzML

folders=$(echo $1 | tr "/" "\n")
myarray=($folders)
length=${#myarray[@]}
VAR1=$(printf "../"'%.0s' $(eval "echo {1.."$(($length+1))"}") )

for DIR in ${1}/*
do
	cd $DIR
	FOL=$(basename "$PWD")
	docker run -it --rm -e WINEDEBUG=-all -v $PWD:/data:rw test_msconvert wine msconvert *.d --zlib --filter "peakPicking true 1-" -o $FOL
	mv $FOL "${VAR1}mzML"
	cd $VAR1
done



