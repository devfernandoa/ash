#!/bin/bash

cd ..

PASS_COUNT=0
FAIL_COUNT=0

echo "Running positive tests..."
for file in tests/positive/*.ash; do
    echo "$file"
    ./ash < "$file" > /dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Passed"
        ((PASS_COUNT++))
    else
        echo "Unexpected failure: $file"
        ((FAIL_COUNT++))
    fi
    echo
done

echo "🔍 Running negative tests..."
for file in tests/negative/*.ash; do
    echo "$file"
    ./ash < "$file" > /dev/null
    if [ $? -ne 0 ]; then
        echo "Correctly failed"
        ((PASS_COUNT++))
    else
        echo "Unexpected pass: $file"
        ((FAIL_COUNT++))
    fi
    echo
done

echo "Total passed: $PASS_COUNT"
echo "Total failed: $FAIL_COUNT"

if [ $FAIL_COUNT -ne 0 ]; then
    exit 1
else
    exit 0
fi
