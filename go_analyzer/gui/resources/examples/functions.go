// Example demonstrating function declarations
package main

import "fmt"

// Function that adds two integers
func add(a int, b int) int {
    return a + b
}

// Function that multiplies two integers
func multiply(x int, y int) int {
    result := x * y
    return result
}

// Function with no return value
func greet(name string) {
    fmt.Println("Hello,", name)
}

func main() {
    sum := add(5, 3)
    product := multiply(4, 7)

    fmt.Println("Sum:", sum)
    fmt.Println("Product:", product)

    greet("World")
}
