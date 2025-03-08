#  Proyecto 1 Compiladores

## 📋 Lista de Integrantes

| Nombre        | Carnet     |
|--------------|------------|
| Vanii Alcantara  | 7690-18-1298   |
| Daniel Miranda  | 7690-22-17930   |
| Jose Salazar | 7690-22-8974   |
| Jose Medina | 7690-20-13785   |
| Jordany López | 7690-16-6870   |


##  Descripción
Este proyecto implementa un intérprete de expresiones matemáticas y lógicas usando ANTLR para el análisis sintáctico y léxico. Se encarga de tokenizar, parsear y evaluar expresiones definidas en un archivo de entrada.

El proyecto interpreta expresiones matemáticas y lógicas definidas en archivo_entrada.txt. Para esto, utiliza ANTLR para generar un analizador léxico y sintáctico basado en la gramática definida en Expr.g4. Luego, Visitor.py recorre el árbol de sintaxis y evalúa las expresiones.

Declara tres variables (x, y, z) con valores enteros.
Imprime los valores iniciales de estas variables.
Realiza las siguientes operaciones aritméticas:
- Suma (x + y + z)
- Resta (x - y - z)
- Multiplicación (x * y * z)
- División (x / y / z)

Imprime los resultados de estas operaciones.
Evalúa diferentes condiciones utilizando estructuras de control if:
- Si la suma es mayor que 10.
- Si la resta es negativa.
- Si la multiplicación es mayor que 20.
- Si la división es menor que 1.
- Si x es mayor que y.
- Si y es mayor que z.

##  Instalación
## 📂 Estructura del Proyecto


```plaintext
 Proyecto 
 ├── Expr.g4               # Archivo de gramática ANTLR
 ├── Expr.interp           # Archivo generado por ANTLR
 ├── Expr.tokens           # Tokens generados por ANTLR
 ├── ExprLexer.interp      # Archivo de interpretación del lexer
 ├── ExprLexer.py          # Lexer generado por ANTLR
 ├── ExprLexer.tokens      # Tokens del lexer
 ├── ExprListener.py       # Listener para la gramática
 ├── ExprParser.py         # Parser generado por ANTLR
 ├── ExprVisitor.py        # Implementación del Visitor Pattern
 ├── Visitor.py            # Archivo con la lógica de visitante
 ├── archivo_entrada.txt   # Archivo de entrada con datos de prueba
 ├── main.py               # Archivo principal para ejecutar el programa
 ├── .gitattributes        # Configuración de Git
```

### Visitor.py - Evaluador del Árbol de Sintaxis

`Visitor.py` implementa la lógica de interpretación del código fuente utilizando la clase generada por ANTLR, `ExprVisitor`. Su función principal es recorrer el Árbol de Sintaxis Abstracta (AST) y ejecutar las instrucciones del lenguaje definido en `Expr.g4`.

---

### Relación con Otros Archivos
- **`Expr.g4`**: Define la gramática del lenguaje.
- **`ExprParser.py`**: Contiene el parser generado por ANTLR.
- **`ExprLexer.py`**: Se encarga del análisis léxico.
- **`ExprVisitor.py`**: Clase base generada por ANTLR, de la cual `Visitor.py` hereda.
- **`main.py`**: Punto de entrada que usa `Visitor.py` para interpretar el código.
- **`archivo_entrada.txt`**: Archivo con el código fuente a ejecutar.

---

##  Funcionalidad de `Visitor.py`

#### Manejo de Variables y Expresiones
- **`self.variables`**: Diccionario para almacenar variables declaradas.
- **`visitAsignacion(ctx)`**: Evalúa una expresión y asigna su valor a una variable.

####  Entrada y Salida
- **`visitImpresion(ctx)`**: Evalúa una expresión y la imprime en la consola.

#### Estructuras de Control
- **`visitCondicion(ctx)`**: Evalúa condiciones `if-else` y ejecuta el bloque correspondiente.
- **`visitBucle(ctx)`**: Maneja bucles `while` y `for`, ejecutándolos según la condición.

### ➕ Operaciones Matemáticas y Lógicas
| Tipo | Operadores | Función |
|------|-----------|---------|
| **Aritméticas** | `+`, `-`, `*`, `/` | `ops[op](left, right)` |
| **Comparación** | `>`, `<`, `==`, `!=` | `comp_ops[op](left, right)` |
| **Lógicas** | `&&`, `||`, `!` | `logical_ops[op](left, right)` |

### Evaluación de Expresiones
- **`visitExpr(ctx)`**: Evalúa números, variables y operaciones matemáticas.
- **`visitPrograma(ctx)`**: Inicia la ejecución del código interpretando todas las declaraciones.

---
```python
import operator
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor

# Definir las operaciones disponibles
ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}

# Operadores de comparación
comp_ops = {'>': operator.gt, '<': operator.lt, '==': operator.eq, '!=': operator.ne}

# Operadores lógicos
logical_ops = {'&&': lambda x, y: x and y, '||': lambda x, y: x or y, '!': lambda x: not x}

class Visitor(ExprVisitor):

    def __init__(self):
        self.variables = {}

    def visitPrograma(self, ctx):
        return self.visit(ctx.declaraciones())

    def visitDeclaraciones(self, ctx):
        for declaracion in ctx.declaracion():
            self.visit(declaracion)

    def visitAsignacion(self, ctx):
        var_name = ctx.ID().getText()  # Obtener el nombre de la variable
        value = self.visit(ctx.expr())  # Evaluar la expresión
        self.variables[var_name] = value  # Asignar el valor a la variable
        return value

    def visitImpresion(self, ctx):
        value = self.visit(ctx.expr())  # Evaluar la expresión
        print(value)  # Imprimir el resultado
        return value

    def visitCondicion(self, ctx):
        if self.visit(ctx.expr()):  # Evaluar la condición
            self.visit(ctx.bloque(0))  # Ejecutar el bloque "if"
        elif ctx.elseBloque():  # Si hay un bloque "else"
            self.visit(ctx.bloque(1))  # Ejecutar el bloque "else"

    def visitBucle(self, ctx):
        if ctx.getChild(0).getText() == 'while':  # Si es un bucle while
            while self.visit(ctx.expr()):  # Evaluar la condición
                self.visit(ctx.bloque())  # Ejecutar el bloque del bucle
        elif ctx.getChild(0).getText() == 'for':  # Si es un bucle for
            self.visit(ctx.asignacion(0))  # Ejecutar la asignación inicial
            while self.visit(ctx.expr()):  # Evaluar la condición
                self.visit(ctx.bloque())  # Ejecutar el bloque del bucle
                self.visit(ctx.asignacion(1))  # Ejecutar la asignación de incremento

    def visitExpr(self, ctx):
        # Si es un número
        if ctx.NUM():
            return int(ctx.NUM().getText())

        # Si es una cadena de texto
        elif ctx.STRING():
            return ctx.STRING().getText()[1:-1]  # Eliminar las comillas

        # Si es una variable
        elif ctx.ID():
            var_name = ctx.ID().getText()
            if var_name in self.variables:
                return self.variables[var_name]
            raise NameError(f"Variable '{var_name}' no definida")

        # Operaciones aritméticas
        elif len(ctx.children) == 3 and ctx.children[1].getText() in ops:
            left = self.visit(ctx.getChild(0))  # Evaluar la izquierda
            op = ctx.getChild(1).getText()  # Obtener el operador
            right = self.visit(ctx.getChild(2))  # Evaluar la derecha
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return ops[op](left, right)  # Realizar la operación
            raise TypeError(f"Operación aritmética con operandos no numéricos: {left}, {right}")

        # Operaciones de comparación
        elif len(ctx.children) == 3 and ctx.children[1].getText() in comp_ops:
            left = self.visit(ctx.getChild(0))  # Evaluar la izquierda
            op = ctx.getChild(1).getText()  # Obtener el operador
            right = self.visit(ctx.getChild(2))  # Evaluar la derecha
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return comp_ops[op](left, right)  # Realizar la comparación
            raise TypeError(f"Operación de comparación con operandos no válidos: {left}, {right}")

        # Operaciones lógicas
        elif len(ctx.children) == 3 and ctx.children[1].getText() in logical_ops:
            left = self.visit(ctx.getChild(0))  # Evaluar la izquierda
            op = ctx.getChild(1).getText()  # Obtener el operador
            right = self.visit(ctx.getChild(2))  # Evaluar la derecha
            if isinstance(left, bool) and isinstance(right, bool):
                return logical_ops[op](left, right)  # Realizar la operación lógica
            raise TypeError(f"Operación lógica con operandos no booleanos: {left}, {right}")

        # Expresiones entre paréntesis
        elif len(ctx.children) == 1:
            return self.visit(ctx.getChild(0))

        raise ValueError(f"Expresión no válida: {ctx.getText()}")
```
### Main
```python
import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from Visitor import Visitor

def main(argv):
    try:
        # Verificar si se proporcionó un archivo de entrada
        if len(argv) < 2:
            print("❌ Debes proporcionar un archivo de entrada.")
            print("Uso: python main.py <archivo>")
            sys.exit(1)

        # Cargar el archivo
        input_file = argv[1]
        print(f"📂 Cargando archivo: {input_file}")
        input_stream = FileStream(input_file, encoding='utf-8')

        # Analizador léxico
        lexer = ExprLexer(input_stream)
        stream = CommonTokenStream(lexer)

        # Analizador sintáctico
        parser = ExprParser(stream)
        tree = parser.programa()  # Construir el árbol sintáctico

        # Ejecutar el Visitor
        print("🚀 Ejecutando el programa...")
        visitor = Visitor()
        visitor.visit(tree)
        print("✅ Ejecución completada.")

    except FileNotFoundError:
        print(f"❌ Error: El archivo '{argv[1]}' no existe.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv)
```
## 📜 Conclusión
Este proyecto es un **intérprete de expresiones matemáticas y lógicas** basado en **ANTLR y Python**.  
Permite definir y ejecutar **operaciones, estructuras de control y variables** de manera eficiente.

 **Ahora puedes ejecutar el código y probar su funcionamiento.** 
