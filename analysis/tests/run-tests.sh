#!/bin/bash

# Go up to the analysis folder (where ash binary is)
cd ..

for file in tests/*.ash; do
    echo "Running $file"
    ./ash < "$file"
    if [ $? -ne 0 ]; then
        echo "❌ Error in $file"
        exit 1
    else
        echo "✅ Success"
    fi
    echo
done
