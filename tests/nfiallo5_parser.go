// Algorithm to validate syntax highlighting for Nicolás Fiallo's contributions
package main

import "fmt"

var edad int = 20 //int

type Person struct { //struct
	name string //string
	age  int    //int
}

type Circle interface {
	area(radius float64) float64 //interface
}

func isWeekDay(day string) string {
	switch day {
	case "monday", "tuesday", "wednesday", "thursday", "friday":
		return "It's a weekday"
	case "saturday", "sunday":
		return "It's the weekend"
	case "holiday":
		fallthrough
	default:
		return "Not a valid day"
	}
}

func sum(nums ...int) int {
	total := 0
	for _, num := range nums {
		total += num
	}
	return total //return
}

func main() {
	var a [5]int
	fmt.Println("emp:", a)

	a[4] = 100
	fmt.Println("set:", a)
	fmt.Println("get:", a[4])

	var twoD [2][3]int
	for i := range 2 {
		for j := range 3 {
			twoD[i][j] = i + j
		}
	}

	const buleano = true //boolean
	sum(1, 2, 3, 4, 5)   //function call
	/*
		It validates multi-line comments
	*/
	if edad == 8 { //if statement
		fmt.Println(str)
	} else if buleano {
		numero-- //minus-minus
	} else { //else statement
		fmt.Println("mal calculado")
	}
}
