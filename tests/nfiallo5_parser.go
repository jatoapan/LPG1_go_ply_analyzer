// Algorithm to validate syntax highlighting for Nicolás Fiallo's contributions
package main

import "fmt"

var edad int = 20

<<<<<<< Updated upstream
type Person struct {
	name string
	age  int
}

func isWeekDay(day string) string {
	switch day {
	case "monday", "tuesday", "wednesday", "thursday", "friday":
=======
type Student struct { //struct
	name string //string
	age  int    //int
}

func isWeekDay(day int) string {
	switch x := 2; x {
	case 1, 2, 3, 4, 5:
>>>>>>> Stashed changes
		return "It's a weekday"
	case 6, 7:
		return "It's the weekend"
<<<<<<< Updated upstream
=======
	case "string_prueba": //invalid case to test error detection
		fallthrough
>>>>>>> Stashed changes
	default:
		return "Not a valid day"
	}
}

func sum(nums ...int) int {
	total := 0
	for i := 0; i < len(nums); i++ {
		total += nums[i]
	}
	return total
}

func main() {
	var a = [5]int{10, 20, 30, 40, 50}
	fmt.Println("array:", a)

	var nums = []int{1, 2, 3, 4, 5}
	fmt.Println("slice:", nums)

	var array = [2]int{1, 2, 3, 4}
	fmt.Println("1D array:", array)

	const buleano = true
	result := sum(1, 2, 3, 4, 5)
	fmt.Println("sum:", result)

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

	day := isWeekDay("monday")
	fmt.Println(day)

	fmt.Println("Person:", p)
}