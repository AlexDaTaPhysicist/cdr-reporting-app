# importing all the required modules
import PyPDF2 #  Reading PDFs

import re   # Regular expressions to define sentences
import matplotlib.pyplot as plt # For plotting the reports
import pandas as pd
import streamlit as st

import warnings
warnings.filterwarnings("ignore")

import pickle

Values = {'CDR': 5, 'Corporate Digital Responsibility': 5, 'Digitale Verantwortung': 5,
          'Verantwortliche Digitalisierung': 5, 'Verantwortungsvolle Digital': 5,
          'Nachhaltige Digitalisierung': 5, 'Digitale Ethik': 5, 'Digitalethik': 5,
          'Ethik der Technologie': 5, 'Digitale Verantwortlichkeit': 5,
          'Verantwortungsvolle Algorithmen': 5, 'Responsible AI': 5, 'Ethical AI': 5, 'KI': 4,
          'Künstliche Intelligenz': 4, 'AI': 4, 'Artificial Intelligence': 4, 'KI Ethik': 4,
          'Verantwortliche KI': 4, 'Verantwortliche Innovation': 4, 'Cyber-Ethik': 4,
          'Digitales Vertrauen': 4, 'Digitale Inklusion': 4, 'Digitale Teilhabe': 4,
          'Model Risk Management': 4, 'Intelligenz': 3, 'Data Privacy': 3,
          'Digitale Nachhaltigkeit': 3, 'nachhaltige Digitalisierung': 3,
          'Twin Transformation': 3, 'Chatbot': 3, 'digital waste': 3, 'Zugangshürden': 3,
          'Teilhabe': 3, 'Selbstbestimmung': 3, 'Blockchain': 3, 'Cybersecurity': 2,
          'Digitale Transformation': 2, 'Digitale Governance': 2, 'Digitale Lösungen': 2,
          'Datenschutzschulung': 2, 'App': 2, 'Digitales Geschäftsmodell': 2, 'Datenschutz': 1,
          'Daten': 1, 'Informationssicherheit': 1, 'papierlos': 1, 'Datenmanagement': 1,
          'Automatisierung': 1, 'Cybersicherheit': 1, 'Plattformlösung': 1, 'Plattform': 1,
          'Model': 1, 'Modell': 1}

def restore_values():
    
    f = open("Values.pkl","wb")

    pickle.dump(Values,f)

    f.close()

def update_values():
    f = open("Values.pkl","wb")

    f.close()

def generate_page_overview(df: pd.core.frame.DataFrame,reader:PyPDF2._reader.PdfReader):
    fig, ax = plt.subplots(figsize=[5, 3])
    df.loc[:, ['Score', 'CDR Sentences']].plot(kind='bar', rot=0, ax=ax)
    ax.set_xticks(ticks=[len(reader.pages) / 4, len(reader.pages) / 2, len(reader.pages) * 3 / 4, len(reader.pages)])
    ax.set_title('CDR Relevance and Number of CDR Sentences per page')
    ax.set_xlabel('Page')
    ax.set_ylabel('Occurence/Score')
    return fig
def generate_CDR_Relevancy(df: pd.core.frame.DataFrame):
    fig, ax = plt.subplots(ncols=2)
    df.loc[:, ['Score']].sum().plot(kind='bar', ax=ax[0])
    ax[0].set_xticks(ticks=[])
    ax[0].set_ylabel('CDR Relevancy')
    
    df.loc[:, ['Sentences']].sum()[0]
    (df.loc[:, ['CDR Sentences']].sum() / df.loc[:, ['Sentences']].sum()[0]).plot(kind='bar', ax=ax[1])
    ax[1].set_xticks(ticks=[])
    ax[1].set_ylabel('CDR Communication')
    plt.tight_layout()
    return fig


def create_scoring(reader:PyPDF2._reader.PdfReader):

    df = pd.DataFrame(columns = ['Page', 'Score','CDR Sentences','Sentences'])


    # print the number of pages in pdf file
    #print(len(reader.pages))

    # print the text of the first page
    for i in range(len(reader.pages)):
        page = reader.pages[i].extract_text()
        page_split = re.split(r'[.!?]+', page)
        #print(len(page_split))
        sentences = len(page_split)
        score = 0
        CDR_sent = 0
        for element in page_split:
            for key in Values.keys():
                if key in element:
                    score += Values[key]
                    if Values[key]>3:
                        CDR_sent += 1
        df.loc[i,:] = [i, score, CDR_sent, sentences]
    return df

def create_scoring_with_extra_terms(reader:PyPDF2._reader.PdfReader,Values:pd.core.frame.DataFrame):

    df = pd.DataFrame(columns = ['Page', 'Score','CDR Sentences','Sentences'])
    Values = pd.Series(Values.values.T[1], index=Values.values.T[0])


    # print the number of pages in pdf file
    #print(len(reader.pages))

    # print the text of the first page
    for i in range(len(reader.pages)):
        page = reader.pages[i].extract_text()
        page_split = re.split(r'[.!?]+', page)
        #print(len(page_split))
        sentences = len(page_split)
        score = 0
        CDR_sent = 0
        for element in page_split:
            for key in Values.index:
                if key in element:
                    score += Values[key]
                    if Values[key]>3:
                        CDR_sent += 1
        df.loc[i,:] = [i, score, CDR_sent, sentences]
    return df


def main():
    st.title("CDR Report App")
    
    menu = ['Default CDR Report','CDR Report with additional Terms']
    
    choice = st.sidebar.selectbox('Menu',menu)
    
    if choice == 'Default CDR Report':
        st.subheader('Default CDR Report')
        pdf_file = st.file_uploader("Upload PDF", type='pdf')
        if st.button("Process"):
            if pdf_file is not None:
                reader = PyPDF2.PdfReader(pdf_file)
                df = create_scoring(reader)
                fig = generate_page_overview(df,reader)
                st.pyplot(fig)
                fig1 = generate_CDR_Relevancy(df)
                st.pyplot(fig1)
                
            
    elif choice == 'CDR Report with additional Terms':
        st.subheader('CDR Report with additional Terms')
        pdf_file = st.file_uploader("Upload PDF", type='pdf')
        values = st.file_uploader("Upload Terms and Scoring", type='csv')
        values = pd.read_csv(values)
        values = values[values.columns]
        if st.button("Process"):
            if (pdf_file is not None) and (values is not None):
                reader = PyPDF2.PdfReader(pdf_file)
                df = create_scoring_with_extra_terms(reader,values)
                fig = generate_page_overview(df,reader)
                st.pyplot(fig)
                fig1 = generate_CDR_Relevancy(df)
                st.pyplot(fig1)
    
        


if __name__ == '__main__':
    main()
