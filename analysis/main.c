#include <stdio.h>

int yyparse(void);

int main() {
    printf("Enter Ash code:\n");
    yyparse();
    return 0;

}
