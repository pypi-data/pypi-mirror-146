#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 08:37:50 2020

@author: oscar
"""

from copy import deepcopy

import matplotlib.pyplot as plt
import pandas as pd

# from wj_analysis.common.nlp_utils import Polarity as pol_dist
import plotly.graph_objects as go

# import plotly.express as px
from numpy import arange, mean
from textblob import TextBlob

pd.options.mode.chained_assignment = None

FOLDER = "/home/oscar/Labs/Data_social_media/Pruebas PWJ-772 digital-social/Media/"
COLUMN = "text"
WORD = input("Marca a buscar: ")
WORDS = [WORD]

DF_ORG = pd.read_csv(FOLDER + "df_media.csv", index_col=0)

DF_ORG.date_published = pd.to_datetime(DF_ORG.date_published)

DF_ORG[COLUMN] = DF_ORG[COLUMN].apply(lambda x: str(x))
DF_ORG[COLUMN] = DF_ORG[COLUMN].apply(lambda x: x.lower())


def words_filter(df_w, words):
    # filtra la palabra objetivo
    DF_M = deepcopy(df_w)
    DF_M["word"] = None

    for i in range(len(DF_M)):
        for word in words:
            word = word.lower()
            if str(DF_M.text.iloc[i]).find(str(word)) > 0:
                DF_M.word.iloc[i] = "ok"
            else:
                continue

    DF_M_FILTER = DF_M[DF_M.word == "ok"]
    return DF_M_FILTER


DF_FILTER_1 = words_filter(df_w=DF_ORG, words=WORDS)


def find_point(df_p, carac="."):
    # filtra por puntos o el caracter escogido
    DF_P = deepcopy(df_p)
    Position = []
    for i in range(len(df_p)):
        pos = []
        last = 0
        text_c = str(DF_P.text.iloc[i])
        while text_c.find(carac, last) != -1:
            last = text_c.find(carac, last) + 1
            pos.append(last)
        Position.append(pos)
    return Position


DF_FILTER_1["Pos"] = find_point(df_p=DF_FILTER_1, carac=".")

for i in range(len(DF_FILTER_1)):
    plt.plot(
        range(len(DF_FILTER_1.Pos.iloc[i])), DF_FILTER_1.Pos.iloc[i], "o-", label=str(i)
    )
plt.title("Longitud de los textos palabra " + str(WORDS[0]))
plt.legend()
plt.show()

# parte entre puntos
TEXT = int(input("Texto a consultar: "))
text = TEXT
num_caract = 50
text_split = []
first = 0
phrases = []
for i in DF_FILTER_1.Pos.iloc[text]:
    p = DF_FILTER_1.text.iloc[text][first:i]
    long = i - first
    phrases.append(long)
    if long > num_caract:
        text_split.append(p)
    else:
        continue
    first = i


DF_POL = pd.DataFrame(text_split)
DF_POL["title"] = DF_FILTER_1.title.iloc[text]
DF_POL = DF_POL.rename(columns={0: "text"})

pol = []
mention = []
size_point = []
for i in range(len(DF_POL)):
    if str(DF_POL.text.iloc[i]).find(str(WORD)) > 0:
        mention.append(WORD)
        size_point.append(60)
    else:
        mention.append(0)
        size_point.append(20)
    get_pol = TextBlob(DF_POL.text.iloc[i])
    # polarity = get_pol.translate(to='en')
    polarity = get_pol.polarity
    pol.append(polarity)

# pol = pol_dist().polarity(df_text=text_split)

# plt.plot(range(len(pol)), pol, c="pink")
# for i in range(len(pol)):
#     plt.scatter(i, pol[i], s=len(text_split[i]) / 2, c=len(text_split[i]), alpha=0.8)
# plt.title(str(DF_FILTER_1.title.iloc[text]))
# plt.xlabel("numero de la frase")
# plt.ylabel("Polaridad")
# plt.grid()
# plt.show()

len_text = []
scale = mean(phrases) / 5
for i in range(len(text_split)):
    len_text.append(len(text_split[i]) / scale)

num_phrase = arange(0, len(pol))

# tamaño longitud frase
fig = go.Figure(
    data=[
        go.Scatter(
            x=num_phrase,
            y=pol,
            text=text_split,
            mode="markers",
            marker=dict(
                color=len_text,
                size=size_point,
                showscale=True,
                line=dict(width=2, color="MediumPurple"),
                colorbar=dict(
                    title="Tamaño frase",
                    tickvals=[min(len_text), mean(len_text), max(len_text)],
                    ticktext=["Bajo", "Promedio", "Alto"],
                ),
                colorscale="Blues",
            ),
        )
    ]
)

fig.update_traces(mode="markers+lines")
fig.update_layout(
    title=str(
        DF_FILTER_1.title.iloc[text]
        + ", tamaño total texto "
        + str(round(sum(len_text) * scale, 0))
    ),
    xaxis=dict(title="Frase"),
    yaxis=dict(
        title="Polaridad, "
        + "(promedio "
        + str(round(mean(pol), 2))
        + ")"
        + " (rango "
        + str(round((max(pol) - min(pol)), 2))
        + ")"
    ),
)
fig.show()
