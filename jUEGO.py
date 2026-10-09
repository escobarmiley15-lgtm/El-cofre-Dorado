import json
import os
import random

ARCHIVO_GUARDADO = "partida.json"


# =========================
# DATOS DEL JUEGO
# =========================
def crear_partida():
    return {
        "jugador": {
            "nombre": "",
            "vida": 100,
            "monedas": 0,
            "objetos": [],
            "logros": []
        },
        "dificultad": "Normal",
        "pistas": 0,
        "objetos_encontrados": 0,
        "templo_superado": False
    }


# =========================
# GUARDAR Y CARGAR
# =========================
def guardar_partida(partida):
    with open(ARCHIVO_GUARDADO, "w", encoding="utf-8") as archivo:
        json.dump(partida, archivo, indent=4, ensure_ascii=False)
    print("\n✓ Progreso guardado correctamente.")


def cargar_partida():
    if not os.path.exists(ARCHIVO_GUARDADO):
        print('\n⚠ Archivo no encontrado. No existe una partida guardada.')
        return None

    try:
        with open(ARCHIVO_GUARDADO, "r", encoding="utf-8") as archivo:
            partida = json.load(archivo)
        print("\n✓ Partida cargada correctamente.")
        return partida
    except (json.JSONDecodeError, OSError):
        print("\n⚠ No se pudo cargar la partida.")
        return None


# =========================
# UTILIDADES
# =========================
def pausa():
    input("\nPresiona ENTER para continuar...")


def mostrar_estado(partida):
    jugador = partida["jugador"]
    print("\n========== ESTADO ==========")
    print(f"Jugador: {jugador['nombre']}")
    print(f"Vida: {jugador['vida']}")
    print(f"Monedas: {jugador['monedas']}")
    print(f"Objetos: {', '.join(jugador['objetos']) if jugador['objetos'] else 'Ninguno'}")
    print(f"Pistas encontradas: {partida['pistas']}")
    print(f"Logros: {', '.join(jugador['logros']) if jugador['logros'] else 'Ninguno'}")
    print("============================")


# =========================
# NUEVA PARTIDA
# =========================
def nueva_partida():
    partida = crear_partida()

    print("\n========== NUEVA PARTIDA ==========")
    nombre = input("Escribe el nombre de tu aventurero: ").strip()

    if not nombre:
        nombre = "Aventurero"

    partida["jugador"]["nombre"] = nombre

    print("\nSelecciona el nivel de dificultad:")
    print("1. Fácil")
    print("2. Normal")
    print("3. Difícil")

    while True:
        opcion = input("Opción: ").strip()
        if opcion == "1":
            partida["dificultad"] = "Fácil"
            break
        elif opcion == "2":
            partida["dificultad"] = "Normal"
            break
        elif opcion == "3":
            partida["dificultad"] = "Difícil"
            break
        else:
            print("Opción inválida.")

    print(f"\n¡Bienvenido, {nombre}!")
    print("Tu misión es explorar el mundo, encontrar pistas,")
    print("superar el templo y obtener el Cofre Dorado.")

    guardar_partida(partida)
    explorar_mapa(partida)


# =========================
# EXPLORAR EL MAPA
# =========================
def explorar_mapa(partida):
    while True:
        print("\n========== EXPLORAR EL MAPA ==========")
        print("1. Buscar objetos")
        print("2. Buscar pistas")
        print("3. Interactuar con personajes")
        print("4. Ver estado")
        print("5. Ir a la puerta del templo")
        print("6. Guardar progreso")
        print("7. Volver al menú principal")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            encontrar_objeto(partida)

        elif opcion == "2":
            encontrar_pista(partida)

        elif opcion == "3":
            hablar_personaje(partida)

        elif opcion == "4":
            mostrar_estado(partida)
            pausa()

        elif opcion == "5":
            if partida["objetos_encontrados"] >= 1 or partida["pistas"] >= 1:
                print("\n✓ Has encontrado suficientes pistas para localizar el templo.")
                entrar_templo(partida)
                if partida["templo_superado"]:
                    return
            else:
                print("\n⚠ No encuentras la puerta del templo.")
                print("Explora el mapa y busca objetos o pistas.")

        elif opcion == "6":
            guardar_partida(partida)

        elif opcion == "7":
            return

        else:
            print("Opción inválida.")


def encontrar_objeto(partida):
    objetos = [
        "Llave antigua",
        "Mapa misterioso",
        "Poción de vida",
        "Medallón dorado"
    ]

    objeto = random.choice(objetos)

    if objeto not in partida["jugador"]["objetos"]:
        partida["jugador"]["objetos"].append(objeto)
        partida["objetos_encontrados"] += 1

        if objeto == "Poción de vida":
            partida["jugador"]["vida"] = min(100, partida["jugador"]["vida"] + 20)
            print("\n✓ Encontraste una Poción de vida. Recuperaste 20 puntos de vida.")
        else:
            print(f"\n✓ Encontraste: {objeto}")

        if partida["objetos_encontrados"] == 1:
            if "Primer descubrimiento" not in partida["jugador"]["logros"]:
                partida["jugador"]["logros"].append("Primer descubrimiento")
                print("🏆 ¡Logro desbloqueado: Primer descubrimiento!")
    else:
        print(f"\nYa tienes el objeto: {objeto}")


def encontrar_pista(partida):
    partida["pistas"] += 1
    print("\n🔎 Encontraste una pista.")
    print("La pista dice: 'La entrada del templo está oculta entre las ruinas.'")

    if partida["pistas"] >= 2:
        print("✓ Ya tienes suficientes pistas para encontrar la entrada.")


def hablar_personaje(partida):
    print("\n👤 Un personaje misterioso se acerca...")
    print('"Si buscas el Cofre Dorado, primero deberás superar el templo."')
    print("Te entrega una moneda como ayuda.")
    partida["jugador"]["monedas"] += 1


# =========================
# TEMPLO
# =========================
def entrar_templo(partida):
    print("\n========== TEMPLO ==========")
    print("Has encontrado la entrada del templo.")
    print("Dentro hay acertijos, trampas y enemigos.")

    while not partida["templo_superado"]:
        print("\n¿Qué deseas hacer?")
        print("1. Resolver un acertijo")
        print("2. Evitar una trampa")
        print("3. Enfrentar a un enemigo")
        print("4. Salir del templo")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            if resolver_acertijo(partida):
                completar_templo(partida)
                break

        elif opcion == "2":
            if evitar_trampa(partida):
                print("\n✓ Has superado la trampa.")
            else:
                if partida["jugador"]["vida"] <= 0:
                    print("\n💀 Tu vida llegó a cero.")
                    print("Debes reiniciar la aventura.")
                    return

        elif opcion == "3":
            if derrotar_enemigo(partida):
                print("\n✓ Enemigo derrotado.")
            else:
                if partida["jugador"]["vida"] <= 0:
                    print("\n💀 Has sido derrotado.")
                    print("Debes reiniciar la aventura.")
                    return

        elif opcion == "4":
            print("\nRegresas al mapa para seguir explorando.")
            return

        else:
            print("Opción inválida.")


def resolver_acertijo(partida):
    print("\n🧩 ACERTIJO")
    print("Tengo ciudades pero no casas,")
    print("tengo montañas pero no árboles.")
    print("¿Qué soy?")
    print("1. Un mapa")
    print("2. Un libro")
    print("3. Una brújula")

    respuesta = input("Respuesta: ").strip()

    if respuesta == "1" or respuesta.lower() == "mapa":
        print("\n✓ ¡Respuesta correcta!")
        partida["jugador"]["logros"].append(
            "Maestro de acertijos"
        ) if "Maestro de acertijos" not in partida["jugador"]["logros"] else None
        return True

    print("\n✗ Respuesta incorrecta.")
    print("Debes volver a intentarlo.")
    return False


def evitar_trampa(partida):
    opciones = ["izquierda", "derecha", "centro"]
    correcta = random.choice(opciones)

    print("\n⚠ Hay una trampa delante.")
    print("Elige: izquierda, derecha o centro.")
    respuesta = input("Tu elección: ").strip().lower()

    if respuesta == correcta:
        return True

    dano = 15 if partida["dificultad"] == "Fácil" else 20
    if partida["dificultad"] == "Difícil":
        dano = 30

    partida["jugador"]["vida"] -= dano
    print(f"\n✗ Activaste la trampa y perdiste {dano} puntos de vida.")
    print(f"Vida restante: {partida['jugador']['vida']}")
    return False


def derrotar_enemigo(partida):
    print("\n💀 ¡Apareció un guardián del templo!")
    print("1. Atacar")
    print("2. Huir")

    opcion = input("Opción: ").strip()

    if opcion == "2":
        print("\nHas escapado del enemigo.")
        return False

    if opcion != "1":
        print("\nOpción inválida.")
        return False

    probabilidad = {
        "Fácil": 0.80,
        "Normal": 0.65,
        "Difícil": 0.50
    }

    if random.random() <= probabilidad[partida["dificultad"]]:
        recompensa = random.randint(10, 30)
        partida["jugador"]["monedas"] += recompensa
        print(f"\n✓ Derrotaste al guardián.")
        print(f"Ganaste {recompensa} monedas.")
        return True

    dano = 20 if partida["dificultad"] != "Difícil" else 30
    partida["jugador"]["vida"] -= dano
    print(f"\n✗ El enemigo te golpeó. Perdiste {dano} de vida.")
    print(f"Vida restante: {partida['jugador']['vida']}")
    return False


def completar_templo(partida):
    partida["templo_superado"] = True
    print("\n🎉 ¡Has completado todos los desafíos del templo!")
    print("La puerta secreta se abre...")
    pausa()
    obtener_cofre(partida)


# =========================
# COFRE DORADO
# =========================
def obtener_cofre(partida):
    print("\n========== COFRE DORADO ==========")
    print("🏆 ¡Has encontrado el Cofre Dorado!")
    print("Dentro encuentras:")
    print("• 100 monedas")
    print("• Un objeto especial")
    print("• Un logro")

    partida["jugador"]["monedas"] += 100

    if "Amuleto del Explorador" not in partida["jugador"]["objetos"]:
        partida["jugador"]["objetos"].append("Amuleto del Explorador")

    if "Cazador del Cofre Dorado" not in partida["jugador"]["logros"]:
        partida["jugador"]["logros"].append("Cazador del Cofre Dorado")

    print("\n✓ Recompensas obtenidas.")
    mostrar_estado(partida)
    pausa()

    jugar_de_nuevo(partida)


# =========================
# JUGAR DE NUEVO
# =========================
def jugar_de_nuevo(partida):
    print("\n========== FIN DE LA AVENTURA ==========")
    print("¿Deseas jugar de nuevo?")
    print("1. Sí, conservar logros")
    print("2. No, salir")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        logros = partida["jugador"]["logros"][:]
        nueva = crear_partida()
        nueva["jugador"]["logros"] = logros
        nueva["jugador"]["nombre"] = partida["jugador"]["nombre"]

        print("\n✓ Se conservaron tus logros.")
        explorar_mapa(nueva)

    else:
        print("\n¡Gracias por jugar 'Busca el Cofre Dorado'!")
        print("¡Hasta la próxima, aventurero! 🎮")


# =========================
# OPCIONES
# =========================
def opciones():
    print("\n========== CONFIGURACIÓN ==========")
    print("1. Sonido")
    print("2. Gráficos")
    print("3. Controles")
    print("4. Idioma")
    print("5. Volver")

    while True:
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            print("\nSonido: Activado")
        elif opcion == "2":
            print("\nGráficos: Calidad media")
        elif opcion == "3":
            print("\nControles: Teclado")
        elif opcion == "4":
            print("\nIdioma: Español")
        elif opcion == "5":
            return
        else:
            print("Opción inválida.")


# =========================
# MENÚ PRINCIPAL
# =========================
def menu_principal():
    while True:
        print("\n")
        print("╔════════════════════════════════════════════╗")
        print("║       AVENTURA DE EXPLORACIÓN              ║")
        print("║          BUSCA EL COFRE DORADO             ║")
        print("╠════════════════════════════════════════════╣")
        print("║  1. Nueva partida                          ║")
        print("║  2. Cargar partida                         ║")
        print("║  3. Opciones                               ║")
        print("║  4. Salir                                  ║")
        print("╚════════════════════════════════════════════╝")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            nueva_partida()

        elif opcion == "2":
            partida = cargar_partida()
            if partida:
                explorar_mapa(partida)

        elif opcion == "3":
            opciones()

        elif opcion == "4":
            print("\n¡Gracias por jugar! 👋")
            break

        else:
            print("\n⚠ Opción inválida. Intenta nuevamente.")


# =========================
# INICIO DEL PROGRAMA
# =========================
if __name__ == "__main__":
    print("==============================================")
    print("   AVENTURA DE EXPLORACIÓN: COFRE DORADO")
    print("==============================================")
    menu_principal()
