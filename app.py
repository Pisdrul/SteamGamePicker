import streamlit as st
import pandas as pd
import MLpart as ml
import webbrowser
from streamlit_autorefresh import st_autorefresh

dataset= pd.read_csv('datasetpulito.csv')
start, result = st.tabs(['Start','Result'])

#inizializzazione variabili di sessione 
if 'id' not in st.session_state:
    st.session_state['id'] = [] #id giochi scelti dall'utente

if 'images' not in st.session_state:
    st.session_state['images']= [] #immagini dei giochi scelti dall'utente
    

if 'risultatopronto' not in st.session_state:
    st.session_state['risultatopronto']= None #variabile usata per controllare se l'utente ha inserito almeno un gioco, oppure se il back-end ha finito di lavorare
    
if 'risultati' not in st.session_state:
    st.session_state['risultati'] = [] #array con risultati e distanze
    
if 'risultatiappid' not in st.session_state:
    st.session_state['risultatiappid']=[] #array con appid risultati
    
if 'risultatiimg' not in st.session_state:
    st.session_state['risultatiimg'] = [] #array con immagini risultati

with start:
    st.title("SteamGamePicker")
    st.write("Choose up to 10 games that you like and then we'll give you our recommendation!")

    option = st.selectbox('Select a game!',dataset.name)
    col1, col2,col3 = st.columns(3)

    with col1: #pulsante submit
        if st.button('Submit game!'):
            indice=dataset.loc[dataset['name']==option]
            #st.write(indice)
            appid=indice['appid'].iloc[0]
            if len(st.session_state['id'])>=10:
                st.write('Hai già inserito 10 giochi')
            elif appid not in st.session_state['id']:
                st.session_state['id'].append(appid)#aggiunge il gioco all'array preferenze
                image = indice['header_image'].iloc[-1]
                st.session_state['images'].append(image)#aggiunge l'immagine del gioco all'array immagini
            else:
                st.write("Choose something that you havent already put in")

    with col2: #pulsante clear
        if st.button('Clear selections'): #svuota array selezioni
            st.session_state['id'].clear()
            st.session_state['images'].clear()
            st.session_state['risultatopronto']= None
            del(st.session_state['risultati'])
            del(st.session_state['risultatiimg'])
            del(st.session_state['risultatiappid']) #cancella tutte le variabili di sessione
           #problema, se viene premuto durante la computazione del back-end annulla il processo
    with col3: #pulsante che non fa nulla se non lasciare all'utente l'accesso alla results page
        if len(st.session_state['id'])<=10:
            if st.button('Submit preferences'):
                st.write('Go to the Result tab!')
                st.session_state['risultatopronto']= False
        

    st.write('Your games list:') #mostra immagini giochi scelti
    colimg1,colimg2= st.columns(2)
    with colimg1:
        for i in range(0,len(st.session_state['images'])):
            if i%2 ==0:
                st.image(st.session_state['images'][i])
    with colimg2:
        for i in range(1,len(st.session_state['images'])):
            if i%2 ==1:
                st.image(st.session_state['images'][i])
    #idea di mettere un pulsante sotto ogni immagine che permetta di togliere il gioco corrispondente, problema nel for

    
    
with result: #pagina risutlati
    if st.session_state['risultatopronto'] == None:
        st.write("You have not finished inserting your chosen games!") #se non hai submittato i giochi non c'è nulla

    elif st.session_state['risultatopronto'] == False: #pulsante per far partire il processo del back-end
        st.write("Press here for results (It might take a bit to process)")
        if st.button('See results'):
            st.session_state['risultatopronto'] = True
            st.markdown("![Alt Text](https://media.tenor.com/wpSo-8CrXqUAAAAj/loading-loading-forever.gif)") #gif per il loading
            st.session_state['risultati']= ml.game_suggestions(st.session_state['id'],10)


    if st.session_state['risultatopronto'] == True:
        st_autorefresh(interval=2000, limit=2, key="refreshpergif") #refresha la pagina in modo tale che il loading sparisca
        st.write('Results, ordered')
        st.session_state['risultatiappid']=st.session_state['risultati'].index
        
        for giochi in st.session_state['risultatiappid']: #converte gli appid dei giochi in immagini da mostrare all'utente
            current=dataset.loc[dataset['appid']==giochi]
            resultimage = current['header_image'].iloc[-1]
            st.session_state['risultatiimg'].append(resultimage)
         
        for i in range(len(st.session_state['risultatiappid'])): #mostra i risultati in ordine da 1 a 10
            st.write(i+1,':')
            st.image(st.session_state['risultatiimg'][i])
            steamlink='https://store.steampowered.com/app/' + str(st.session_state['risultatiappid'][i])
            st.markdown(f'''
                            <a href={steamlink}><button style="background-color:GreenYellow;">Stackoverflow</button></a>''',unsafe_allow_html=True)
