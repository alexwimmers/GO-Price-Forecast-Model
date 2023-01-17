#from gurobipy import *
import csv
import datetime
#model = Model("GooPrices")

input_Goo = '.\\Data\\issuedGoos.csv'
input_Demand = '.\\Data\\monthly_demand.csv'
country_list = '.\\Data\\Countries.csv'
price_list = '.\\Data\\sorted.csv'
sector_list = '.\\Data\\Sectors.csv'
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
    with open(country_list) as country:
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
    with open(sector_list) as sector:
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
    with open(sizes_list) as size:
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
    with open(tec_list) as technology:
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

def define_demand(countries, sectors, sizes, periods, input_Demand):
    demand={}
    for g in sizes:        
        for c in countries:
            for s in sectors:                                                     
                with open(input_Demand) as demands:
                    demand_reader = csv.reader(demands, delimiter=';')
                    next(demand_reader)                        
                    for line in demand_reader:
                        for p in periods:
                            i=3
                            print(countries[c]+sectors[s]+sizes[g]+str(p)+str(i)+": "+ line[i])
                            demand[countries[c],sectors[s],sizes[g],p]=(line[i])                                            
                    #print(demand)       
                            i+=1
    print(demand)
    return demand            

def define_supply(countries, periods, technologies, input_Supply):
    supply={}
    for c in countries:
        for t in technologies:
            for p in periods:
                with open(input_Supply) as supplies:
                        supply_reader = csv.reader(supplies, delimiter=';')
                        next(supply_reader)
                        i = 1
                        for line in supply_reader:
                            supply[c,t,p]=(line[i])
                            i += 1
    return supply

def read_prices(countries, periods, technologies, sectors, sizes, price_list):
    prices={}
    for c in countries:
        for s in sectors:
            for g in sizes:
                for t in technologies:
                    with open(price_list) as price:
                        price_reader = csv.reader(price, delimiter=';')
                        next(price_reader)
                        i=0             
                        for line in price_reader:
                          prices[c,s,g,t]=(line[5])     
                          i +=1
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
                        purchase[c,s,g,t,p] = m.addVar(vtype=GRB.CONTINUOUS, name="purchase"+str(c)+'_'+str(g)+'_'+str(s)+'_'+str(t)+'_'+str(p))
                        
    m.update()
    
# =============================================================================
#  Bedingungen
# =============================================================================   
    
    for c in countries:
        for s in sectors:
            for g in sizes:
                for p in periods:
                    m.addConstr(demand[c,s,g,p]) >= quicksum(purchase[s,g,c,p,t] for t in technologies)
     
    for t in technologies:
        m.addConstr(supply[t,o,p] >= quicksum(purchase[s,g,c,p,t] for s in sectors for g in sizes for c in countries))              
   
    
    m.update()

# =============================================================================
#  Optimierungsproblem
# =============================================================================   
    
    m.setObjective(quicksum(purchase[s,g,c,p,t]*prices[s,g,c,p,t] for c in countries for g in sizes for s in sectors for t in technologies for p in periods), GRB.MINIMIZE)
    
    m.update()
    
    
# =============================================================================
#  Solve
# =============================================================================    
    
    m.optimize()

    for c in countries:
        for s in sectors:
            for g in sizes:
                for t in technologies:
                    for p in periods:
                        if purchase[c,s,g,t,p] > 0:
                            print("Prices for "+str(t)+' in period ' +str(p)+": " +prices[s,g,c,p,t])
                            

def ausführen():
    p = define_periods(dates)
    c = read_countries(country_list)
    g = read_sizes(size_list)
    s = read_sectors(sector_list)
    t = read_technologies(tec_list)
    d = define_demand(c,s,g,p,input_Demand)     
    sup = define_supply(c,p,t,input_Goo)
    pr = read_prices(c,p,t,s,g,price_list)       
    solve(c,s,g,t,p,d,sup,pr)


ausführen()