#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 13:03:38 2023

@author: alessandrooddone
"""
import pandas as pd
import numpy as np

data = pd.read_csv('datasetpulito.csv')
data = data.set_index('appid', verify_integrity=True)

#trova la distanza tra un vettore di preferenza e un vettore di un gioco
def distance(a, b):
    p1 = np.sum([(x * x) for x in a])
    p2 = np.sum([(y * y) for y in b])
    p3 = -1 * np.sum([(2 * x*y) for (x, y) in zip(a, b)])
    dist = np.sqrt(np.sum(p1 + p2 + p3))
    return dist
    # c = pd.DataFrame()
    # c = [abs(a[i]-b[i]) for i in range(len(a))]
    # #print(c)
    # return sum(c)

#ritorna il vettore di un gioco
def genre_vector(appid):
    vector = data.loc[appid]
    buffer = vector.drop(['name', 'reviews', 'header_image'])
    return buffer

#normalizza pesi in percentuali
def normalize_vector(vect):
    summ = sum(vect)
    for i in range(len(vect)):
        vect[i] = vect[i]/summ
    return vect

def normal_genre_vector(appid):
    return normalize_vector(genre_vector(appid))

#ritorna il vettore preferenza dato un array dei game ID preferiti
def sum_favourites(pref):
    ser = pd.Series()
    print(pref)
    for appid in pref:
        ser = ser.add(normal_genre_vector(appid), fill_value=0)
    normalize_vector(ser)
    print(ser)
    return ser

#dato un vettore preferenza ritorna gli n giochi piu' simili
def rank_game_distance(pref):
    d = {'appid': [], 'distance': []}
    df = pd.DataFrame(data=d)
    for appid in data.index:
        print(appid)
        df.loc[len(df)] = [appid, distance(pref, normal_genre_vector(appid))]
    df.set_index('appid', inplace=True)
    return df

#Prende una lista di appid e ne ritorna gli n piu' vicini
def game_suggestions(pref, n):
    fav_vect = sum_favourites(pref)
    final = rank_game_distance(fav_vect)
    final.drop(pref, inplace=True)
    print(final.nsmallest(n, 'distance'))
    return final.nsmallest(n, 'distance')

#Prende un array di appid e ne ritorna array di nomi
def game_names(ids):
    return [data.loc[ID]['name'] for ID in ids]

#prende due appid e ne ritorna la distanza
def test_func(uno,due):
    gioco1 = genre_vector(uno)
    gioco2 = genre_vector(due)

    a = normalize_vector(gioco1)
    b = normalize_vector(gioco2)

    return distance(a,b)

#print(test_func(10, 240))


#pref = [238960,210970,221380]

#sugg = game_suggestions(pref, 20)
#print(game_names(sugg.index))
