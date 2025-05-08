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
%token <str> INT_TYPE STRING_TYPE BOOL_TYPE VOID_TYPE

%token LET FUNCTION IF ELSE FOR WHILE RETURN IN
%token ECHO_KW READ
%token EQ NEQ GTE LTE GT LT
%token ASSIGN PLUS MINUS MUL DIV MOD
%token LPAREN RPAREN LBRACE RBRACE SEMI COLON COMMA DOTDOT
%token <str> BANG_LINE
%token <str> BANG_EXPR
%token OR AND NOT
%token ERROR

// Precedence declarations (lowest to highest)
%nonassoc OR
%nonassoc AND
%left EQ NEQ
%left GT LT GTE LTE
%left PLUS MINUS
%left MUL DIV MOD
%nonassoc UNARY

%type <str> type

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
  | parameter
  | parameter_list COMMA parameter
  ;

parameter:
    type IDENTIFIER
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
    RETURN optional_expression SEMI
  ;

optional_expression:
    /* empty */
  | expression
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
    logical_or_expression
  ;

logical_or_expression:
    logical_and_expression
  | logical_or_expression OR logical_and_expression
  ;

logical_and_expression:
    equality_expression
  | logical_and_expression AND equality_expression
  ;

equality_expression:
    relational_expression
  | equality_expression EQ relational_expression
  | equality_expression NEQ relational_expression
  ;

relational_expression:
    additive_expression
  | relational_expression GT additive_expression
  | relational_expression LT additive_expression
  | relational_expression GTE additive_expression
  | relational_expression LTE additive_expression
  ;

additive_expression:
    multiplicative_expression
  | additive_expression PLUS multiplicative_expression
  | additive_expression MINUS multiplicative_expression
  ;

multiplicative_expression:
    unary_expression
  | multiplicative_expression MUL unary_expression
  | multiplicative_expression DIV unary_expression
  | multiplicative_expression MOD unary_expression
  ;

unary_expression:
    postfix_expression
  | MINUS unary_expression %prec UNARY
  | NOT unary_expression %prec UNARY
  ;

postfix_expression:
    primary_expression
  | function_call
  ;

primary_expression:
    LPAREN expression RPAREN
  | IDENTIFIER
  | INT
  | STRING
  | BOOL
  | read_expression
  | BANG_EXPR
  ;

function_call:
    IDENTIFIER LPAREN argument_list RPAREN
  ;

argument_list:
    /* empty */
  | expression_list
  ;

expression_list:
    expression
  | expression_list COMMA expression
  ;

read_expression:
    READ LPAREN RPAREN
  ;

type:
    INT_TYPE       { $$ = $1; }
  | STRING_TYPE    { $$ = $1; }
  | BOOL_TYPE      { $$ = $1; }
  | VOID_TYPE      { $$ = $1; }
  ;

%%

void yyerror(const char* s) {
    fprintf(stderr, "Error: %s\n", s);
}