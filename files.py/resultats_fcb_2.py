from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from datetime import datetime

    
def crear_df():
    df=pd.DataFrame(columns=['Equip Local','Equip Visitant','Resultat','Competició',
                                   'Jornada','Data'])
    return df
    
def create_soup(url):
    
    fcb = requests.get(url)
    soup = BeautifulSoup(fcb.content, 'html.parser')
    
    return soup
    
def parse (soup):
    
    partits=soup.find_all(class_="grid-list__items")
    local=soup.find_all(class_="scoreboard__team local__team")
    visitant=soup.find_all(class_="scoreboard__team visitor__team")
    return partits,local,visitant

def valors(partits,local, visitant):
    
    try:
        competicio=[e.get_text().strip() for e in partits[0].select('.match__main__competition')]
        nom_jornada=[e.get_text().strip() for e in partits[0].select('.match__main__phase')]
        data=[e.get_text().strip() for e in partits[0].select('.match__main__date__dmy')]
        equip_local=[e.get_text().strip() for e in local]
        equip_visitant=[e.get_text().strip() for e in visitant]
        resultat=[re.sub(r'\s+','',e.get_text()) for e in partits[0].select('.scoreboard__score__result')]
    
    except IndexError:
        compteticio=['']
        nom_jornada=['']
        data=['']
        equip_local=['']
        equip_visitant['']
        resultat=['']
    
    return competicio,nom_jornada,data,equip_local,equip_visitant,resultat

def crea_df(competicio,nom_jornada,data,equip_local,equip_visitant,resultat):
    
    resultats_mes=pd.DataFrame({'Equip Local':equip_local,'Equip Visitant':equip_visitant,'Resultat':resultat,
                            'Competició':competicio,'Jornada':nom_jornada,'Data':data})
    resultats_mes=resultats_mes.iloc[1:]
    resultats_mes=resultats_mes.sort_values(by='Data').reset_index(drop=True)
    resultats_mes['Data']=pd.to_datetime(resultats_mes['Data'], format='%d/%m/%Y')
    #resultats_mes=resultats_mes.sort_values()
    return resultats_mes

def amplia_df(df0,df1):
     
    df0=pd.concat([df0,df1],ignore_index=True)
    df0=df0.sort_values(by='Data')
    return df0

def expandeix_resultats(df):
    a=df.Resultat.str.split('-',expand=True)
    df['Gols Local']=a[0]
    df['Gols Visitant']=a[1]
    
def resultat_fcb(resultats_fcb):
        # Cas empat
    resultats_fcb.loc[resultats_fcb['Gols Local'] == resultats_fcb['Gols Visitant'], 
                      'Resultat per FCB'] = 'Empata'
    
    # Cas Barça guanya a casa
    resultats_fcb.loc[(resultats_fcb['Gols Local'] > resultats_fcb['Gols Visitant']) 
                        & (resultats_fcb['Equip Local']=='FC Barcelona'), 
                        'Resultat per FCB'] = 'Guanya'
    
    # Cas Barça perd a casa
    resultats_fcb.loc[(resultats_fcb['Gols Local'] < resultats_fcb['Gols Visitant']) 
                        & (resultats_fcb['Equip Local']=='FC Barcelona'), 
                        'Resultat per FCB'] = 'Perd'
    
    # Cas Barça guanya a domicili
    resultats_fcb.loc[(resultats_fcb['Gols Local'] < resultats_fcb['Gols Visitant']) 
                        & (resultats_fcb['Equip Local']!='FC Barcelona'), 
                        'Resultat per FCB'] = 'Guanya'
    
    # Cas Barça perd a domicili
    resultats_fcb.loc[(resultats_fcb['Gols Local'] > resultats_fcb['Gols Visitant']) 
                        & (resultats_fcb['Equip Local']!='FC Barcelona'), 
                        'Resultat per FCB'] = 'Perd'

def converteix_csv(df):
    df.to_csv('resultats_fcb.csv',encoding='utf-8-sig')
    
