// Test file for Juan Francisco Fernandez parser contributions
// Tests: if/else, structs, methods, maps, and composite literals

package main

import "fmt"

// Struct type declaration - defines a Person composite type
type Person struct {
	name string
	age  int
	city string
}

// Struct type declaration - defines a Rectangle type
type Rectangle struct {
	width  float64
	height float64
}

// Map type declaration for storing student scores
var scores map[string]int

// Map type declaration for user profiles
var profiles map[int]Person

// Method with receiver - calculates area of Rectangle
func (r Rectangle) Area() float64 {
	return r.width * r.height
}

// Method with receiver - calculates perimeter of Rectangle
func (r Rectangle) Perimeter() float64 {
	return 2 * (r.width + r.height)
}

// Method with pointer receiver - updates Person name
func (p *Person) UpdateName(newName string) {
	p.name = newName
}

// Method with receiver - checks if person is adult
func (p Person) IsAdult() bool {
	return p.age >= 18
}

func main() {
	// If statement - simple condition
	x := 10
	if x > 5 {
		fmt.Println("x is greater than 5")
	}

	// If-else statement - binary decision
	y := 3
	if y > 5 {
		fmt.Println("y is greater than 5")
	} else {
		fmt.Println("y is not greater than 5")
	}

	// If-else-if chain - multiple conditions
	score := 85
	if score >= 90 {
		fmt.Println("Grade: A")
	} else if score >= 80 {
		fmt.Println("Grade: B")
	} else if score >= 70 {
		fmt.Println("Grade: C")
	} else {
		fmt.Println("Grade: F")
	}

	// If with initialization statement
	if age := 25; age >= 18 {
		fmt.Println("Adult")
	} else {
		fmt.Println("Minor")
	}

	// If with initialization and else-if
	if num := x * 2; num > 15 {
		fmt.Println("Large number")
	} else if num > 10 {
		fmt.Println("Medium number")
	} else {
		fmt.Println("Small number")
	}

	// Struct literal - creating Person instances
	person1 := Person{name: "Alice", age: 30, city: "NYC"}
	person2 := Person{name: "Bob", age: 25, city: "LA"}

	// Struct literal - creating Rectangle instance
	rect := Rectangle{width: 10.5, height: 20.0}

	// Using methods on structs
	area := rect.Area()
	perimeter := rect.Perimeter()

	fmt.Println("Area:", area)
	fmt.Println("Perimeter:", perimeter)

	// Map literal - initializing with key-value pairs
	ages := map[string]int{
		"Alice": 30,
		"Bob":   25,
		"Carol": 28,
	}

	// Map literal - creating coordinate map
	coordinates := map[string]float64{
		"x": 10.5,
		"y": 20.3,
		"z": 5.7,
	}

	// Empty map literal
	emptyMap := map[string]bool{}

	// Nested if statements with map access
	if val := ages["Alice"]; val > 0 {
		if val >= 18 {
			fmt.Println("Alice is an adult")
		}
	}

	// Method calls on struct instances
	if person1.IsAdult() {
		fmt.Println(person1.name, "is an adult")
	}

	person2.UpdateName("Robert")
	fmt.Println("Updated name:", person2.name)

	// Composite literal for nested structs
	data := map[int]Person{
		1: Person{name: "Dave", age: 35, city: "Boston"},
		2: Person{name: "Eve", age: 40, city: "Seattle"},
	}

	fmt.Println(data)
	fmt.Println(coordinates)
	fmt.Println(emptyMap)
}
