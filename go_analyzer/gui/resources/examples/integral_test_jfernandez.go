package main

import "fmt"

// ---------------------------------------------------------
// 1. PRUEBA SINTÁCTICA: STRUCTS (Responsabilidad Juan)
// ---------------------------------------------------------
type Usuario struct {
	id     int
	nombre string
	activo bool
	saldo  float64
}

// ---------------------------------------------------------
// 2. PRUEBA SEMÁNTICA: RE-DECLARACIÓN DE FUNCIONES (ERROR)
// Regla Juan: No permitir dos funciones con el mismo nombre.
// ---------------------------------------------------------
func iniciarSistema() int {
	return 1
}

func iniciarSistema() int { // <--- EL ANALIZADOR DEBE REPORTAR ERROR AQUÍ
	return 0
}

// ---------------------------------------------------------
// 3. PRUEBA SINTÁCTICA: MÉTODOS CON RECEPTOR
// Regla Juan: func (r Receiver) Nombre()
// ---------------------------------------------------------
func (u Usuario) EsValido() bool {
	// Prueba de Operadores Lógicos (&&, ||, !)
	if u.activo && (u.saldo > 0.0 || !u.activo) {
		return true
	}
	return false
}

func main() {
	// -----------------------------------------------------
	// 4. PRUEBA SINTÁCTICA: MAPS (Responsabilidad Juan)
	// -----------------------------------------------------
	var baseDeDatos map[string]Usuario

	// Inicialización compuesta de Map con Structs anidados
	baseDeDatos = map[string]Usuario{
		"admin": {
			id:     1,
			nombre: "Juan",
			activo: true,
			saldo:  100.50,
		},
	}

	// -----------------------------------------------------
	// 5. PRUEBA SEMÁNTICA: RE-DECLARACIÓN VARIABLES (ERROR)
	// Regla Juan: Validar ámbito local.
	// -----------------------------------------------------
	var intentos int = 0
	var maximo int = 5

	var intentos int = 10 // <--- EL ANALIZADOR DEBE REPORTAR ERROR AQUÍ

	// -----------------------------------------------------
	// 6. PRUEBA DE ÁMBITOS (SCOPE) Y SHADOWING (VÁLIDO)
	// Regla Juan: Esto NO debe dar error porque está dentro del IF
	// -----------------------------------------------------

	// Estructura de Control IF / ELSE IF / ELSE
	if usuario := baseDeDatos["admin"]; usuario.EsValido() {

		var intentos int = 1 // Válido: Shadowing (nueva variable en scope interno)
		fmt.Println("Acceso concedido")

		// -------------------------------------------------
		// 7. PRUEBA LÉXICA: ASIGNACIONES COMPUESTAS
		// Regla Juan: +=, *=, <<=
		// -------------------------------------------------
		intentos += 1
		intentos *= 2
		intentos <<= 1 // Bitwise shift assignment

	} else if intentos >= maximo {
		fmt.Println("Bloqueado")
	} else {
		fmt.Println("Intente de nuevo")
	}
}
