echo "Converting to pdf folder: $1"

for directory in $1*
do
    echo "Doing folder: $directory"
    for file in $directory/*
        do
        new_dir=$2/${directory/$1/""}${file/$directory/""}/
        echo creating: $new_dir
        mkdir -p $new_dir
        pdftoppm -png $file $new_dir -r 350
    done
done


echo "done all folder"
