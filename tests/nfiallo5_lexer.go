// Algorithm to validate lexer from Nicolas Fiallo
package main
import "fmt"

const str string = "hola mundo" //string
var numero = 20                 //int
var negativo float64 = -14.5    //float64

func powerOf2(a int) int {
	return 1 << a //function
}

func isWeekDay(day string) string {
	switch day {
	case "monday", "tuesday", "wednesday", "thursday", "friday":
		return "It's a weekday"
	case "saturday", "sunday":
		return "It's the weekend"
	default:
		return "Not a valid day"
	}
}

func main() {
	numero++                     //plus-plus
	x := powerOf2(3)               //assign
	var booleano bool = true       //boolean
	var num = []int{1, 2, 3, 4, 5} //array
	var edades map[string]int

	for i := 0; i < 5; i++ { //for loop
		if i == 3 {
			continue //continue
		}
		if i == 4 {
			break //break
		}
	}

	/*
		It validates multi-line comments
	*/
	if x == 8 { //if statement
		fmt.Println(str)
	} else if booleano {
		numero-- //minus-minus
	} else { //else statement
		fmt.Println("mal calculado")
	}

    nums := []int{1, 2, 3, 4, 5}
    totalSum := 0
    for i := 0; i < len(nums); i++ {
        totalSum += nums[i]
    }
    fmt.Println("Total Sum:", totalSum)

    for i := 0; i < len(num); i++ {
        fmt.Println("Indice:", i, "Valor:", num[i])
    }
}