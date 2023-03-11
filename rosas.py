from pyverse import Pyverse
import random

cosas_y_atributos = {
    "Florencia": "bonita",
    "la ocurrencia": "osada",
    "la leña": "marrón",
    "la nuez": "marrón"
}

def busca_rima(frase):
    frase_en_lista = frase.split()
    ultima_palabra = frase_en_lista[-1]
    try:
        verse = Pyverse(ultima_palabra)
        rima = verse.consonant_rhyme
        return rima
    except:
        print("error en " + ultima_palabra)

def busca_cosa_atributo(frase):
    rima = busca_rima(frase)
    print("Tiene que rimar con", rima) # Así vemos si Pyverse ha visto bien la rima
    cosas_candidatas = []
    for cosa in cosas_y_atributos:
        if cosa.endswith(rima):
            cosas_candidatas.append(cosa)
    
    if len(cosas_candidatas) == 0: # No hay rima
        print("No se me ocurre una palabra que rime y que tenga un atributo con el que pueda hacer el poema.")
    elif len(cosas_candidatas) == 1: # Solo hay una palabra que rime en el diccionario
        cosa_elegida = cosas_candidatas[0]
        atributo = cosas_y_atributos[cosa_elegida]
        return cosa_elegida, atributo
    else: # Hay varias palabras que riman en el diccionario, así que escoge una al azar
        index_al_azar = random.randint(0, len(cosas_candidatas)-1)
        cosa_elegida = cosas_candidatas[index_al_azar]
        atributo = cosas_y_atributos[cosa_elegida]
        return cosa_elegida, atributo

def estrofa(frase):
    try:
        cosa, atributo = busca_cosa_atributo(frase)
        return "\nLas rosas son rojas\n" + atributo + " es " + cosa + "\n" + frase
    except:
        pass

def main():
    frase = input("Dime una frase y te hago un poema: ")
    poema = estrofa(frase)
    print(poema)

main()