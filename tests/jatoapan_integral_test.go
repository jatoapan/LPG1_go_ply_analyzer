package main

// Variables globales
var globalCounter int = 10
var globalFlag bool = true
var globalName string = "Jose"
const PI float64 = 3.14

func main() {
    // Declaraciones locales
    var a int = 5
    b := 3
    var c float64 = 2.5
    var d string = "Texto local"
    var e bool = false
	globalCounter++       
	globalCounter += 8    
	break                 // ERROR: fuera de un for
	continue              // ERROR: fuera de un for
	PI = 3.1416           // ERROR: reasignación de constante

    // Slices explícitos
    var numeros []int = []int{2, 4, 6, 8, 10}
    var valores []float64 = []float64{1.1, 2.2, 3.3}
    var nombres []string = []string{"Ana", "Luis", "Maria"}
    var estados []bool = []bool{true, false, true}

    // Slices vacíos
    var emptyInts []int = []int{}
    var emptyStrings []string = []string{}

    // Operaciones aritméticas simples
    suma := a + b
    resta := a - b
    producto := a * b
    division := a / b
    modulo := a % b

    // Operadores de incremento y asignación
    a++
    b--
    a += 5
    b -= 2

    // Operadores de shift
    var x int = 8
    var y int = 2
    shiftLeft := x << y
    shiftRight := x >> y

    // For clásico con operaciones
    for i := 0; i < 5; i++ {
        temp := i * 2
        temp += 3
        temp--
        result := temp % 4
        shifted := temp << 1
        globalCounter = result + shifted
    }

    // Operaciones finales
    final := suma + resta + producto + division + modulo + shiftLeft + shiftRight
    globalCounter = final
}