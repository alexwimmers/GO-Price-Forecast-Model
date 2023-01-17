import pandas as pd
# numpy as np
#from pandas import Series, DataFrame
from datetime import datetime


# =============================================================================
#  Modell zur Bestimmung von Zahlungsbereitschaft, Nachfrage und Angebot
# =============================================================================
def ausführen():
    
    hh_wtp = wtp_Matching_HH()
    print('Households mateched')
    ind_wtp = wtp_Matching_IND()
    print('Ind mateched')
    ind_wtp_max = max_wtp_Calculation_IND(ind_wtp)
    print('Ind maxed')
    wtp_compl = wtp_combination(hh_wtp, ind_wtp_max)
    print('WTP combined')
    wtp_compl_der = derated_wtp_calculation(wtp_compl)
    print('wtp derated')
    wtp_sorting(wtp_compl_der)
    print('wtp sorted')
    hh_dem = assume_household_demand()
    print('hh demand')
    ind_dem = assume_industry_demand()
    print('ind demand')
    combine_demand(hh_dem, ind_dem)
    print('demand combined')
    goo_issuance()
    print('goos issued')
    
    
    
#Funktionen

# =============================================================================
#  Ermittlung der Zahlungsbereitschaften der Industrie (in Prozent) in Abhängigkeit der Zahlungsfähigkeit und der Konsumentennähe
# =============================================================================

    
def wtp_Matching_IND():
    abt_table = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v03_aw.xlsx', sheet_name = 'ZF_Ind')
    cons_aware = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v03_aw.xlsx', sheet_name = 'Env_Ind')
    wtp_val_list = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v03_aw.xlsx', sheet_name = 'ZB_Ind')
    wtp_list = abt_table[['Land','Sektor','Größe']].copy()
    atp_val_list = abt_table.merge(cons_aware, on=["Sektor", "Kode"], how='left')
    for year in range(2010,2018):
        new_Column = pd.DataFrame(columns=[year])
        for i in range(len(atp_val_list)):            
            for wtp_atp in range(2,7):
                for wtp_cons in range(1,6):
                    if wtp_val_list.iat[wtp_cons, 0] >= atp_val_list.loc[i,year] and wtp_val_list.columns[wtp_atp] >= atp_val_list.loc[i, "Umweltbewusstsein"]:                                                     
                        new_Column.at[i,year] = wtp_val_list.iat[wtp_cons,wtp_atp]
                        #print(wtp_val_list.iat[wtp_cons,wtp_atp])
                       
                        break
                    else:
                        continue
                    break
        print(new_Column)
        wtp_list[year]=new_Column[year]
    '''
    for abt_pos in range(len(abt_table)):        
        for cons_pos in range(len(cons_aware)):    
            
            abt_sek = abt_table.iat[abt_pos,1]
            cons_sek = cons_aware.iat[cons_pos,0]
            
            if cons_sek == abt_sek:
                
                for i in range(4,12):
                    abt_year = abt_table.columns[i]
                    abt_cou = abt_table.iat[abt_pos,0]
                    abt_val = abt_table.iat[abt_pos,i]
                    abt_siz = abt_table.iat[abt_pos,3]
                    cons_val = cons_aware.iat[cons_pos,2]
                    
                   # print(abt_year)
                    
                    for wtp_abt in range(2, 7):  
                        
                        for wtp_cons in range(1, 6):  
                            #print(wtp_val_list.iat[wtp_cons, 0], wtp_val_list.columns[wtp_abt], abt_year)
                           
                             if wtp_val_list.iat[wtp_cons, 0] >= cons_val and wtp_val_list.columns[wtp_abt] >= abt_val:                                                     
                                wtp_val = wtp_val_list.iat[wtp_cons, wtp_abt]                                                 
                                wtp_Row = pd.Series(data={'Land':abt_cou,'Größe':abt_siz,'Sektor': abt_sek, 'Jahr':abt_year, 'WTP':wtp_val})                                
                                wtp_list = wtp_list.append(wtp_Row, ignore_index=True)
                                break
                        else:                                
                             continue
                        break
    '''                    
    wtp_list.to_csv('Data\WTP_Ind.csv', index = None, sep=";", mode="a") 
    return wtp_list 

# =============================================================================
#  Ermittlung der Zahlungsbereitschaften der Haushalte (in €/MWh) für die verschiedenen "Arten" der Haushalte hinsichtlich Präferenzen
# =============================================================================    

def wtp_Matching_HH():
    wtp_table = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v03_aw.xlsx', sheet_name= 'ZB_HH')
    el_cost = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v03_aw.xlsx', sheet_name= 'SP_HH')
    wtp_list = pd.DataFrame(columns=['Land', 'Sektor','Größe', 2010,2011,2012,2013,2014,2015,2016,2017,2018,2019])
    
    for j in range(len(el_cost)):
        for i in range(len(wtp_table)):            
            new_Row = pd.DataFrame(data={'Land':el_cost.loc[j,'Land'],'Sektor':el_cost.loc[j,'HHCOMP'], 'Größe':i}, index=[0])            
            for year in range(2010,2019):
                wtp_val = el_cost.loc[j,year]*wtp_table.iat[i,1]*1000
                new_Row[year] = wtp_val
            wtp_list = wtp_list.append(new_Row, ignore_index = True)
    wtp_list.to_csv('Data\WTP_HH.csv', index= None, sep=";", mode="a")            
    return wtp_list    

# =============================================================================
#  Ermittlung der Zahlungsbereitschaft in €/MWh durch Multiplikation der oben berechneten Werte mit den durchn. Strompreisen (Hier: exkl. VAT) = Preise
# =============================================================================           

def max_wtp_Calculation_IND(wtp_list):
    
    el_cost = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v03_aw.xlsx', sheet_name = 'SP_Ind')
   # el_cost = el_cost.drop(columns=['Energiesektor','Kode'])
    max_wtp_list = el_cost.merge(wtp_list, on=['Land','Sektor','Größe'])
    
    for year in range(2010, 2018):
         max_wtp_list[year]=max_wtp_list[str(year)+"_x"]*max_wtp_list[str(year)+"_y"]*1000
         max_wtp_list.drop(str(year)+"_x",axis=1,inplace=True)
         max_wtp_list.drop(str(year)+"_y",axis=1,inplace=True)
   
    max_wtp_list.to_csv('Data\maxWTP_Ind.csv', index = None, sep=";", mode="a")    
    
    return max_wtp_list            

# =============================================================================
#  Zusammenführen der Listen für Haushalte und Industrie
# =============================================================================

def wtp_combination(wtp_hh, wtp_ind):
    #wtp_hh = pd.read_csv('Data/WTP_HH.csv', delimiter=';')
    #wtp_ind = pd.read_csv('Data/maxWTP_Ind.csv', delimiter=';')
    
    wtp_compl = pd.concat([wtp_hh,wtp_ind])
    wtp_compl.to_csv('Data\WTP_compl.csv', index = None, sep = ';', mode='a')
    return wtp_compl

                  
# =============================================================================
#  Ermittlung der Zahlungsbereitschaften für einzelne Technologie-Herkunft-obminationen von GoOs (Oben nur Maxe Berechnet) [Herkunft noch nicht einbezogen]
# =============================================================================

def derated_wtp_calculation(wtp_list):
    #print('line79')
    #wtp_list = pd.read_csv('Data/WTP_compl.csv', delimiter=';')
   # wtp
    derated_wtp_list = pd.DataFrame(columns=['Land', 'Größe', 'Sektor', 'Technologie', 'Derated WTP'])
    derating_factors = pd.read_excel('Data/20200921_GoO Information_v02_aw.xlsx', sheet_name = 'Derating_Factors')
    derated_wtp_list_compl = derating_factors.merge(wtp_list, on='Land')
    #print(derated_wtp_list_compl.head(10))
    for t in range(2,8):
        tec = derated_wtp_list_compl.columns[t]
        #print(tec)        
        derated_wtp_list_tec = derated_wtp_list_compl[['Land','Größe','Sektor','Herkunft',tec,2010,2011,2012,2013,2014,2015,2016,2017]]
        #derated_wtp_list_tec.to_csv('Data\deratedWTP_tec.txt', index = None, sep=";", mode="a")
        for year in range(2010,2018):      
            derated_wtp_list_tec[str(year)] = derated_wtp_list_tec[str(year)]*derated_wtp_list_tec[tec]                                              
        derated_wtp_list_tec.rename(columns={tec : 'Technologie'}, inplace=True)
        derated_wtp_list_tec['avg'] = derated_wtp_list_tec.mean(axis=1)        
        derated_wtp_list_tec['Technologie']=tec
        derated_wtp_list=derated_wtp_list.append(derated_wtp_list_tec, ignore_index=True)
    derated_wtp_list.drop_duplicates(subset=['Land','Größe','Sektor','Herkunft','Technologie','Derated WTP'], keep = 'first', inplace = True)
    #derated_wtp_list_tec.drop(['Derated WTP'], axis=1, inplace=True)
    for year in range(2010,2018):      
            derated_wtp_list.drop([str(year)], axis=1, inplace=True)    
    derated_wtp_list.to_csv('Data\deratedWTP_2.csv', index = None, sep=";", mode="a")
    return derated_wtp_list

# =============================================================================
#  GoO Herausgabe i.A. von FU-Daten und vergangenen GO-Herausgabe-Quoten = Angebot
# =============================================================================
def goo_issuance():
    fu_data = pd.read_excel('Data/20200921_GoO Information_v02_aw.xlsx', sheet_name = 'EE-GEN')
    issue_rates = pd.read_excel('Data/20200921_GoO Information_v02_aw.xlsx', sheet_name = 'Issue Rates') 
    merged_data = fu_data.merge(issue_rates, how='left', on=['Land', 'Technologie'])
    merged_data.drop(columns=['Country'])
    merged_data.to_csv('Data\gootest.csv', index = None, sep=";", mode="a")
    issued_goo = merged_data[['Land', 'Technologie']].copy()
    #merged_data_sel =  merged_data.iloc[:,0:21]
    
    for year in range(2020,2040):
       issued_goo[year] = merged_data[str(year)+"_y"]*merged_data[str(year)+"_x"]*1000 #Gwh zu MWh
    
    issued_goo.to_csv('Data/issuedGoos.csv', index = None, sep=';', mode='a')
    
    return issued_goo          
      

     

#Vergangene Daten werden erstmal nicht berücksichtigt. Das heißt interessant wird es ab 2025
'''def goo_availability(goo_list):
    available_goos = pd.DataFrame(columns=['Goo','Anzahl'])
    country_tec_combi = pd.read_Excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Land_Tec_Kombinationen')
    issuance_2019 = pd.read_Excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Past Cancellation Data')
    cancellation_2019 = pd.read_Excel('Data/20200921_GoO Information_v01_aw.xlsx', sheet_name = 'Past Issuance Data')
    for goo_range in range(len(goo_list)):
        for cou_tec_num in range(len(country_tec_combi)):
            combi_cou = country_tec_combi.iat[cou_tec_num,0]
            combi_tec = country_tec_combi.iat[cou_tec_num, 1]
            for d in range(2020,2025):
                for m in range(1,13):
                    date = datetime(d, m, 1)
                    location_in_goo_list = findGoo(goo_list, combi_cou, combi_tec, date)
'''                        
# =============================================================================
#  Sortierung der Zahlungsbereitschaften (ggf. nicht notwendig?)
# =============================================================================
def wtp_sorting(derated_wtp):
    #derated_wtp['avg'] = derated_wtp.mean(axis=1)
    sorted_wtp = derated_wtp.sort_values('avg', ascending=False)
    #for year in range(2008,2018):
       # sorted_wtp.drop([year],axis=1, inplace=True)
    sorted_wtp.to_csv('Data\sorted.csv', index = None, sep=";", mode="a")
    return sorted_wtp
    #Durchschnittliche WTP eines Unternehmens eines Sektors eines Landes für eine bestimmte Technologie *pro Jahr* -> Durchschnitt aus 2008-2017


# =============================================================================
#  Annahme des Industriebedarfs
# =============================================================================
def assume_industry_demand():
    ind_dem = pd.read_excel('Data/20200917_Stromverbräuche_v03_aw.xlsx', sheet_name = 'Dem_Ind') #Nachfrage eines Durchschnittsunternehmens [MWh]
    ind_no = pd.read_excel('Data/20200917_Stromverbräuche_v03_aw.xlsx', sheet_name = 'NO_Ind') #Anzahl der Unternehmen
    ind_dev = pd.read_excel('Data/20200917_Stromverbräuche_v03_aw.xlsx', sheet_name = 'Dev_Ind') #Prognostizierte Entwicklung des Bedarfs i.A. des Vorjahresverbrauchs
    ind_dem_nozero = ind_dem[~(ind_dem==0).any(axis=1)]
    #ind_dem_nozero.to_csv('Data\inddem_1pre.txt', index = None, sep=";", mode="a") 
    merged = pd.merge(ind_dem_nozero,ind_dev, how="left", on=['Sektor'])
  #  ind_dem_assum = pd.DataFrame(columns=["Land","Sektor", "Größe"])
    #merged.to_csv('Data\inddem_pre.txt', index = None, sep=";", mode="a")    
    for year in range(2020, 2040):
        if year == 2020:
            new_Column = pd.DataFrame(data={year: merged[2017]*merged[2020]*1000}) #GWh zu MWh          
            merged[2020] = new_Column[2020]
        else:
            #print(merged[year].head(5))
            #print(merged[year-1].head(5))
            new_Column = pd.DataFrame(data={year: merged[year-1]*merged[year]})        
            merged[year] = new_Column[year]    
    merged.drop(columns=['Kode',2017],axis=1, inplace=True)
    complete_sector = pd.merge(merged, ind_no, how='left', on=['Land', 'Sektor', 'Größe'])    
    #print(complete_sector.head(5))
    #complete_sector.to_excel('Data\inddem_complete.xls', sheet_name='industry demand')  
    for year in range(2020, 2040):
        complete_sector[year] = complete_sector[year]*complete_sector[2017]       
    #merged.drop(['Kode', 'Energiesektor', 2017], axis=1, inplace=True)
    merged.to_csv('Data\inddem_einzeln.csv', index = None, sep=";", mode="a")
    complete_sector.to_excel('Data\inddem_complete.xls', sheet_name='industry demand')                   
    return merged
    #Industry demand per Country & Sektor für 2020-2050        
    
# =============================================================================
#  Annahme des Haushaltsbedarfs
# =============================================================================
def assume_household_demand():
    hh_dem = pd.read_excel('Data/20200917_Stromverbräuche_v03_aw.xlsx', sheet_name = 'Dem_HH') #Nachfrage eines Durchschnittshaushalts [kWh] -> Noch keine Aufteilung nach Präferenzen
    hh_no = pd.read_excel('Data/20200917_Stromverbräuche_v03_aw.xlsx', sheet_name = 'NO_HH') #Anzahl der Haushalte
    hh_dev = pd.read_excel('Data/20200917_Stromverbräuche_v03_aw.xlsx', sheet_name = 'Dev_HH') #Voraussichtliche Entwicklung der Haushaltsverbräuche
    hh_dem_nozero = hh_dem[~(hh_dem==0).any(axis=1)]
    #ind_dem_nozero.to_csv('Data\inddem_1pre.txt', index = None, sep=";", mode="a") 
    merged = pd.merge(hh_dem_nozero,hh_dev, how="left", on=['HHCOMP'])
  #  ind_dem_assum = pd.DataFrame(columns=["Land","Sektor", "Größe"])
    #merged.to_csv('Data\inddem_pre.txt', index = None, sep=";", mode="a")    
    for year in range(2020, 2040):
        if year == 2020:
            new_Column = pd.DataFrame(data={year: merged[2018]*merged[2020]}) #kWh zu MWh, aber Anzahl der HH in Tsd. -> 1          
            merged[2020] = new_Column[2020]
        else:
            #print(merged[year].head(5))
            #print(merged[year-1].head(5))
            new_Column = pd.DataFrame(data={year: merged[year-1]*merged[year]})        
            merged[year] = new_Column[year]    
    complete_sector = pd.merge(merged, hh_no, how='left', on=['Land', 'HHCOMP'])    
    for year in range(2020, 2040):
        complete_sector[year] = complete_sector[year]*complete_sector[2019]       
    #merged.drop(['Kode', 'Energiesektor', 2017], axis=1, inplace=True)
    hh_dist = pd.read_excel('Data/20200917_Zahlungsbereitschaft_v03_aw.xlsx', sheet_name= 'ZB_HH') #Verteilung der Haushalte auf die verschiedenen Präferenzen
    hh_dem = pd.DataFrame(columns=['Land', 'Sektor','Größe'])
    for j in range(2020,2040):
        new_Column = pd.DataFrame(columns=[j])
        hh_dem[j] = new_Column[j]
    for i in range(len(hh_dist)):
        for j in range(len(complete_sector)):            
            new_Row = pd.DataFrame(data={'Land':complete_sector.loc[j,'Land'],'Sektor':complete_sector.loc[j,'HHCOMP'], 'Größe':i}, index=[0])            
            for year in range(2020,2040):
                hh_val = complete_sector.loc[j,year]*hh_dist.iat[i,0]
                new_Row[year] = hh_val
            hh_dem = hh_dem.append(new_Row, ignore_index = True)
    hh_dem.to_csv('Data\hhdem_per_sector.csv', index = None, sep=";", mode="a")
    complete_sector.to_excel('Data\hhdem_complete.xls', sheet_name='industry demand')                   
    return merged 

# =============================================================================
#  Zusammenführung der Bedarfsinformationen (Nachfrage) und der Zahlungsbereitschaften = Preis
# =============================================================================            
 
def combine_demand(dem_hh, dem_ind):
    demand_compl = dem_hh.append(dem_ind, ignore_index=True)
    demand_compl.to_csv('Data\complete_demand.csv', index = None, sep=";", mode="a")
    return demand_compl


# =============================================================================
#  Zusammenführung der Bedarfsinformationen (Nachfrage) und der Zahlungsbereitschaften = Preis
# =============================================================================
def merge_sorted_wtp_and_demand(sorted_wtp,ind_dem):
    #industry_demand_pc = pd.read_excel('Data/20200917_Stromverbräuche_v01_aw.xlsx', sheet_name = 'Industrie')
    industry_amount = pd.read_excel('Data/20200917_Stromverbräuche_v02_aw.xlsx', sheet_name = 'Anzahl Unternehmen')
    #industry_demand_pc["2017"] = 1000*industry_demand_pc["2017"] #GWh to MWh
    ind_dem_compl= pd.merge(ind_dem, industry_amount, how='left',on=['Land', 'Sektor', 'Größe'])
    
    merged_data=pd.merge(ind_dem_compl,sorted_wtp, how='left',on=['Land', 'Sektor', 'Größe'])
    merged_data.to_csv('Data\merged_wtp_demand.csv', index = None, sep=";", mode="a")                   

    return merged_data

def get_monthly_demand():
    ind_dem = pd.read_excel('Data/inddem_complete.xls', sheet_name='industry demand')
    output = ind_dem[['Land','Sektor','Größe']].copy()
    for year in range(2020,2051):               
        periods = ind_dem[['Land','Sektor','Größe',year]].copy()
        #print(periods)        
        for m in range(0,12):           
            month = datetime(year, m+1, 1).strftime("%d-%m-%y")
            new_Column = pd.DataFrame(data={month: periods[year]/12})
            periods[month] = new_Column
        periods.drop([year],axis=1, inplace=True)
        output = output.merge(periods, how='left',on=['Land','Sektor','Größe'])
    output.to_csv('Data\monthly_demand.csv', index = None, sep=";", mode="a")                
    return output

ausführen()
