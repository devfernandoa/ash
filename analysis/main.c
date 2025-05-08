#include <stdio.h>

int yyparse(void);

void yyerror(const char* s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    int result = yyparse();
    return result;  // returns non-zero if there was a syntax error
}
