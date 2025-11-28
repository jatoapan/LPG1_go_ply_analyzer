package main

import "fmt"

type Student struct { //struct
	name string //string
	age  int    //int
}

type Profesor struct {
	name    string
	subject string
	Student
}

var valor = "Hello World"

var a = [5]int{10, 20, 30, 40, 50}
var num [3]string
var b = [5]int{10, 20}

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
	edades := [4]int{18, 20, 22, 24}

	if edad == 20 {
		fmt.Println("Edad correcta")
	} else if buleano {
		edad++
		fmt.Println("Edad incrementada")
	} else {
		fmt.Println("mal calculado")
	}
}
