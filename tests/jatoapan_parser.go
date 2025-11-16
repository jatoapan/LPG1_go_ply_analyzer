package main

// José Toapanta's Syntax Validation Algorithm for Go Parser
// Tests for lexical and syntactic analysis of Go language subset

// Global variable declarations
var globalCounter int = 100
var globalTemperature float64 = 36.5
var globalName string = "GoProgram"
var globalActive bool = true

const MAX_VALUE int = 1000
const PI float64 = 3.14159

// Multiple return types
func calculateBasic() (int, int, int) {
    result1 := 10 + 5
    result2 := 20 * 2
    result3 := 100 - 30
    return result1, result2, result3
}

// Mixed return types
func getInfo() (string, float64, bool) {
    text := "Information"
    value := 42.5
    flag := true
    return text, value, flag
}

// Basic arithmetic operations
func basicArithmetic() {
    var a int = 10
    var b int = 5
    
    sum := a + b
    difference := a - b
    product := a * b
    quotient := a / b
    remainder := a % b
}

// Multiple arithmetic operators
func complexArithmetic() {
    var x int = 10
    var y int = 5
    var z int = 3
    
    result1 := x + y * z
    result2 := x * y + z
    result3 := x + y + z
    result4 := x - y - z
    result5 := x * y * z
    result6 := x / y + z
}

// Precedence with parentheses
func arithmeticWithParentheses() {
    var a int = 10
    var b int = 5
    var c int = 2
    
    result1 := (a + b) * c
    result2 := a * (b + c)
    result3 := (a - b) * (c + 1)
    result4 := (a + b) / (c + 1)
}

// Short assignment
func shortAssignment() {
    a := 10
    b := 20
    c := 30
    d := 40
}

// Compound assignments
func compoundAssignment() {
    x := 100
    x += 50
    x -= 20
    x *= 2
    x /= 5
    x %= 3
}

// For loop with condition
func forLoopCondition() {
    counter := 0
    for counter < 10 {
        counter += 1
    }
}

// Classic for loop
func forLoopClassic() {
    for i := 0; i < 10; i++ {
        result := i + 1
    }
}

// For loop decrement
func forLoopDecrement() {
    for j := 10; j > 0; j-- {
        product := j * 2
    }
}

// For loop custom step
func forLoopCustomIncrement() {
    for k := 0; k < 20; k += 2 {
        squared := k * k
    }
}

// Infinite for loop
func forLoopInfinite() {
    x := 0
    for {
        x += 2
        if x > 20 {
            break
        }
    }
}

// For with continue
func forLoopContinue() {
    for i := 0; i < 20; i++ {
        if i < 5 {
            continue
        }
        result := i * 2
    }
}

// Nested loops
func nestedForLoops() {
    for i := 0; i < 5; i++ {
        for j := 0; j < 5; j++ {
            sum := i + j
        }
    }
}

// Nested with operations
func nestedWithArithmetic() {
    for i := 1; i < 4; i++ {
        for j := 1; j < 4; j++ {
            product := i * j
            total := i + j
        }
    }
}

// Break in nested loops
func nestedLoopsWithBreak() {
    for i := 0; i < 10; i++ {
        for j := 0; j < 10; j++ {
            if i == 5 && j == 5 {
                break
            }
            value := i * j
        }
    }
}

// Continue in nested loops
func nestedLoopsWithContinue() {
    for i := 0; i < 8; i++ {
        for j := 0; j < 8; j++ {
            if j % 2 == 0 {
                continue
            }
            result := i + j
        }
    }
}

// Break with multiple conditions
func breakWithConditions() {
    counter := 0
    for counter < 100 {
        if counter > 50 && counter < 60 {
            break
        }
        counter += 10
    }
}

// Continue with complex logic
func continueWithLogic() {
    for i := 0; i < 30; i++ {
        if i > 5 && i < 10 || i > 20 {
            continue
        }
        value := i * 2
    }
}

// Int slice
func sliceInt() {
    numbers := []int{1, 2, 3, 4, 5}
    moreNumbers := []int{10, 20, 30, 40}
}

// Float slice
func sliceFloat() {
    temperatures := []float64{36.5, 37.2, 38.1, 39.5}
    values := []float64{1.1, 2.2, 3.3}
}

// String slice
func sliceString() {
    names := []string{"Alice", "Bob", "Charlie"}
    cities := []string{"Madrid", "Barcelona"}
}

// Bool slice
func sliceBool() {
    statuses := []bool{true, false, true}
    flags := []bool{false, true}
}

// Empty slices
func emptySlices() {
    emptyInt := []int{}
    emptyFloat := []float64{}
    emptyString := []string{}
    emptyBool := []bool{}
}

// Slice with expressions
func sliceWithExpressions() {
    nums := []int{1 + 2, 5 * 3, 10 - 4}
    floats := []float64{1.5 + 2.5, 3.0 * 2.0}
}

// Multiple slices
func multipleSlices() {
    intSlice := []int{1, 2, 3, 4, 5}
    floatSlice := []float64{1.1, 2.2, 3.3}
    stringSlice := []string{"one", "two", "three"}
    boolSlice := []bool{true, false}
}

// AND operator
func logicalAND() {
    a := 10
    b := 20
    result := a > 5 && b < 30
    condition := a != 0 && b != 0
}

// OR operator
func logicalOR() {
    x := 5
    y := 15
    condition1 := x < 0 || y > 10
    condition2 := x == 5 || y == 15
}

// NOT operator
func logicalNOT() {
    flag := true
    negFlag := !flag
    condition := !false
}

// Complex logical expressions
func complexLogical() {
    a := 10
    b := 20
    c := 30
    result1 := a > 5 && b < 30 && c > 25
    result2 := a == 10 || b == 15 || c == 30
    result3 := !(a < 5) && (b > 15)
}

// Relational operators
func relationalOps() {
    x := 10
    y := 20
    eq := x == y
    neq := x != y
    lt := x < y
    le := x <= y
    gt := x > y
    ge := x >= y
}

// Post increment
func postIncrement() {
    i := 0
    i++
    j := 5
    j++
}

// Post decrement
func postDecrement() {
    i := 10
    i--
    j := 5
    j--
}

// For with post operators
func forLoopWithPostOp() {
    for i := 0; i < 10; i++ {
        x := i + 1
    }
    
    for j := 10; j > 0; j-- {
        y := j * 2
    }
}

// Four return types
func multiReturn() (int, float64, string, bool) {
    intVal := 42
    floatVal := 3.14
    stringVal := "test"
    boolVal := true
    return intVal, floatVal, stringVal, boolVal
}

// Arithmetic in loop
func arithmeticInLoop() {
    for i := 1; i < 6; i++ {
        result := i * 2 + 5
        expr := (i + 2) * (i - 1)
    }
}

// Global and local variables
func globalLocalTest() {
    localCounter := 50
    localTemp := 25.5
    
    total := globalCounter + localCounter
    tempDiff := globalTemperature + localTemp
}

// Comprehensive validation
func comprehensiveTest() {
    var initial int = 100
    var rate float64 = 0.05
    var description string = "Process"
    var running bool = true
    
    for year := 0; year < 10; year++ {
        initial += 10
        rate += 0.01
    }
    
    for month := 0; month < 12; month++ {
        monthValue := initial * 2
        monthRate := rate * 100.0
    }
    
    numbers := []int{1, 2, 3, 4, 5}
    temps := []float64{20.5, 21.3, 22.1}
    codes := []string{"A", "B", "C"}
}

// Break and continue mixed
func breakContinueMixed() {
    counter := 0
    for counter < 50 {
        if counter % 2 == 0 {
            counter += 1
            continue
        }
        
        if counter > 30 {
            break
        }
        
        value := counter * 3
        counter += 1
    }
}

// Multiple breaks and continues
func multipleBreaKsContinues() {
    for i := 0; i < 15; i++ {
        if i == 3 {
            continue
        }
        
        if i == 7 {
            continue
        }
        
        if i == 12 {
            break
        }
        
        sum := i + 5
    }
}

// Main entry point
func main() {
    var x int = 1000
    var y float64 = 0.05
    var label string = "Start"
    var active bool = true
    
    for i := 0; i < 10; i++ {
        x += 50
        y += 0.01
    }
    
    data := []int{10, 20, 30, 40, 50}
    values := []float64{1.5, 2.5, 3.5}
    
    for j := 0; j < 15; j++ {
        if j == 5 {
            break
        }
        
        if j % 2 == 0 {
            continue
        }
        
        result := j * 2
    }
}