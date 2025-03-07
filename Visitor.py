import operator
ops = {'+' : operator.add, '-' : operator.sub, '*' : operator.mul, '/' : operator.truediv, '^' : operator.pow}

if "name" is not None and "." in "name":
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor

class Visitor(ExprVisitor):
     
    def __init__(self):
         self.myvars = {}
         
    def visitRoot(self,ctx):
        l = list(ctx.getChildren())
        for i in range(len(l)-1):
            result = self.visit(l[i])
            if result is not None: 
                print(result)
    
    def visitExpr(self,ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            if l[0].getText() in self.myvars:
                return self.myvars[l[0].getText()]
            return int(l[0].getText())
        else:
            left = self.visit(l[0])
            right = self.visit(l[2])
            return ops[l[1].getText()](left, right)
    
    def visitCondition(self, ctx):
        left = self.visit(ctx.getChild(0))
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.getChild(2))

        comparisons = {
            "==": operator.eq,
            "!=": operator.ne,
            "<": operator.lt,
            ">": operator.gt,
            "<=": operator.le,
            ">=": operator.ge
        }

        return comparisons[op](left, right)
    
    def visitBlock(self, ctx):
        if ctx.getChildCount() > 1:
            for i in range(1, ctx.getChildCount() - 1):
                self.visit(ctx.getChild(i))
        else:  
            self.visit(ctx.getChild(0))

    def visitAction(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 3:  # Asignación (VAR IGUAL expr)
            if l[1].getText() == ':=' or l[1].getText() == '=':
                self.myvars[l[0].getText()] = self.visit(l[2])
                return f'Asignación realizada: {l[0].getText()} = {self.myvars[l[0].getText()]}'
            else:
                return 'ERROR: Sintaxis de asignación incorrecta'
        elif len(l) >= 4 and l[0].getText() == "if":  # Estructura IF
            condition_result = self.visit(l[1])
            if condition_result:
                return self.visit(l[3])
            elif len(l) == 6 and l[4].getText() == "else":
                return self.visit(l[5])
            return None
        elif l[0].getText() == "while":  # Estructura WHILE
            while self.visit(l[1]):
                self.visitBlock(l[3])
            return None
        elif l[0].getText() == "for":  # Estructura FOR
            var_name = l[1].getText()
            start = self.visit(l[3])
            end = self.visit(l[5])

            if not isinstance(start, int) or not isinstance(end, int):
                return "ERROR: Rango de for debe ser numérico"

            self.myvars[var_name] = start

            step = 1 if start < end else -1

            while (self.myvars[var_name] <= end if step == 1 else self.myvars[var_name] >= end):
                self.visitBlock(l[7])
                self.myvars[var_name] += step

            return None
        elif l[0].getText() == 'print':  # Impresión
            if l[1].getText() in self.myvars:
                value = self.myvars[l[1].getText()]
                print(value)
                return None
            else:
                return 'ERROR: Variable no definida'
        else:
            return 'ERROR: Acción desconocida'