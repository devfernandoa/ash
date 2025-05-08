#!/bin/bash

cd "$(dirname "$0")"

PASS=0
FAIL=0
TMP_OUT=".tmp_output.sh"
TMP_RESULT=".tmp_output.txt"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

run_positive_test() {
    testfile="$1"
    base="${testfile%.ash}"
    expected_out="${base}.out"

    echo -e "${YELLOW}Running positive test: $testfile${NC}"

    python3 semantic/main.py "$testfile" "$TMP_OUT"
    if [ $? -eq 0 ]; then
        if [[ "$testfile" == *"input_output_echo_read.ash" ]]; then
            echo "TestInput" | ./"$TMP_OUT" > "$TMP_RESULT"
        else
            ./"$TMP_OUT" > "$TMP_RESULT"
        fi

        diff -q "$TMP_RESULT" "$expected_out" > /dev/null
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}PASS${NC}"
            ((PASS++))
        else
            echo -e "${RED}FAIL: output mismatch${NC}"
            echo "--- Expected:"
            cat "$expected_out"
            echo "--- Got:"
            cat "$TMP_RESULT"
            ((FAIL++))
        fi
    else
        echo -e "${RED}FAIL: compilation error${NC}"
        ((FAIL++))
    fi
}

run_negative_test() {
    testfile="$1"
    echo -e "${YELLOW}Running negative test: $testfile${NC}"

    python3 semantic/main.py "$testfile" "$TMP_OUT" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${GREEN}Correctly failed${NC}"
        ((PASS++))
    else
        echo -e "${RED}Unexpected success${NC}"
        ((FAIL++))
    fi
}

# POSITIVE TESTS
for file in tests/positive/*.ash; do
    run_positive_test "$file"
    echo
done

# NEGATIVE TESTS
for file in tests/negative/*.ash; do
    run_negative_test "$file"
    echo
done

rm -f "$TMP_OUT" "$TMP_RESULT"

echo "=============================="
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"

if [ $FAIL -ne 0 ]; then
    exit 1
else
    exit 0
fi