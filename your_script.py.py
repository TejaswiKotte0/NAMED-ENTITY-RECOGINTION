# -*- coding: utf-8 -*-
"""Untitled27.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n1bwqOa_og1biRayGM8zuInOlLPG8O9I
"""

import spacy
import stanza
from spacy import displacy
from PyPDF2 import PdfReader
import re
import pandas as pd
import streamlit as st


HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
stanza.download('en', package='mimic', processors={'ner': 'bc5cdr'})
new_nlp = stanza.Pipeline('en', package='mimic', processors={'ner': 'bc5cdr'})
nlp=spacy.load("en_ner_bc5cdr_md")
s_nlp=spacy.load("en_ner_bionlp13cg_md")

def main():
  st.title("NAMED ENTITY RECOGINITION")
  activities = ["Disease and Chemicals", "General Medical Terms", "Search"]
  choice = st.sidebar.selectbox("select activity",activities)

  if choice == "Disease and Chemicals":
    st.subheader("Disease and Chemicals")
    file = st.file_uploader('Choose a file to upload')
    reader = PdfReader("medicalmerged.pdf")
    text =""
    for page in reader.pages:
      text += page.extract_text() + "/n"
    words = re.sub("[A-Za-z""]+[0-9" "]+"," ",text).lower()
    docx = nlp(words)
    Dataframe = [(ent.text,ent.label_)for ent in docx.ents]
    

    
      

    


    uniue_char = []
    for c in Dataframe:
      if not c in uniue_char:
        uniue_char.append(c)
    df = pd.DataFrame(uniue_char,columns = ['Name', 'Disease/Chemical'])
    st.table(df)
    html = displacy.render(docx,style = "ent")
    html = html.replace("/n","/n")
    st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)


  if choice == 'General Medical Terms':
    st.subheader("General Medical Terms")
    file = st.file_uploader('Choose a file to upload')
    reader = PdfReader("medicalmerged.pdf")
    text = ""
    for page in reader.pages:
      text += page.extract_text() + "/n"
    words = re.sub("[^A-Za-z" "]+[0-9" "]+", " ", text).lower()
    docx = s_nlp(words)
    Dataframe = [(ent.text,ent.label_) for ent in docx.ents]
    uniue_char = []
    for c in Dataframe:
      if not c in uniue_char:
        uniue_char.append(c)
    df=pd.DataFrame(uniue_char,columns=['name','medical terms'])
    st.table(df)
    html = displacy.render(docx,style = "ent")
    html = html.replace("\n","\n")
    st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

    @st.cache
    def convert_df_to_csv(df):
      return df.to_csv().encode('utf-8')


  if choice == 'Search':
    st.subheader("Manual Search")
    file = st.file_uploader('Choose a file to upload')
    reader = PdfReader("medicalmerged.pdf")
    text = ""
    for page in reader.pages:
      text += page.extract_text() + "\n"
    text = re.sub("[^A-Za-z" "]+[0-9" "]+", " ", text).lower()
    d=nlp(text)
    Dataframe=[(ent.text,ent.label_) for ent in d.ents]
    uniue_char = []
    for c in Dataframe:
      if not c in uniue_char:
        uniue_char.append(c)

    word = st.text_input("Enter Text Here:")
          
    if word in text:
      lst=new_nlp(word)
      dataframe=[(ent.text,ent.type) for ent in lst.entities]
      uniue_char.extend(dataframe) 
        
        

      

      

      st.success("Success")
    else:
      st.error("Word not Found")

    st.write(uniue_char)

    @st.cache
    def convert_df_to_csv(df):
      return df.to_csv().encode('utf-8')

    df = pd.DataFrame(uniue_char,columns = ['Name', 'Disease/Chemical'])     

    st.download_button(
          label="Download data as CSV",
          data=convert_df_to_csv(df),
          file_name='New_dataa.csv',
          mime='text/csv',)

if __name__ == '__main__':
  main()

!streamlit run streamlit_app.py & npx localtunnel --port 8501

pip install PyPDF2

pip install stanza

pip install streamlit

pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bc5cdr_md-0.5.1.tar.gz

pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bionlp13cg_md-0.5.1.tar.gz

pip install nltk