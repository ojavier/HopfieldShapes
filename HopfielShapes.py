"""Red de Hopfield para reconocer formas dibujadas en una cuadricula."""


def crear_pesos(patrones):
	"""Crea la matriz de pesos usando la regla de Hebb."""
	cantidad_neuronas = len(patrones[0])
	pesos = [[0 for _ in range(cantidad_neuronas)] for _ in range(cantidad_neuronas)]

	for patron in patrones:
		for i in range(cantidad_neuronas):
			for j in range(cantidad_neuronas):
				pesos[i][j] += patron[i] * patron[j]

	for i in range(cantidad_neuronas):
		pesos[i][i] = 0

	return pesos


def activar(valor, valor_anterior):
	"""Aplica la funcion escalon y conserva el estado si la suma es cero."""
	if valor > 0:
		return 1
	if valor < 0:
		return -1
	return valor_anterior


def recordar(patron, pesos, maximo_iteraciones=20):
	"""Recupera el patron hasta que la red llega a un estado estable."""
	estado = patron[:]

	for _ in range(maximo_iteraciones):
		nuevo_estado = []
		for i in range(len(estado)):
			suma = sum(pesos[i][j] * estado[j] for j in range(len(estado)))
			nuevo_estado.append(activar(suma, estado[i]))

		if nuevo_estado == estado:
			return estado
		estado = nuevo_estado

	return estado


def forma_a_patron(forma):
	"""Convierte una matriz de -1 y 1 en un vector de neuronas."""
	if not forma or not all(forma):
		raise ValueError("La forma debe ser una matriz no vacia")

	ancho = len(forma[0])
	if any(len(fila) != ancho for fila in forma):
		raise ValueError("La forma debe ser una matriz rectangular")
	if any(valor not in (-1, 1) for fila in forma for valor in fila):
		raise ValueError("Una forma solo puede contener -1 y 1")
	return [valor for fila in forma for valor in fila]


def patron_a_forma(patron, ancho):
	"""Convierte un vector de neuronas a una matriz visible."""
	return [patron[fila:fila + ancho] for fila in range(0, len(patron), ancho)]


def mostrar_forma(forma):
	"""Muestra una matriz usando bloques para las neuronas activas."""
	for fila in forma:
		print(" ".join("##" if valor == 1 else ".." for valor in fila))


def agregar_ruido(patron, posiciones):
	"""Invierte las neuronas indicadas para simular una forma incompleta."""
	ruidoso = patron[:]
	for posicion in posiciones:
		if posicion < 0 or posicion >= len(ruidoso):
			raise IndexError("La posicion del ruido esta fuera de la forma")
		ruidoso[posicion] *= -1
	return ruidoso


def similitud(primer_patron, segundo_patron):
	"""Devuelve el porcentaje de neuronas iguales entre dos patrones."""
	iguales = sum(a == b for a, b in zip(primer_patron, segundo_patron))
	return iguales / len(primer_patron)


def emparejar_forma(forma, formas_aprendidas, pesos):
	"""Recupera una forma y devuelve su nombre y nivel de coincidencia."""
	patron = forma_a_patron(forma)
	recuperado = recordar(patron, pesos)
	coincidencias = {
		nombre: similitud(recuperado, patron_aprendido)
		for nombre, patron_aprendido in formas_aprendidas.items()
	}
	nombre = max(coincidencias, key=coincidencias.get)
	return nombre, coincidencias[nombre], recuperado


def patrones_ejemplo():
	"""Patrones 1, 2 y 4 del ejemplo de 8x5."""
	return [
		[
			[-1, -1, 1, -1, -1],
			[-1, -1, 1, -1, -1],
			[-1, -1, 1, -1, -1],
			[-1, -1, 1, -1, -1],
			[-1, -1, 1, -1, -1],
			[-1, -1, 1, -1, -1],
			[-1, -1, 1, -1, -1],
			[-1, -1, 1, -1, -1],
		],
		[
			[1, 1, 1, 1, 1],
			[1, -1, -1, -1, 1],
			[1, -1, -1, -1, 1],
			[-1, -1, 1, -1, -1],
			[-1, 1, 1, 1, -1],
			[1, -1, -1, -1, 1],
			[1, -1, -1, -1, 1],
			[1, 1, 1, 1, 1],
		],
		[
			[1, 1, -1, 1, 1],
			[1, -1, -1, -1, 1],
			[1, -1, -1, -1, 1],
			[1, 1, 1, 1, 1],
			[-1, -1, 1, -1, -1],
			[-1, -1, 1, -1, -1],
			[-1, -1, 1, -1, -1],
			[-1, -1, 1, -1, -1],
		],
	]


def main():
	"""Entrena la red y demuestra el emparejamiento de una forma con ruido."""
	nombres = ["linea", "marco", "flecha"]
	formas_aprendidas = {
		nombre: forma_a_patron(forma)
		for nombre, forma in zip(nombres, patrones_ejemplo())
	}
	pesos = crear_pesos(list(formas_aprendidas.values()))

	forma_entrada = agregar_ruido(formas_aprendidas["flecha"], [10, 17, 31])
	nombre, coincidencia, recuperado = emparejar_forma(
		patron_a_forma(forma_entrada, 5), formas_aprendidas, pesos
	)

	print("Forma de entrada:")
	mostrar_forma(patron_a_forma(forma_entrada, 5))
	print("\nForma recuperada:")
	mostrar_forma(patron_a_forma(recuperado, 5))
	print(f"\nEmparejamiento: {nombre} ({coincidencia:.0%})")


if __name__ == "__main__":
	main()
 