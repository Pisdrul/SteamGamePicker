
"""
Created on Mon Jan  9 11:11:12 2023

@author: Alessandro Gregori, Francesco Trevisan

"""



import pandas as pd

pesi = pd.read_csv('steamspy_tag_data.csv')
giochi = pd.read_csv('steam.csv')
media = pd.read_csv('steam_media_data.csv')

#unito dataset con tag con quello generico per avere nome del gioco, recensioni e tag in un unico dataset
datasetpulito = giochi.merge(pesi, on= ['appid'],how='outer')

#unito dataset che contiene immagini dei giochi
datasetpulito = datasetpulito.merge(media, on= ['appid'],how='outer')


#tolti giochi non in inglese
datasetpulito=datasetpulito[datasetpulito.english !=0]


#tolte righe vuote
datasetpulito = datasetpulito[datasetpulito.name.notnull()]


#tolti giochi con più recensioni negative di quelle postiive
datasetpulito = datasetpulito.drop(datasetpulito[datasetpulito.positive_ratings<datasetpulito.negative_ratings].index)



#tolti giochi con poche reviews
datasetpulito=datasetpulito.drop(datasetpulito[datasetpulito.positive_ratings+datasetpulito.negative_ratings<1000].index)


#tolti giochi con poche reviews
recensioni = datasetpulito.positive_ratings/(datasetpulito.positive_ratings+datasetpulito.negative_ratings)

#trasformiamo positive ratings e negative ratings in una singola percentuale
datasetpulito.insert(4, 'reviews',recensioni)

#eliminiamo colonne non utili alla nostra analisi
datasetpulito.drop(['release_date','positive_ratings','negative_ratings','achievements','categories','english','price','owners', 'average_playtime','median_playtime','steamspy_tags','developer','publisher','platforms','required_age','genres','screenshots','background','movies'],axis=1, inplace=True)


#tolte colonne inutili
print(datasetpulito)


datasetpulito.to_csv('datasetpulito.csv',index=False)
