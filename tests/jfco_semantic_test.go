package main

import "fmt"

// Test 1: Function redeclaration (should trigger error)
func calculate() int {
    return 42
}

func calculate() int {
    return 100
}

// Test 2: Variable redeclaration in same scope (should trigger error)
var globalX int = 10
var globalX int = 20

func main() {
    // Test 3: Local variable redeclaration (should trigger error)
    var localY int = 5
    var localY int = 10

    // Test 4: This is fine - shadowing in nested scope
    var z int = 1
    if true {
        var z int = 2
        fmt.Println(z)
    }

    fmt.Println(localY)
    fmt.Println(globalX)
    fmt.Println(z)
}
