from resultats_fcb_2 import *

mes=[i+1 for i in range(12)]
temporada={602:'2011-2012',603:'2012-2013',604:'2013-2014',605:'2014-2015',
           606:'2015-2016',607:'2016-2017',1101:'2017-2018', 3201:'2018-2019'}

x=temporada.items()

resultats_fcb=crear_df()

for key,temporada in x:
    print (temporada)
    for e in mes:
        url='''https://www.fcbarcelona.cat/futbol/primer-equip/resultats?endpoint=https%3A%2F%2Fwww.fcbarcelona.cat%
2Ffutbol%2Fprimer-equip%2Fresultats%3Fp_p_id%3Dfcb_calendar_WAR_fcb_components_INSTANCE_CfNJZ2wSsm3j%26p_p_lifecycle%
3D2%26p_p_state%3Dnormal%26p_p_mode%3Dview%26p_p_resource_id%3Dload-more-games%26p_p_cacheability%3DcacheLevelPage%
26p_p_col_id%3Dcolumn-6%26p_p_col_count%3D2%26competitionId%3D0%26month%3D0%26temporada%3D1202%
23p_fcb_calendar_WAR_fcb_components_INSTANCE_CfNJZ2wSsm3j&results=0&filter-competition=0&filter-month=0&
filter-season=1202&competitionId=0&month={}&temporada={}'''.format(e,key)
        soup=create_soup(url)
        partits,local,visitant=parse(soup)
        competicio,nom_jornada,data,equip_local,equip_visitant,resultat=valors(partits,local,visitant)
        df=crea_df(competicio,nom_jornada,data,equip_local,equip_visitant,resultat)
        resultats_fcb=amplia_df(resultats_fcb,df)
expandeix_resultats(resultats_fcb)
 



resultat_fcb(resultats_fcb)
converteix_csv(resultats_fcb)



