%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(const char* s);
int yylex(void);
%}

%union {
    int integer;
    int boolean;
    char* str;
}

%token <str> IDENTIFIER STRING
%token <integer> INT
%token <boolean> BOOL

%token LET FUNCTION IF ELSE FOR WHILE RETURN IN
%token ECHO_KW READ
%token INT_TYPE STRING_TYPE BOOL_TYPE VOID_TYPE
%token EQ NEQ GTE LTE GT LT
%token ASSIGN PLUS MINUS MUL DIV MOD
%token LPAREN RPAREN LBRACE RBRACE SEMI COLON COMMA DOTDOT
%token <str> BANG_LINE
%token <str> BANG_EXPR
%token ERROR

%type type

%%

program:
    program function_declaration
  | program statement
  | /* empty */
  ;

function_declaration:
    type FUNCTION IDENTIFIER LPAREN parameter_list RPAREN block
  ;

parameter_list:
    /* empty */
  | type IDENTIFIER
  | parameter_list COMMA type IDENTIFIER
  ;

statement:
    variable_declaration
  | assignment
  | if_statement
  | for_loop
  | while_loop
  | echo_statement
  | return_statement
  | inline_command
  | expression SEMI
  | block
  ;

block:
    LBRACE statement_list RBRACE
  ;

statement_list:
    /* empty */
  | statement_list statement
  ;

variable_declaration:
    LET IDENTIFIER COLON type optional_init SEMI
  ;

optional_init:
    /* empty */
  | ASSIGN expression
  ;

assignment:
    IDENTIFIER ASSIGN expression SEMI
  ;

echo_statement:
    ECHO_KW LPAREN expression RPAREN SEMI
  ;

return_statement:
    RETURN expression SEMI
  | RETURN SEMI
  ;

if_statement:
    IF LPAREN expression RPAREN block else_clause
  ;

else_clause:
    /* empty */
  | ELSE block
  ;

for_loop:
    FOR LPAREN IDENTIFIER IN expression DOTDOT expression RPAREN block
  ;

while_loop:
    WHILE LPAREN expression RPAREN block
  ;

inline_command:
    BANG_LINE SEMI
  ;

expression:
    expression PLUS expression
  | expression MINUS expression
  | expression MUL expression
  | expression DIV expression
  | expression MOD expression
  | expression EQ expression
  | expression NEQ expression
  | expression GT expression
  | expression LT expression
  | expression GTE expression
  | expression LTE expression
  | LPAREN expression RPAREN
  | function_call
  | read_expression
  | BANG_EXPR
  | IDENTIFIER
  | INT
  | STRING
  | BOOL
  ;

function_call:
    IDENTIFIER LPAREN argument_list RPAREN
  ;

argument_list:
    /* empty */
  | expression
  | argument_list COMMA expression
  ;

read_expression:
    READ LPAREN type RPAREN
  ;

type:
    INT_TYPE
  | STRING_TYPE
  | BOOL_TYPE
  | VOID_TYPE
  ;

%%

void yyerror(const char* s) {
    fprintf(stderr, "Error: %s\n", s);
}
