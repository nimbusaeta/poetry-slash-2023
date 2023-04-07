import pandas as pd
import re

df = pd.read_csv("data/pagina.csv")
advs = df["text"].to_list()

cortos = []
for adv in advs:
    if len(adv) < 100: # 203 de 5994
        cortos.append(adv)

with open("data/terminaciones.txt", "a", encoding="utf-8") as f:
    for corto in cortos:
        corto = re.sub("\s*ADV$", "", corto)
        corto = corto.split()
        rima = corto[-2:]
        f.write(" ".join(rima) + "\n")

