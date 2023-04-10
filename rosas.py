from pyverse import Pyverse
import random
import re

with open("versos_sueltos.txt", "r", encoding="utf-8") as v:
    cosas_y_atributos = eval(v.read())

# Carmen Mola son tres
# tres son Carmen Mola

def busca_rima(frase):
    frase_en_lista = frase.split()
    ultima_palabra = frase_en_lista[-1]

    # buscar la rima de un monosílabo
    # TODO: fui (rima con -í), que, quién, estoy, soy
    monosílabo = re.match("^([b-df-hj-np-tv-zñ]{0,2})([aeiouáéíóú])([b-df-hj-np-tv-xzñ]{0,2})$", ultima_palabra)
    if monosílabo:
        if "a" in ultima_palabra:
            vocal_acentuada = "á"
        elif "e" in ultima_palabra:
            vocal_acentuada = "é"
        elif "i" in ultima_palabra:
            vocal_acentuada = "í"
        elif "o" in ultima_palabra:
            vocal_acentuada = "ó"
        elif "u" in ultima_palabra:
            vocal_acentuada = "ú"
        rima = vocal_acentuada + monosílabo.group(3)
        return rima

    # buscar la rima de una palabra con tilde
    palabra_con_tilde = "(.*?)([áéíóúÁÉÍÓÚ])(.*)"
    lleva_tilde = re.match(palabra_con_tilde, ultima_palabra)
    if lleva_tilde: # tildes
        rima = lleva_tilde.group(2) + lleva_tilde.group(3)
        return rima
    else:
        try:
            verse = Pyverse(ultima_palabra)
            rima = verse.consonant_rhyme
            return rima
        except:
            print("error en " + ultima_palabra)

def enriquecer_bv(rima):
    # TODO: "obvio" en el ADV
    if "b" in rima:
        return (rima, re.sub("b", "v", rima), re.sub("b", "bv", rima))
    elif "v" in rima:
        return (rima, re.sub("v", "b", rima), re.sub("v", "bv", rima))
    else:
        return rima

def busca_cosa_atributo(frase):
    rima = busca_rima(frase)
    rima = enriquecer_bv(rima)
    # TODO: enriquecer_chtx

    print("Tiene que rimar con", rima) # Así vemos si Pyverse ha visto bien la rima
    cosas_candidatas = []
    for cosa in cosas_y_atributos:
        if cosa.endswith(rima):
            cosas_candidatas.append(cosa)
    
    if len(cosas_candidatas) == 0: # No hay rima
        print("No se me ocurre una palabra que rime y que tenga un atributo con el que pueda hacer el poema.")
        # TODO: listas de adjetivos y de sustantivos y que las combine: pillar de DiaDeTodosLosCorpus
        # TODO: rima asonante
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
        return "\nLas rosas son rojas\n" + atributo + " " + cosa + "\n" + frase
    except:
        pass

def main():
    frase = input("Dime una frase y te hago un poema: ")
    poema = estrofa(frase)
    print(poema)

