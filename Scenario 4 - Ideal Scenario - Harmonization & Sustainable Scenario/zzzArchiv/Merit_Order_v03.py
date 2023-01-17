import pandas as pd
import csv
from datetime import datetime


wtps = pd.read_csv('Data\sorted.csv', delimiter=';')
demand = pd.read_csv('Data\monthly_demand.csv', delimiter=';')
supply = pd.read_csv('Data\issuedGoos.csv', delimiter=';')
country_list = pd.read_excel('Data/Countries.xlsx',sheet_name="Countries")
#price_list = '.\\Data\\sorted_test.csv'
sector_list = pd.read_excel('Data/Sectors.xlsx',sheet_name="Sectors")
size_list = pd.read_excel('Data/Sizes.xlsx',sheet_name="Sizes")
tec_list = pd.read_excel('Data/Technologies.xlsx',sheet_name="Technologies")
dates = ['2020-01-01','2050-12-01']

def define_periods(dates):
    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    periods = []
    for tot_m in range(total_months(start)-1, total_months(end)):
        y, m = divmod(tot_m, 12)
        periods.append(datetime(y, m+1, 1).strftime("%b-%y"))
    return periods

def wtp_to_dict():
    wtp_dict={}
    for i in range(len(wtps)):
        wtp_dict[wtps.loc[i,'Land'],wtps.loc[i,'Sektor'],wtps.loc[i,'Größe'],wtps.loc[i,'Technologie']]=wtps.loc[i,'avg']
    #print(wtp_dict)
    return wtp_dict

def demand_to_dict(p):
    demand_dict={}
    for i in range(len(demand)):
        j=3
        for t in p:            
            demand_dict[demand.loc[i,'Land'],demand.loc[i,'Sektor'],demand.loc[i,'Größe'],str(t)] = demand.iat[i,j]
            j+=1
        if i > 54:
            break    
    #print(demand_dict)
    return demand_dict

def supply_to_dict(p):
    supply_dict={}
    for i in range(len(supply)):
        j = 2
        for t in p:
            supply_dict[supply.loc[i,'Technologie'],str(t)] = supply.iat[i,j]
            j +=1
    #print(supply_dict)
    return supply_dict

def read_countries(country_list,wtps):
    countries={}
    sorted_countries = wtps.merge(country_list, how='inner', on="Land")
    sorted_countries = sorted_countries['Land']
    sorted_countries = sorted_countries.drop_duplicates()    
    for i in range(len(sorted_countries)-1):
        countries[i]=sorted_countries.iloc[i]
    print(countries)
    return countries

def read_sectors(sector_list,wtps):
    sectors={}
    sorted_sectors = wtps.merge(sector_list, how='inner', on="Sektor")
    sorted_sectors = sorted_sectors['Sektor']
    sorted_sectors = sorted_sectors.drop_duplicates()
    for i in range(len(sorted_sectors)-1):
        sectors[i]=sorted_sectors.iloc[i]
    print(sectors)
    return sectors


def read_sizes(sizes_list,wtps):
    sizes={}
    sorted_sizes = wtps.merge(size_list, how='inner', on="Größe")
    sorted_sizes = sorted_sizes['Größe']
    sorted_sizes = sorted_sizes.drop_duplicates()
    for i in range(len(sorted_sizes)-1):
        sizes[i]=sorted_sizes.iloc[i]
    print(sizes)      
    return sizes

def read_technologies(tec_list,wtps):
    technologies={}
    sorted_tec = wtps.merge(tec_list, how='inner', on="Technologie")
    sorted_tec = sorted_tec['Technologie']
    sorted_tec = sorted_tec.drop_duplicates()
    for i in range(len(sorted_tec)-1):
        technologies[i]=sorted_tec.iloc[i]
    print(technologies) 
    return technologies

def merit_order(dem, sup, wtp, tec, cou, sec, siz, per):
    prices = {}
    #Initialize Price Dictionary
    for t in tec:
        for p in per:
            prices[tec[t],str(p)] = 100000            
    for p in per:
        for c in cou:
            for s in sec:
                for g in siz:
                    for t in tec:
                        try:                    
                            wtp_val = wtp[(cou[c],sec[s],siz[g],tec[t])]
                            print(wtp_val)
                                #print(p)
                                #while(dem[cou[c],sec[s],siz[g],str(p)]!=0):
                            dem_val = float(dem[cou[c],sec[s],siz[g],p])
                            sup_val = float(sup[tec[t],p])
                            if sup_val > 0:
                                new_sup = sup_val - dem_val
                                if new_sup < 0:
                                    dem[cou[c],sec[s],siz[g],str(p)] = (-1)*new_sup
                                else:
                                    dem[cou[c],sec[s],siz[g],str(p)] = 0
                                    sup[tec[t],str(p)]= new_sup                     
                                if prices[tec[t],str(p)] > wtp_val:
                                    prices[tec[t],str(p)]=wtp_val
                        except KeyError:
                            pass
    
    return prices, dem, sup

def ausfuehren():
    per = define_periods(dates)
    dem = demand_to_dict(per)
    #print(dem)
    sup = supply_to_dict(per)
    wtp = wtp_to_dict()
    tec = read_technologies(tec_list,wtps)
    sec = read_sectors(sector_list,wtps)
    siz = read_sizes(size_list,wtps)
    cou = read_countries(country_list,wtps)
    prices, dem_rem, sup_dem = merit_order(dem,sup,wtp,tec,cou,sec,siz,per)
    with open('.\\Data\\Prices.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in prices.items():
            writer.writerow([key, value])
    with open('.\\Data\\Remaining Demand.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in dem_rem.items():
            writer.writerow([key, value])        
    with open('.\\Data\\Remaining Supply.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in sup_dem.items():
            writer.writerow([key, value])        


ausfuehren()



























       
