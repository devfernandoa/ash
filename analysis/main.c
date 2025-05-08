#include <stdio.h>

int yyparse(void);

int main() {
    int result = yyparse();
    return result;  // returns non-zero if there was a syntax error
}
