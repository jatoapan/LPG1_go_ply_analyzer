// Algorithm to validate lexer tokens

package main // PACKAGE

import "fmt" // IMPORT

var age int = 20                     // VAR, INT_TYPE, INT
const baseSalary float64 = 470.50    // CONST, FLOAT64_TYPE, FLOAT64
var isActive bool := true            // VAR, BOOL_TYPE, SHORT_ASSIGN, TRUE
var name string = "Jose"             // VAR, STRING_TYPE, STRING

func calculate(a int, b int) int {   // FUNC, IDENTIFIER, INT_TYPE
    return a + b - 1 * 2 / 4 % 3     // RETURN, arithmetic ops, INT
}

func main() {
    age++                            // PLUSPLUS
    baseSalary--                     // MINUSMINUS
    isActive = false                 // ASSIGN, FALSE
    name := "User"                   // SHORT_ASSIGN, STRING

    result := age * 2 / 4 % 3        // arithmetic ops
    isEqual := age == 26             // EQ
    isDifferent := age != 20         // NEQ
    isLess := age < 30               // LT
    isLessOrEqual := age <= 40       // LE
    isGreater := age > 15            // GT
    isGreaterOrEqual := age >= 10    // GE

    var status bool = true           // VAR, BOOL_TYPE, TRUE
    var message string := "Lexer test completed" // STRING

    fmt.Println(result)
    fmt.Println(isEqual, isDifferent, isLess, isLessOrEqual, isGreater, isGreaterOrEqual)
    fmt.Println(status, message)
}
