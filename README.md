# Go Analyzer

Analizador estático de código Go implementado en Python utilizando PLY (Python Lex-Yacc). Realiza análisis léxico, sintáctico y semántico de programas Go con detección de errores y generación de tabla de símbolos.

## Características

- **Análisis Léxico**: Tokenización completa con detección de errores léxicos
- **Análisis Sintáctico**: Validación de gramática y construcción de árbol de análisis
- **Análisis Semántico**: Verificación de tipos, reglas semánticas y tabla de símbolos
- **Interfaz Gráfica**: GUI intuitiva construida con tkinter
- **Detección de Errores**: Reportes detallados con números de línea
- **Exportación**: Guardar resultados del análisis en archivos

## Requisitos

- Python 3.7+
- PLY 3.11

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd project_py_analyzer
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Instalar el paquete (opcional):
```bash
pip install -e .
```

## Uso

### Interfaz Gráfica

Ejecutar la aplicación GUI:
```bash
python run_gui.py
```

La interfaz permite:
- Escribir o cargar código Go
- Ejecutar análisis completo con `Ctrl+R`
- Ver resultados con código de colores
- Exportar análisis a archivos

### Línea de Comandos

Análisis léxico:
```bash
python run_lexer.py <archivo.go>
```

Análisis sintáctico:
```bash
python run_parser.py <archivo.go>
```

Análisis semántico:
```bash
python run_semantic.py <archivo.go>
```

## Estructura del Proyecto

```
project_py_analyzer/
├── go_analyzer/
│   ├── core/
│   │   ├── lexer/          # Analizador léxico
│   │   ├── parser/         # Analizador sintáctico
│   │   └── analyzer.py     # Módulo principal de análisis
│   └── gui/
│       ├── components/     # Componentes de la interfaz
│       ├── handlers/       # Manejadores de eventos
│       └── main_window.py  # Ventana principal
├── tests/                  # Archivos de prueba en Go
├── logs/                   # Logs de análisis
├── run_gui.py             # Ejecutar GUI
├── run_lexer.py           # Ejecutar análisis léxico
├── run_parser.py          # Ejecutar análisis sintáctico
└── run_semantic.py        # Ejecutar análisis semántico
```

## Atajos de Teclado (GUI)

- `Ctrl+R`: Ejecutar análisis
- `Ctrl+L`: Limpiar resultados
- `Ctrl+O`: Abrir archivo
- `Ctrl+S`: Guardar resultados

## Ejemplo

```go
package main

import "fmt"

func main() {
    var x int = 10
    const PI = 3.14
    fmt.Println(x + int(PI))
}
```

El analizador detectará:
- Tokens correctos del código
- Estructura sintáctica válida
- Tipos compatibles en operaciones
- Correcta declaración de constantes y variables

## Desarrollo

Este proyecto fue desarrollado como parte del curso de Lenguajes de Programación en ESPOL.

## Licencia

Proyecto académico - ESPOL 2025
