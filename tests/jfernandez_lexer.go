// Algorithm to validate lexer tokens for Juan Fernández's contributions

package main // PACKAGE

import "fmt" // IMPORT

// Testing FLOAT64 literals with different formats
var pi float64 = 3.14159                    // VAR, FLOAT64_TYPE, FLOAT64
const gravity float64 = 9.8                 // CONST, FLOAT64_TYPE, FLOAT64
var scientific float64 = 1.5e10             // FLOAT64 with scientific notation
var negativeExp float64 = 2.5e-3            // FLOAT64 with negative exponent
var noDecimal float64 = 5e2                 // FLOAT64 without decimal point
var startWithDot float64 = .456             // FLOAT64 starting with dot

// Testing STRING literals
var greeting string = "Hello, World!"       // VAR, STRING_TYPE, STRING
var escaped string = "Line 1\nLine 2"       // STRING with escape sequence
var quotes string = "He said \"Hi\""        // STRING with escaped quotes
var empty string = ""                       // Empty STRING

// Testing type declarations and struct
type Point struct {                         // TYPE, IDENTIFIER, STRUCT
    x float64                               // FLOAT64_TYPE
    y float64
}

// Testing logical operators
func testLogicalOps(a bool, b bool) bool {  // FUNC, BOOL_TYPE
    andResult := a && b                     // SHORT_ASSIGN, LAND
    orResult := a || b                      // LOR
    notResult := !a                         // LNOT

    complex := (a && b) || (!a && !b)       // Combination of LAND, LOR, LNOT

    return andResult || orResult || notResult || complex
}

// Testing compound assignment operators
func testCompoundAssignments() {            // FUNC
    var num int = 10                        // VAR, INT_TYPE, ASSIGN
    num += 5                                // PLUS_ASSIGN
    num -= 3                                // MINUS_ASSIGN
    num *= 2                                // MULT_ASSIGN
    num /= 4                                // DIV_ASSIGN
    num %= 3                                // MOD_ASSIGN

    var bits int = 8
    bits &= 7                               // AND_ASSIGN
    bits |= 4                               // OR_ASSIGN
    bits ^= 2                               // XOR_ASSIGN
    bits <<= 1                              // LSHIFT_ASSIGN
    bits >>= 2                              // RSHIFT_ASSIGN

    var price float64 = 100.50              // FLOAT64
    price += 25.75                          // PLUS_ASSIGN with FLOAT64
    price -= 10.25                          // MINUS_ASSIGN with FLOAT64
    price *= 1.15                           // MULT_ASSIGN with FLOAT64
    price /= 2.0                            // DIV_ASSIGN with FLOAT64
}

// Testing switch-case statements
func testSwitchCase(value int) string {     // FUNC, INT_TYPE, STRING_TYPE
    var result string                       // VAR, STRING_TYPE

    switch value {                          // SWITCH
    case 1:                                 // CASE
        result = "One"                      // ASSIGN, STRING
    case 2:                                 // CASE
        result = "Two"
    case 3:                                 // CASE
        result = "Two or Three"
    default:                                // DEFAULT
        result = "Other"
    }

    return result                           // RETURN
}

// Testing nested switch with logical operators
func evaluateGrade(score float64) string {  // FUNC, FLOAT64_TYPE, STRING_TYPE
    passed := score >= 60.0                 // SHORT_ASSIGN, GE, FLOAT64
    excellent := score >= 90.0              // GE, FLOAT64

    switch {                                // SWITCH without expression
    case excellent && passed:               // CASE, LAND
        return "Excellent"                  // RETURN, STRING
    case passed && !excellent:              // LAND, LNOT
        return "Passed"
    default:                                // DEFAULT
        return "Failed"
    }
}

func main() {                               // FUNC
    // Test logical operators
    isTrue := true                          // SHORT_ASSIGN, TRUE
    isFalse := false                        // SHORT_ASSIGN, FALSE

    logicResult := testLogicalOps(isTrue, isFalse)  // IDENTIFIER

    // Test compound assignments
    testCompoundAssignments()

    // Test switch-case
    dayName := testSwitchCase(1)            // SHORT_ASSIGN

    // Test strings and float64
    message := "Testing complete"           // SHORT_ASSIGN, STRING
    version := 2.5                          // FLOAT64

    // Complex logical expression
    condition := (isTrue || isFalse) && (!isFalse)  // LOR, LAND, LNOT

    // Grade evaluation
    grade := evaluateGrade(85.5)            // FLOAT64

    // Print results
    fmt.Println(logicResult)
    fmt.Println(dayName)
    fmt.Println(message, version)
    fmt.Println(condition)
    fmt.Println(grade)

    // Create a Point instance
    p := Point{x: 3.14, y: 2.71}  // ← prueba esto           // IDENTIFIER, LBRACE, FLOAT64, RBRACE
    fmt.Println(p.x, p.y)
}
