#!/bin/bash
fact() {
local n=$1
if (( $n <= 1 )); then
echo 1
return
fi
echo $(( $n * $( fact $(( $n - 1 )) ) ))
return
}
result=$( fact 5 )
echo $result