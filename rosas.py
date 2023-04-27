from pyverse import Pyverse
import random
import re
import json

with open("versos_sueltos.txt", "r", encoding="utf-8") as v:
    cosas_y_atributos = json.load(v)

# TODO: Carmen Mola son tres
# tres son Carmen Mola

def busca_rima(frase):
    frase_en_lista = frase.split()
    ultima_palabra = frase_en_lista[-1]

    # casos especiales
    Reagan = re.match("Reagan", ultima_palabra)
    if Reagan:
        rima = "igan"
        return rima

    # buscar la rima de una palabra acabada en vocal e -y
    termina_en_vocal_e_y = re.match("(.*?)([aeiouáéíóúAEIOUÁÉÍÓÚ])([yY])$", ultima_palabra)
    if termina_en_vocal_e_y:
        rima = (termina_en_vocal_e_y.group(2) + "y", termina_en_vocal_e_y.group(2) + "i")
        return rima

    # buscar la rima de un monosílabo con diptongo
    # TODO: que tmb busque la rima en palabras polisílabas
    monosílabo_dip = re.match("^([b-df-hj-np-tv-zñB-DF-HJ-NP-TV-ZÑ]{0,2})([aeiouáéíóúAEIOUÁÉÍÓÚ])([aeiouáéíóúAEIOUÁÉÍÓÚ])([b-df-hj-np-tv-zñB-DF-HJ-NP-TV-ZÑ]{0,2})$", ultima_palabra)
    if monosílabo_dip:
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
        rima = vocal_acentuada + monosílabo_dip.group(4)
        return rima

    # buscar la rima de un monosílabo
    # TODO: que tmb busque la rima en palabras polisílabas
    monosílabo = re.match("^([b-df-hj-np-tv-zñB-DF-HJ-NP-TV-ZÑ]{0,2})([aeiouáéíóúAEIOUÁÉÍÓÚ])([b-df-hj-np-tv-zñB-DF-HJ-NP-TV-ZÑ]{0,2})$", ultima_palabra)
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
    # TODO: suéter - tinder, océano - mano, fértil - vaginesil, dramático - chico
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
    if "bv" in rima:
        return (rima, re.sub("bv", "v", rima), re.sub("bv", "b", rima))
    elif "b" in rima:
        return (rima, re.sub("b", "v", rima), re.sub("b", "bv", rima))
    elif "v" in rima:
        return (rima, re.sub("v", "b", rima), re.sub("v", "bv", rima))
    else:
        return rima

def enriquecer_chtx(rima):
    if "ch" in rima:
        return (rima, re.sub("ch", "tx", rima))
    elif "tx" in rima:
        return (rima, re.sub("tx", "ch", rima))
    else:
        return rima

def busca_cosa_atributo(frase):
    rima = busca_rima(frase)

    # ampliaciones
    rima = enriquecer_bv(rima)
    rima = enriquecer_chtx(rima)

    print("Tiene que rimar con", rima) # Así vemos si Pyverse ha visto bien la rima # TODO: cuando haya varias, que lo formatee bien
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
        # si la última palabra de la cosa que encuentra coincide con la última palabra de frase, excluye la cosa de las candidatas
        frase_en_lista = frase.split()
        ultima_palabra = frase_en_lista[-1]
        for cosa_candidata in cosas_candidatas:
            cosa_candidata_en_lista =  cosa_candidata.split()
            ultima_palabra_cosa_candidata = cosa_candidata_en_lista[-1]
            if ultima_palabra == ultima_palabra_cosa_candidata:
                cosas_candidatas.remove(cosa_candidata)

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

main()