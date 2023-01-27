# SteamGamePicker
A game recommendation web app

Project for the Software Engineering course at the University of Trieste.
The project consists of a web app made with python utilizing the streamlit library. 
The dataset we utilized can be found at https://www.kaggle.com/datasets/nikdavis/steam-store-games
We utilized 3 of the CSV that were provided in the link, which you can find in the dataset folder.
The CSVs were merged utilizing dataset.py, which resulted in datasetpulito.csv which was what we used in the app.

The app.py is the streamlit/front-end part of the app, while MLpart.py is the back-end which calculates the game recommendations utilizing a KNN-like method. 
