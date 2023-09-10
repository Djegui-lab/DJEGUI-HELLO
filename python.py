import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
st.set_page_config(page_title='djégui', layout='wide')
# Numéro WhatsApp (remplacez par votre numéro)
whatsapp_number = "+212605275874"  # Utilisez votre propre numéro WhatsApp

# Créez une URL WhatsApp avec le numéro pré-rempli
whatsapp_url = f"https://wa.me/{whatsapp_number}"

# Titre de l'application
st.title("Application d'Assurance Auto")

# Bouton pour permettre à l'utilisateur d'appeler via WhatsApp
if st.button("Appeler via WhatsApp"):
    st.write(f"Appel en cours via WhatsApp vers le numéro {whatsapp_number}...")
    st.markdown(f"[Cliquez ici pour appeler via WhatsApp]({whatsapp_url})")
# Saisie du nom de l'utilisateur
user_name = st.text_input("Entrez votre nom et prénom")
# Saisie des centres d'intérêt
interests = st.text_area("quel est votre centre d'intérêt ?")
if st.button("Salutation"):
    # Affichage du message de salutation
    if user_name:
       interests_list = interests.split("\n")
       for interest in interests_list:
           st.write(f"Bonjour {user_name} ! merci pour votre analyse. ")
           st.write("je suis un model qui a été fabriqué par Mr.DJEGUI-WAGUÉ.")
           st.write("Votre centre d'intérê est :")
           st.write("- ", interest)
           st.write("")
           st.write("vous êtes la bienvenu(e)",user_name,"!", "vous pouvez continuer à analyser votre base de données dès maintenant ! ")
           st.write("vous souhaitez nous contacter ?")
           st.markdown(f"[Cliquez ici pour appeler via WhatsApp]({whatsapp_url})")

    else:
        st.write("Veuillez entrer votre nom.")
st.write("AUTEUR : Mr.DJEGUI-WAGUÉ")
st.title('VISUALISATION')
st.subheader("merci pour votre analyse")

uploaded_file = st.file_uploader('Choisir un fichier XLSX ', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.title('votre tableau a été telecharger avec succes :')
    statist=df["Age_du_conducteur"]
    st.dataframe(df)
    st.title('ANALYSE DESCRIPTIVE :')
    st.write(df.describe())
    st.write(f" {user_name}  VOUS ETES FORMIDABLE!  ")

    st.title('diagramme à bandes pour age :')
    st.bar_chart(statist)


    groupby_column = st.selectbox(
        "Qu'aimeriez-vous analyser ?",
        ('Nombre_de_sinistres', 'Age_du_conducteur', 'Puissance_fiscale', 'Annees_assurance','Date_de_permis','annee_circulation'),
    )
    # -- GROUP DATAFRAME
    output_columns = ['Annees_assurance', 'Age_du_conducteur']
    df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].mean()
    st.dataframe(df_grouped)
    # -- PLOT DATAFRAME
    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y='Age_du_conducteur',
        color='Annees_assurance',
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>age du conducteur & année assurance by {groupby_column}</b>'
    )
    st.plotly_chart(fig)
st.write("")

st.write("")


st.write("Rebonjour encore",user_name,"!","","permettez moi de vous presentez une base de données :")

# Connexion à la base de données SQLite distante
conn = sqlite3.connect('nex_data_assurance.db')
curseur=conn.cursor()

# Charger les données dans un DataFrame
df = pd.read_sql_query('SELECT * FROM nex_data_assurance', conn)

# Afficher les données dans l'interface utilisateur
st.write("base de données pour ",user_name,".")
st.title("votre base de données a l'etat brute:")
st.dataframe(df.head())
# matrice de correlation
correlation=df[["Age_du_conducteur","Nombre_de_sinistres","Annees_assurance","Date_de_permis"]].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation,annot=True, cmap='coolwarm',linewidths=0.1)
st.title("Matrice de corellation :")
st.subheader("age__Nombre_de_sinistres__Annees_assurance__Date_de_permis")
st.pyplot(plt.gcf())

st.title(" statistique descriptive de votre base de données :")
st.dataframe(df.describe().style.background_gradient(cmap="Reds"))



df_describe=df.describe()
if st.sidebar.checkbox(" AFFICHER LES DIAGRAMMES ET GRAPHIQUES ", False):
   st.subheader( "analyse diagramme a bandes pour Age_conducteur :")
   st.bar_chart(df["Age_du_conducteur"])
   st.subheader( "analyse graphique en ligne (puissance_fiscale) :")
   st.line_chart(df["Puissance_fiscale"])

st.write("merci pour votre visite", user_name,"!")


ok=df[df["Age_du_conducteur"]<=35.57] [["Annees_assurance","Puissance_fiscale"]].std()
st.dataframe(ok)
conn.close()



# Créez un formulaire pour collecter les informations
st.title("Votre demande de devis AUTO")

conducteur = st.number_input("Nom du conducteur")
annee_circulation = st.number_input("Année de circulation")
nombre_de_sinistres = st.number_input("Nombre de sinistres")
puissance_fiscale = st.number_input("Puissance fiscale")
annee_assurance = st.number_input("Année d'assurance")
age_du_conducteur = st.number_input("Âge du conducteur")
date_de_permis = st.number_input("Date de permis de conduire")
risque = st.number_input("Risque")

# Ajoutez un bouton pour soumettre les informations
if st.button("Obtenir un devis"):
    # Connectez-vous à la base de données SQLite
    conn = sqlite3.connect("nex_data_assurance.db")
    cursor = conn.cursor()

    # Assurez-vous que les données sont présentes
    if (annee_assurance and conducteur and age_du_conducteur and date_de_permis and
            risque and nombre_de_sinistres and annee_circulation and puissance_fiscale):
        # Insérez les données dans la base de données
        cursor.execute("""
            INSERT INTO nex_data_assurance (Conducteur,annee_circulation,Nombre_de_sinistres,Puissance_fiscale,Annees_assurance, Age_du_conducteur, Date_de_permis, risque)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (conducteur,annee_circulation, nombre_de_sinistres,puissance_fiscale,annee_assurance,age_du_conducteur, date_de_permis, risque))

        # Validez l'insertion des données
        conn.commit()
        st.success("votre demande de devis a bien été prise en compte !")

        # Fermez la connexion à la base de données
        conn.close()
    else:
        st.warning("Veuillez remplir tous les champs.")


st.dataframe(df)


