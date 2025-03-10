#!/bin/sh

if [ -z $VIRTUAL_ENV ]; then
    echo "This script should be executed from a Python virtual environment.";
    exit 1;
fi

if [ -d transpiled_pc_examples ]; then
    echo "transpiled_pc_examples already exists";
    exit 1;
else
    mkdir transpiled_pc_examples;
fi

for file in pc_examples/**/*.pc; do
    relative_path="${file#pc_examples/}"
    output_dir="transpiled_pc_examples/$(dirname "$relative_path")"
    mkdir -p "$output_dir"
    output_file="$(basename $file | cut -d '.' -f1).py"
    echo "Transpiling $file to $output_file";
    python ../pcc/pcc.py --output-rendered-source 0 -o "$output_dir/$output_file" "$file"
done


echo "Done";
exit 0;