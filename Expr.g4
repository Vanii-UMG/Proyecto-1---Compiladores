grammar Expr;
root: action+ EOF;

action: VAR IGUAL expr
    | 'print' (VAR | STRING)
    | 'if' condition 'then' block ('else' block)?
    | 'while' condition 'do' block
    | 'for' VAR 'in' expr 'to' expr 'do' block
    | expr
    ;

block: '{' action* '}' 
     | action           
     ;


condition: expr ('==' | '!=' | '<' | '>' | '<=' | '>=') expr ;

expr: <assoc=right> expr ELE expr
    | expr (MUL|DIV) expr
    | expr (SUM|RES) expr
    | expr MOD expr
    | '(' expr ')'
    | VAR
    | NUM
    | STRING
    ;
    
NUM : [0-9]+ ;
VAR : [_a-zA-Z][_a-zA-Z0-9]* ;
STRING : '"' (~["\\] | '\\' .)* '"' ;
SUM : '+';
RES : '-' ;
MUL : '*' ;
DIV : '/' ;
ELE : '^' ;
MOD: '%';
IGUAL : ':='|'=' ;


WS : [ \n\t]+ -> skip ;
