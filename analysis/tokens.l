%option yylineno
%{
#include "parser.tab.h"
#include <string.h>
#include <stdlib.h>
%}

%%

"=="        { return EQ; }
"!="        { return NEQ; }
">="        { return GTE; }
"<="        { return LTE; }
">"         { return GT; }
"<"         { return LT; }

"let"       { return LET; }
"function"  { return FUNCTION; }
"if"        { return IF; }
"else"      { return ELSE; }
"for"       { return FOR; }
"while"     { return WHILE; }
"return"    { return RETURN; }
"echo"      { return ECHO_KW; }
"read"      { return READ; }
"in"        { return IN; }

"int"       { return INT_TYPE; }
"string"    { return STRING_TYPE; }
"bool"      { return BOOL_TYPE; }
"void"      { return VOID_TYPE; }

"true"      { yylval.boolean = 1; return BOOL; }
"false"     { yylval.boolean = 0; return BOOL; }

"="         { return ASSIGN; }
"+"         { return PLUS; }
"-"         { return MINUS; }
"*"         { return MUL; }
"/"         { return DIV; }
"%"         { return MOD; }

"("         { return LPAREN; }
")"         { return RPAREN; }
"{"         { return LBRACE; }
"}"         { return RBRACE; }
";"         { return SEMI; }
":"         { return COLON; }
","         { return COMMA; }
".."        { return DOTDOT; }

"!("[^)]*")" { 
    yylval.str = strdup(yytext+2); 
    yylval.str[strlen(yylval.str)-1] = '\0'; 
    return BANG_EXPR; 
}

"!"[^ \t\n\r=;]+ { 
    yylval.str = strdup(yytext+1); 
    return BANG_LINE; 
}

[a-zA-Z_][a-zA-Z0-9_]* { yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+                { yylval.integer = atoi(yytext); return INT; }
\"([^\"\n]*)\"        { yylval.str = strdup(yytext); return STRING; }

[ \t\r\n]+  ;  /* Skip whitespace */

.           { return ERROR; }

%%

int yywrap() {
    return 1;
}