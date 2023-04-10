import pandas as pd
import re
from rosas import estrofa

df = pd.read_csv("data/pagina.csv")
advs = df["text"].to_list()

cortos = []
for adv in advs:
    if len(adv) < 100: # 203 de 5994
        cortos.append(adv)
    # Si no tienen signos de puntuación...
    # Si tienen 16 sílabas (o mejor: 8 pies + 8 pies)

with open("data/terminaciones_all.txt", "a", encoding="utf-8") as f:
    for corto in cortos:
        corto = re.sub("\s*ADV$", "", corto)
        corto = corto.split()
        rima = corto[-2:]
        f.write(" ".join(rima) + "\n")

with open("data/poemas_generados.txt", "a", encoding="utf-8") as f:
    for corto in cortos:
        corto = re.sub("\s*ADV$", "", corto)
        try:
            f.write(estrofa(corto) + "\n")
        except:
            pass

