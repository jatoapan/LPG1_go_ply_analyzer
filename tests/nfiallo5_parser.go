// Algorithm to validate syntax highlighting for Nicolás Fiallo's contributions
package main

import "fmt"

var edad int = 20

const pi float64 = 3.14

var lista [5]int = [5]int{5, 4, 3, 2, 1}
var valor = "Hola Mundo"

// type struct
type Student struct { //struct
	name string //string
	age  int    //int
}

type Profesor struct {
	name    string
	subject string
	Student
}

// switch_initialization
func switch_con_asignacion() string {
	switch x := 2; x {
	case 1, 2, 3, 4, 5:
		return "It's a weekday"
	case 6, 7:
		return "It's the weekend"
	case "string_prueba": //invalid case to test error detection
		fmt.Println("Caso inválido")
	default:
		return "Not a valid day"
	}
}

// switch_true
func switch_true() {
	switch {
	case edad < 18:
		fmt.Println("Menor de edad")
	case edad >= 18 && edad < 65:
		fmt.Println("Adulto")
	default:
		fmt.Println("Anciano")
	}
}

// switch_expression
func switch_expresion() {
	switch valor {
	case "Hola Mundo":
		fmt.Println("Saludo detectado")
	case "Adiós":
		fmt.Println("Despedida detectada")
	default:
		fmt.Println("Otro valor")
	}
}

func broken_switch() {
	switch valor {
	case "Test": // false string case
		fmt.Println("Test case")
	case 123: // Invalid int case
		fmt.Println("Invalid case")
	case 25.4: // Invalid float case
		fmt.Println("Another invalid case")
	}
}

func main() {
	// array initialization
	var a = [5]int{10, 20, 30, 40, 50}
	fmt.Println("array:", a)

	// array
	var nums = [...]int{1, 2, 3, 4, 5}
	fmt.Println("slice:", nums)

	/*
		It validates multi-line comments
	*/
	if edad == 20 {
		fmt.Println("Edad correcta")
	} else if buleano {
		edad++
		fmt.Println("Edad incrementada")
	} else {
		fmt.Println("mal calculado")
	}
}
