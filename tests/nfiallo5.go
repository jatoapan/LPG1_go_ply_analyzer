// Algorithm to validate lexer from Nicolas Fiallo
package main

import "fmt"

const str string = "hola mundo" //string
var numero = 20                 //int
var negativo float64 = -14.5    //float64

func powerOf2(a int) int {
	return 1 << a //function
}

func main() {
	negativo++               //plus-plus
	x := powerOf2(3)         //assign
	var booleano bool = true //boolean

	/*
		It validates multi-line comments
	*/
	if x == 8 { //if statement
		fmt.Println(str)
	} else if booleano {
		numero-- //minus-minus
	} else { //else statement
		fmt.Println("mal calculado")
	}
}
