#include <stdio.h>
extern int yylineno;
extern char* yytext;

int yyparse(void);

void yyerror(const char* s) {
    fprintf(stderr, "Error: %s at '%s' on line %d\n", s, yytext, yylineno);
}

int main(int argc, char** argv) {
    yyparse();
    return 0;
}