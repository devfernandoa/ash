#!/bin/bash

for file in tests/*.ash; do
    echo "Running $file"
    ./ash < "$file"
    if [ $? -ne 0 ]; then
        echo "❌ Error in $file"
    else
        echo "✅ Success"
    fi
    echo
done
