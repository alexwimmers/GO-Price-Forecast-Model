#from gurobipy import *
import csv
import datetime
#model = Model("GooPrices")

input_Goo = '.\\Data\\issuedGoos.csv'
input_Demand = '.\\Data\\monthly_demand.csv'
country_list = '.\\Data\\Countries_Tests.csv'
price_list = '.\\Data\\sorted.csv'
sector_list = '.\\Data\\Sectors_Test.csv'
size_list = '.\\Data\\Sizes.csv'
tec_list = '.\\Data\\Technologies.csv'
dates = ['2020-01-01','2027-12-01'] #Testweise nur bis 2027

# =============================================================================
#  Einlesen der Daten
# =============================================================================

def define_periods(dates):
    start, end = [datetime.datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    periods = []
    for tot_m in range(total_months(start)-1, total_months(end)):
        y, m = divmod(tot_m, 12)
        periods.append(datetime.datetime(y, m+1, 1).strftime("%b-%y"))
    return periods

def read_countries(country_list):
    countries={}
    with open(country_list, encoding = 'iso-8859-1') as country:
        country_reader = csv.reader(country, delimiter=';')
        next(country_reader)
        i=0             
        for line in country_reader:
          countries[i]=(line[0])     
          i +=1
    #print(countries)
    return countries

def read_sectors(sector_list):
    sectors={}
    with open(sector_list, encoding = 'iso-8859-1') as sector:
        sector_reader = csv.reader(sector, delimiter=';')
        next(sector_reader)
        i=0             
        for line in sector_reader:
          sectors[i]=(line[0])     
          i +=1
    #print(sectors)
    return sectors


def read_sizes(sizes_list):
    sizes={}
    with open(sizes_list, encoding = 'iso-8859-1') as size:
        size_reader = csv.reader(size, delimiter=';')
        next(size_reader)
        i=0             
        for line in size_reader:
          sizes[i]=(line[0])     
          i +=1
    #print(sizes)      
    return sizes

def read_technologies(tec_list):
    technologies={}
    with open(tec_list, encoding = 'iso-8859-1') as technology:
        tec_reader = csv.reader(technology, delimiter=';')
        next(tec_reader)
        i=0             
        for line in tec_reader:
          technologies[i]=(line[0])     
          i +=1
    #print(technologies)
    return technologies

def read_origins(origin_list):
    origins={}
    with open(origin_list) as origin:
        origin_reader = csv.reader(origin, delimiter=';')
        next(origin_reader)
        i=0             
        for line in origin_reader:
          origins[i]=(line[0])     
          i +=1
    return origins

def define_demand(periods, input_Demand):
    demand={}                                                     
    with open(input_Demand, encoding = 'iso-8859-1') as demands:
        demand_reader = csv.reader(demands, delimiter=';')
        next(demand_reader)                        
        for line in demand_reader:
            i = 3
            for p in periods:               
                demand[line[0],line[1],line[2],str(p)]=(line[i])                                            
                    #print(demand)       
                i+=1
                if i > 84:
                    break
    #print(demand)
    return demand            

def define_supply(periods, input_Supply):
    supply={}
    with open(input_Supply, encoding = 'iso-8859-1') as supplies:
        supply_reader = csv.reader(supplies, delimiter=';')
        next(supply_reader)
        for line in supply_reader:
            i = 1
            for p in periods:    
                supply[line[0],line[1],p]=(line[i])
                i += 1
    return supply

def read_prices(price_list):
    prices={}
    with open(price_list, encoding = 'iso-8859-1') as price:
        price_reader = csv.reader(price, delimiter=';')
        next(price_reader)
                    
        for line in price_reader:
            prices[line[0],line[2],line[1],line[3]]=(line[5])     
            
    return prices


# =============================================================================
#  Lineares Optimierungsmodell
# =============================================================================

def solve(countries, sectors, sizes, technologies, periods, demand, supply, prices):

    
    m = Model('priceEstimation')
# =============================================================================
#  Variablen
# =============================================================================

    purchase={}
    for c in countries:
        for s in sectors:
            for g in sizes:
                for t in technologies:
                    for p in periods:
                        purchase[countries[c],sectors[s],sizes[g],technologies[t],str(p)] = m.addVar(vtype=GRB.CONTINUOUS, name="purchase"+str(countries[c])+'_'+str(sectors[s])+'_'+str(sizes[g])+'_'+str(technologies[t])+'_'+str(p))
                        
    m.update()
    
# =============================================================================
#  Bedingungen
# =============================================================================   
    
    for c in countries:
        for s in sectors:
            for g in sizes:
                for p in periods:
                    m.addConstr(demand[countries[c],sectors[s],sizes[g],p]) >= quicksum(purchase[countries[c],sectors[s],sizes[g],technologies[t],p] for t in technologies)
     
    for t in technologies:
        m.addConstr(supply[technologies[t],p] >= quicksum(purchase[countries[c],sectors[s],sizes[g],technologies[t],p] for g in sizes for s in sectors for c in countries))              
   
    
    m.update()

# =============================================================================
#  Optimierungsproblem
# =============================================================================   
    
    m.setObjective(quicksum(purchase[countries[c],sectors[s],sizes[g],technologies[t],p]*prices[countries[c],sectors[s],sizes[g],technologies[t]] for c in countries for g in sizes for s in sectors for t in technologies for p in periods), GRB.MINIMIZE)
    
    m.update()
    
    
# =============================================================================
#  Solve
# =============================================================================    
    
    m.optimize()
    
    with open('.\\Data\\purchases.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in purchase.items():
            writer.writerow([key, value])
    
    with open('.\\Data\\prices.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in prices.items():            
            writer.writerow([key, value])
    
    for c in countries:
        for s in sectors:
            for g in sizes:
                for t in technologies:
                    for p in periods:
                        if purchase[c,s,g,t,p] > 0:
                            print("Prices for "+str(t)+' in period ' +str(p)+": " +prices[s,g,c,p,t])
                            
def test(countries, sectors, sizes, technologies, periods):
    purchase={}
    for c in countries:
        for s in sectors:
            for g in sizes:
                for t in technologies:
                    for p in periods:
                        print('Durchlauf Nr. '+str(p)) 
                        purchase[countries[c],sectors[s],sizes[g],technologies[t],str(p)] = 1
                        
    print(purchase)
                        
def ausführen():
    p = define_periods(dates)
    c = read_countries(country_list)
    g = read_sizes(size_list)
    s = read_sectors(sector_list)
    t = read_technologies(tec_list)
    d = define_demand(p,input_Demand)     
    sup = define_supply(p,input_Goo)
    pr = read_prices(price_list)
    
    '''
    for a in c:
        for b in s:
            for q in g:
                for f in p:
                    #print(c[a], )
                    #for key in d:
                        #print(key, d[key])
                    #k = str(c[a])
                    #print(k)
                    #print(p[f])
                    
                    try:
                        print(d[c[a], str(s[b]), str(g[q]), f])
                    except KeyError:
                        pass
    '''
    print('ich teste jetzt')               
    test(c,s,g,t,p)


ausführen()