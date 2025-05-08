#!/bin/bash

# Move to analysis directory where the ash binary is located
cd ..

PASS_COUNT=0
FAIL_COUNT=0

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running positive tests...${NC}"
for file in tests/positive/*.ash; do
    echo "→ $file"
    ./ash < "$file" > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✔ Passed${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}✘ Unexpected failure: $file${NC}"
        ((FAIL_COUNT++))
    fi
    echo
done

echo -e "${YELLOW}Running negative tests...${NC}"
for file in tests/negative/*.ash; do
    echo "→ $file"
    ./ash < "$file" > /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${GREEN}✔ Correctly failed${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}✘ Unexpected pass: $file${NC}"
        ((FAIL_COUNT++))
    fi
    echo
done

echo -e "${YELLOW}Summary:${NC}"
echo -e "${GREEN}✔ Total passed: $PASS_COUNT${NC}"

if [ $FAIL_COUNT -ne 0 ]; then
    echo -e "${GREEN}✔✔✔ All tests passed! ✔✔✔ ${NC}"
    exit 1
else
    echo -e "${RED}✘ Total failed: $FAIL_COUNT${NC}"
    exit 0
fi
