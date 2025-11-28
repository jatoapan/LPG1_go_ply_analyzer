// Example demonstrating control flow statements
package main

import "fmt"

func main() {
    // If-else statement
    x := 10
    if x > 5 {
        fmt.Println("x is greater than 5")
    } else {
        fmt.Println("x is less than or equal to 5")
    }

    // For loop
    sum := 0
    for i := 1; i <= 5; i++ {
        sum = sum + i
    }
    fmt.Println("Sum from 1 to 5:", sum)

    // Nested control structures
    for j := 0; j < 3; j++ {
        if j % 2 == 0 {
            fmt.Println(j, "is even")
        } else {
            fmt.Println(j, "is odd")
        }
    }
}
