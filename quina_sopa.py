# -*- coding: utf-8 -*-
"""QUINA_SOPA_ETS.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UTJ01GFcOjUdufrs0tcJjmBKjkXfxh60
"""

# Abans de tot importo les llibreries i connecto el drive
import streamlit as st
import re
import pandas as pd
import numpy as np
import string
import warnings

# Suppress Streamlit-specific warnings
#st.set_option('deprecation.showfileUploaderEncoding', False)
#st.set_option('deprecation.showPyplotGlobalUse', False)

# Suppress general Python warnings
warnings.filterwarnings("ignore")

#from google.colab import drive
#drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/14_PROJECTES/01_Persones_i_Sentiments/Questionari

# FUNCIONA

# Function to calculate the user's soup
def calculate_soup(respostes):
    sopes = {
        "Escudella": 0, "Puchero": 0, "Gazpacho": 0, "Sopa de ceba": 0, "Sopa de peix": 0,
        "Vichyssoise": 0, "Pho": 0, "Crema de verdures": 0, "Crema de carbassa": 0, "Sopa de miso": 0
    }

    # descripcions de les sopes
    sopes_descripcions = {"Escudella":"Tradició, casa, en la simplicitat està la màgia, per ocasions especials (sembla simple però realment li posa molt esforç a tot. és una persona que fa que les persones que l’envolten tinguin la mateixa importancia que ella i brilla molt en ocasions especials. Treballa per soft català en el sentit purista i pot cansar)",
                    "Puchero": "Sopa de cigrons amb choriço (persona forta, te l’has de treballar, molta personalitat. Tradicional i quan està en un grup sempre es fa notar, te moltes aficions diferents. Pot tenir sortides que no t’esperes. Es una personalitat que no a tothom li agrada però mai t’avorrira) ", 
                    "Gazpacho": "Fresca, intensa, es aquesta gent que no la veus sempre però quan la veus no saps perquè l’has deixat de veure i aleshores t’anadones que es repeteix. Té energia, sola o acompanyada.", 
                    "Sopa de ceba": "És una persona de casa, calida i que valora tan el seu temps que a vegades et fa perdre el teu deixante en l’ultim moment tirat. Es molt del tu a tu, no li molen els espais amb molta gent perquè no destaca i sol portar jersei de coll alt i li encanta el cinema. Dona molt bones abraçades i sempre et diu el que t’ha de dir quan necessites", 
                    "Sopa de peix": "Es una amiga a la que veus molt poc. es aquella amiga que te uns amics que no et cauen bé però a ella te la estimes. Surt de festa a bling bling i abans de quedar et pregunta com aniras vestida. Si calculessis el preu de la roba que porta posada es mes cara que tot el teu armari. Ara bé, no farda del seu estatus i et fa sentir comode tot i les diferencies.Pero no soportes als seus amics.",
                    "Vichyssoise": "persona adaptable, la pots portar on sigui que no has d’estar pendent d’ella. No li costa estar una estona sola. No busca el protagonisme però sempre destaca sense voler. La mires amb admiració i enveja. No es l’amiga que mes t’escolta, no perque no vulgui, es que no té profunditat.",
                    "Pho": "Aventurera però amb els peus a terra. Es aquella persona que quan tu expliques algo t’escolta i et diu el que toca en la quantitat que toca perque t’ha escoltat. Quan ella parla, li agrada sentir les opinions dels altres i aleshores formar la seva. Tot i que viu en un pis compartit té un privilegi que de tant en tant surt a la llum i entens aquest to despreocupat que sempre l’acompanya. ",
                    "Crema de verdures": "Amiga comfort, sempre està allà, et coneix millor que tu a tu mateixa. A ella no la pots enganyar, es aquella persona que quan li presentes a algú et diu “segur?” perquè realment sap que no es per tu perquè es la unica que te el valor de dir-te que no et compris un pantalons blancs ni unes botes de cowboy. Però, alhora, és la mateixa que sempre estarà al teu costat com uns bons texans",
                    "Crema de carbassa": "es aquesta amiga amb la que fa tant de temps que us coneixeu que no saps ja de que us coneixeu. Es una amistat amb la que quedes amb ella a soles. Disfrutes el moment i hi ha vegades que la trobes a faltar però no la pots tenir sempre ni la pots portar amb altre gent. Es aquella amiga que te una feina molt demandant o viu lluny i costa de materialitzar la quedada però quan la veus no entens com ha pogut passar tant de temps sense veureus i et tornes a sentir tant comode com sempre, com a casa.",
                    "Sopa de miso": "és lleugera. és molt facil de tractar sembla simple perque sol estar callada però quan li preguntes directament t’adones que te moltes capes. Els teus amics no l’acaben de captar al principi perque es molt timida però al final tots l’acabeu estimant i et demanen que torni. és una persona molt reservada i assertivament et fa saber que no vol quedar perque necessita temps per ella, i ho acceptes, perquè l’estimes."
        
    }

    preguntes = [
        ("Mar o Muntanya?", [["Gazpacho", "Sopa de peix", "Vichyssoise", "Pho", "Sopa de miso"], ["Escudella", "Puchero", "Sopa de ceba", "Crema de verdures", "Crema de carbassa"]]),
        ("Consell de Cent o Carrer Blai?", [["Escudella", "Sopa de ceba", "Sopa de peix", "Crema de verdures", "Crema de carbassa"], ["Puchero", "Gazpacho", "Vichyssoise", "Pho", "Sopa de miso"]]),
        ("Quan tens un granet de pus a la cara que es veu molt: L’explotes, El deixes o El tapes?", [["Gazpacho", "Sopa de peix"], ["Puchero", "Vichyssoise", "Pho", "Crema de verdures", "Sopa de miso"], ["Escudella", "Sopa de ceba", "Crema de carbassa"]]),
        ("He sortit de festa com torno a casa: Agafo Uber, Camino/Transport Públic, No torno a casa meva?", [["Escudella", "Sopa de peix", "Pho", "Crema de carbassa"], ["Puchero", "Sopa de ceba", "Crema de verdures", "Sopa de miso"], ["Gazpacho", "Vichyssoise"]]),
        ("Dormir o Menjar?", [["Escudella", "Sopa de ceba", "Crema de verdures", "Crema de carbassa", "Sopa de miso"], ["Puchero", "Gazpacho", "Sopa de peix", "Vichyssoise", "Pho"]]),
        ("Estas parlant amb una persona que te un moc al nas i no el coneixes gaire: Li dius o No li dius?", [["Puchero", "Gazpacho", "Sopa de ceba", "Vichyssoise", "Crema de verdures", "Sopa de miso"], ["Escudella", "Sopa de peix", "Pho", "Crema de carbassa"]]),
        ("Monstera o Pothus?", [["Escudella", "Sopa de ceba", "Sopa de peix", "Pho", "Crema de verdures", "Sopa de miso"], ["Puchero", "Gazpacho", "Vichyssoise", "Crema de carbassa"]]),
        ("Rajola hidràulica o Parquet?", [["Escudella", "Gazpacho", "Pho", "Crema de carbassa", "Sopa de miso"], ["Puchero", "Sopa de ceba", "Sopa de peix", "Vichyssoise", "Crema de verdures"]]),
        ("Les plantes es moren perquè: Les regues massa o Massa poc?", [["Escudella", "Sopa de ceba", "Sopa de peix", "Crema de verdures", "Crema de carbassa"], ["Puchero", "Gazpacho", "Vichyssoise", "Pho", "Sopa de miso"]]),
        ("Et conviden a casa d’algú a sopar: Portes algo fet per tu, Portes pica pica comprat, Portes alcohol o Portes els ingredients per cuinar allà?", [["Escudella", "Crema de verdures", "Sopa de miso"], ["Sopa de peix", "Vichyssoise", "Crema de carbassa"], ["Gazpacho", "Pho"], ["Puchero", "Sopa de ceba"]])
    ]

    for i, respostes in enumerate(respostes):
        for sopa in preguntes[i][1][respostes]:
            sopes[sopa] += 1

    sopa_max = max(sopes, key=sopes.get)
    return sopa_max, sopes_descripcions, sopes



####################################################
# Streamlit App UI
st.set_page_config(page_title="Quina sopa ets?", page_icon="🍲", layout="wide", initial_sidebar_state="expanded")


# ------------ Header section: 
with st.container():
  st.title("🍲 Quin tipus de sopa ets?")
  st.subheader("Respon les següents preguntes per descobrir quin tipus de sopa ets!")


# --------- DEFININT PARÀMETRES ---------------
preguntes = [
    "Mar o Muntanya?",
    "Consell de Cent o Carrer Blai?",
    "Quan tens un granet de pus a la cara que es veu molt?",
    "He sortit de festa com torno a casa?",
    "Dormir o Menjar?",
    "Estas parlant amb una persona que te un moc al nas i no el coneixes gaire?",
    "Monstera o Pothus?",
    "Rajola hidràulica o Parquet?",
    "Les plantes es moren perquè?",
    "Et conviden a casa d’algú a sopar?"

]

opcions = [
    [["Mar", "Muntanya"]],
    [["Consell de Cent", "Carrer Blai"]],
    [["L’explotes", "El deixes", "El tapes"]],
    [["Agafo Uber", "Camino/Transport Públic", "No torno a casa meva"]],
    [["Dormir", "Menjar"]],
    [["Li dius", "No li dius"]],
    [["Monstera", "Pothus"]],
    [["Rajola hidràulica", "Parquet"]],
    [["Les regues massa", "Massa poc"]],
    [["Portes algo fet per tu", "Portes pica pica comprat", "Portes alcohol", "Portes els ingredients per cuinar allà"]]
]

# Use local CSS
# per el format de el contact form fem servir un document css que hem guardat a la carpeta style
# el document l'he agafat del github del tutorial

def local_css(file_name):
   with open(file_name) as f:
      st.markdown(f'<style>{f.read()}<style>', unsafe_allow_html=True)

local_css("style/style.css")


# Initialize session state for radio buttons
# sinó tenia error
if 'respostes' not in st.session_state:
    st.session_state['respostes'] = [None] * len(preguntes)

# --------------QUESTIONARI ----------------:
# variable per guardar les respostes
respostes = []

# Faig dues columnes perquè 
with st.container():
    st.write("---") # linia divisoria

    # separo la pàgina en dues columnes
    left_column, right_column = st.columns(2)

    # columna esquerra:
    with left_column:
       # itera per l'índex (i) i cada pregunta

       for i, pregunta in enumerate(preguntes):
          # defineix l'estil del titol de la pregunta (també a style.css)
          st.markdown(f"<p style='margin-bottom: -1px; font-size:16px;'><b>{pregunta}</b></p>", unsafe_allow_html=True)


          # crea una radio button (un botó on només pots escollir una opció)
          # " " - fa que no hi apareixi res escrit sobre les opcions
          # opcions[i][0] proporciona una llista de les op cions per la pregunta corresponent (i)
          # index = None fa que quan obres l'app cap pregunta estigui pre-seleccionada
          # key=f"pregunta_{i}" dona una clau única a cada pregunta perquè streamlit pugui guardar cada resposta independentment
       
          resposta = st.radio(" ", opcions[i][0], index=None, key=f"pregunta_{i}")

          if resposta is not None:
             # quan l'usuari selecciona una resposta, la guarda a la llista de respostes
             respostes.append(opcions[i][0].index(resposta))  

        # Botó per descobrir quina sopa és l'usuari
       if st.button("Descobreix la teva sopa!"):
          
          # totes les respostes han d'estar contestades
          if len(respostes) == len(preguntes):
             
             # fem servir la funció calculate_soup de l'inici per calcular la sopa amb més punts (sopa max)
             # el recompte de totes les sopes (sopes)
             # i la descirpció de cada sopa (sopes_descripcions)
             sopa_max, sopes_descripcions, sopes = calculate_soup(respostes)
            
             st.success(f"🌟 Ets la sopa: **{sopa_max}**! 🎉")
             st.write(f"Com és la/el **{sopa_max}**: {sopes_descripcions[sopa_max]}")

             # creo una Flag perquè el recompte només s'activi quan es premi el botó
             show_recompte = True


          else:
             st.error("🚫 Per favor, respon totes les preguntes abans de descobrir la teva sopa!")

       else: 
          # en el cas de que el botó no s'hagi premut, la flag serà False
          show_recompte = False

    # columna dreta:
    with right_column:
       
       # perquè funcioni sopa, sopes... he de tornar a crida la funció calculate_soup.
         # això és perquè la funció calculate_soup no està definida fora de la condició del botó

       sopa_max, sopes_descripcions, sopes = calculate_soup(respostes)


# -------------- DESCRIPCIONS DE LES SOPES ------------:
       st.subheader("Descripcions de les sopes:")

       for sopa, descripcio in sopes_descripcions.items():
        if st.button(sopa):
           st.write(descripcio)


# -------------- RECOMPTES DE PUNTUACIONS ------------:

       if show_recompte: # si s'activa show_recompte = True (flag)
          st.subheader("Recompte de puntuacions:")

          for sopa, count in sopes.items():
            st.write(f"- {sopa}: {count}")

# ------------ CONTACT SECTION ------------:
with st.container():
   st.write("---")
   st.header("Vols parlar amb nosaltres?")
   st.write("##")

   # form taken from: https://formsubmit.co/
   contact_form = """
   <form action="https://formsubmit.co/berta.llugany@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder = "Nom i Cognoms" required>
     <input type="email" name="email" placeholder = "Email" required>
     <textarea name="message" placeholder = "Missatge" required></textarea>
     <button type="submit">Send</button>
</form>

"""
# perquè el contact form no faci servir tot l'espai faig dues columnes:
left_column, right_column = st.columns(2)
with left_column:
   # incloem la info del contact_fom que hem fet
   st.markdown(contact_form, unsafe_allow_html= True)
with right_column:
   # deixem la columna buida
   st.empty()