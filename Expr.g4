grammar Expr;
root: action+ EOF;

action: VAR IGUAL expr
    | 'print' VAR
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
    | '(' expr ')'
    | VAR
    | NUM
    ;
    
NUM : [0-9]+ ;
VAR : [_a-zA-Z][_a-zA-Z0-9]* ;
SUM : '+';
RES : '-' ;
MUL : '*' ;
DIV : '/' ;
ELE : '^' ;
IGUAL : ':='|'=' ;


WS : [ \n\t]+ -> skip ;