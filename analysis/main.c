#include <stdio.h>

int yyparse(void);

void yyerror(const char* s) {
    fprintf(stderr, "Error: %s at or near '%s'\n", s);
}

int main(int argc, char** argv) {
    yyparse();
    return 0;
}