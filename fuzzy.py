from simpful import *

# A simple decision support model to diagnose sepsis in the ICU
# Creating 4 fuzzy system object for each sections
#FS=Fuzzsystem for fruits
#VS=>vegetable fuzzy system
#MS=>milk related fuzzy system
#RS=> rice related fuzzy system
FS = FuzzySystem()
VS = FuzzySystem()
MS = FuzzySystem()
RS = FuzzySystem()

#Here I set the terms as high and low only
#Whatever i got in 'Main_data.iloc[:,[1,2,3,4]].mean()' I'm taking 20 as c here for fruits
# Define fuzzy sets for fruits
P1 = FuzzySet(function=Sigmoid_MF(c=20, a=0.1), term="high")
P2 = FuzzySet(function=InvSigmoid_MF(c=20, a=0.1), term="low")
FP = LinguisticVariable([P1,P2], concept="Fruits score", universe_of_discourse=[0,50])
FS.add_linguistic_variable("Fruits_Point", FP)

#Whatever i got in 'Main_data.iloc[:,[1,2,3,4]].mean()' I'm taking 20 as c here for vegetables
# Define fuzzy set for vegetables
V1 = FuzzySet(function=Sigmoid_MF(c=20, a=0.1), term="high")
V2 = FuzzySet(function=InvSigmoid_MF(c=20, a=0.1), term="low")
VP = LinguisticVariable([V1,V2], concept="Vegetables score", universe_of_discourse=[0,50])
VS.add_linguistic_variable("Vegetables_Point", VP)

#Whatever i got in 'Main_data.iloc[:,[1,2,3,4]].mean()' I'm taking 5 as c here for rice
# Define fuzzy set for rice 
R1 = FuzzySet(function=Sigmoid_MF(c=5, a=0.1), term="high")#for rice only one product will be purchased normally so if customer has taken any one of the rice product we wont recommend him/her to purchase another rice
R2 = FuzzySet(function=InvSigmoid_MF(c=5, a=0.1), term="low")
RP = LinguisticVariable([R1,R2], concept="Rice score", universe_of_discourse=[0,10])
RS.add_linguistic_variable("Rice_Point", RP)

#Whatever i got in 'Main_data.iloc[:,[1,2,3,4]].mean()' I'm taking 5 as c here for milk
# Define fuzzy set for milk
M1 = FuzzySet(function=Sigmoid_MF(c=5, a=0.1), term="high")
M2 = FuzzySet(function=InvSigmoid_MF(c=5, a=0.1), term="low")
MP = LinguisticVariable([M1,M2], concept="Milk score", universe_of_discourse=[0,10])
MS.add_linguistic_variable("Milk_Point", MP)

#A graphical representation of the fuzzy variables value range and terms "high","low"
#FS.produce_figure()
#VS.produce_figure()
#MS.produce_figure()
#RS.produce_figure()

#Actual and possible ooutcomes of fuzzy system
# Defining the consequents
FS.set_crisp_output_value("high_chance_for_fruit", 100)
FS.set_crisp_output_value("low_chance_for_fruit", 10)
VS.set_crisp_output_value("high_chance_for_vegetables", 100)
VS.set_crisp_output_value("low_chance_for_vegetables", 10)
MS.set_crisp_output_value("high_chance_for_milk", 100)
MS.set_crisp_output_value("low_chance_for_milk", 10)
RS.set_crisp_output_value("high_chance_for_rice", 100)
RS.set_crisp_output_value("low_chance_for_rice", 10)

#New rules
RULE1="IF (Fruits_Point IS high) THEN (Purchase IS low_chance_for_fruit)"
RULE2="IF (Fruits_Point IS low) THEN (Purchase IS high_chance_for_fruit)"
RULE3="IF (Vegetables_Point IS low) THEN (Purchase IS high_chance_for_vegetables)"
RULE4="IF (Vegetables_Point IS high) THEN (Purchase IS low_chance_for_vegetables)"
RULE5="IF (Rice_Point IS low) THEN (Purchase IS high_chance_for_rice)"
RULE6="IF (Rice_Point IS high) THEN (Purchase IS low_chance_for_rice)"
RULE7="IF (Milk_Point IS low) THEN (Purchase IS high_chance_for_milk)"
RULE8="IF (Milk_Point IS high) THEN (Purchase IS low_chance_for_milk)"

#Adding the appropriate rules to each fuzzy systems
FS.add_rules([RULE1, RULE2])
VS.add_rules([RULE3, RULE4])
RS.add_rules([RULE5, RULE6])
MS.add_rules([RULE7, RULE8])

#fuzzy function defined , inputs will be the points got for the customer after buying all items from different respective sections
#a=>fruits point,b=> vegetable points,c=> rice,d=> milk
def fuzzy(a,b,c,d):
    #setting antecedents
    FS.set_variable('Fruits_Point', a)
    VS.set_variable('Vegetables_Point', b)
    RS.set_variable('Rice_Point', c)
    MS.set_variable('Milk_Point', d)
    #a=FS.Sugeno_inference(["Purchase"])
    #p=a["Purchase"]
    #the Purchase is a variable here.This one is also used in rules too. Check for Purchase in rules you can see "Purchase IS" in all rules
    f=FS.Sugeno_inference(["Purchase"])
    f=f["Purchase"]

    v=VS.Sugeno_inference(["Purchase"])
    v=v["Purchase"]

    m=MS.Sugeno_inference(["Purchase"])
    m=m["Purchase"]

    r=RS.Sugeno_inference(["Purchase"])
    r=r["Purchase"]
    
    return f,v,m,r

###################################################
##############final code session###################
###################################################
import pandas as pd
import streamlit as st
#importing the repaired dataset for further process
#fuzzydat,fruits,vegetables,milk,rice were saved as csv in previous code session
Main = pd.read_csv("fuzzdat/fuzzydat.csv")
fruits = pd.read_csv("fuzzdat/fruits.csv")
#We need to sort the dataset to get High rated products becomes at the top
#this ratings were randomly generated. Based on the profit method we can change these ratings for each product for more clarified way of doing
#eg: chillies are small quantity neede so it can be rated as 2 point or 1 point where as the potato,tomato are more needed so it can be rated as 6/7/8/9 as our wish or clients criteria
fruits=fruits.sort_values("Points",ascending=False)
#similarly here also
veggies = pd.read_csv("fuzzdat/vegetables.csv")
veggies=veggies.sort_values("Points",ascending=False)
milk = pd.read_csv("fuzzdat/milk.csv")
milk=milk.sort_values("Points",ascending=False)
rice = pd.read_csv("fuzzdat/rice.csv")
rice=rice.sort_values("Points",ascending=False)

#Function to get the items bought by the customer. Reads a string of a no of items bought by the customer
def Items_Bought_by_Customer():
    #input("Items bought")
    Items=txxt
    #The function get_customer_points will return the Items, fruit point, vegetables point,milk point,rice point for the customer
    Items,f,v,m,r = get_customer_points(Items)
    return Items,f,v,m,r

#calculates the points based on the items purchased, Input would be the string: Items bought by the customer
def get_customer_points(x):
    #consider an empty list lst, fp,vp,mp,rp are points which are points of fruit,veg,milk,rice
    lst = []
    fp=0
    vp=0
    mp=0
    rp=0
    #converting the argument to string
    items = str(x)
    #Appends items to lst
    lst.append(items.split(","))
    #Gets all kind of items in an iterable format
    all_items=[i for item in lst for i in item]
    #if any items in the list all_items then corresponding points will be calculated forcorresponding products and added and stored for return
    for i in all_items:
        for j in range(24):
            if(i == fruits.iloc[j,0]):
                fp = fp+fruits.iloc[j,1]
    for i in all_items:
        for j in range(14):
            if(i == veggies.iloc[j,0]):
                vp = vp+veggies.iloc[j,1]
    for i in all_items:
        for j in range(3):
            if(i == milk.iloc[j,0]):
                mp = mp+milk.iloc[j,1]
    for i in all_items:
        for j in range(71):
            if(i == rice.iloc[j,0]):
                rp = rp+rice.iloc[j,1]
    return all_items,fp,vp,mp,rp
    
#Function for recommendation, input would be the output of fuzzy=>probability of a customer to buy from correspoding/respective section(fruit/veg/rice/milk)
def fruit(F):
    
    #Fruit-case
    #fruits will be recommended only if the customer has bought fruits
    while(f>0):
        #The value 75 was based on my logic we change it upto the criteria needed by client
        #if the probability is less than 75 that means the customer has already bought some fruits so less chance to buy high rated/pointed fruits hence recommending low point fruits

        #Items="dasherimango,dholkapomogranates,soursopcustardapple,hortusgoldpapaya,galaapple,tomatolocal,cherrietomato,redchilli,gaajar,redbellpepper,buffalomilk,brownrice"
        fruit=list(fruits['product'])
        #list f contains only fruits other than the fruits bought by the customer. There wont be any any fruit in f which is already purchased by the customer
        fr=[items for items in fruit if items not in Items]
        if(f < 75):
            return (fr[-5:-1])
            break
            #else we recommend some high rated/pointed fruits    
        else:
            return (fr[0:5])
            break
    return 0
    #similarly in vegetables also
    #Vegetables-case
    #vegetables will be recommended only if the customer has bought vegetables
def vegetable(V):
    while(v>0):
        vegg=list(veggies['product'])
        vr=[items for items in vegg if items not in Items]
        if(v < 75):
            return (vr[-5:-1])
            break
        else:
            return (vr[0:5])
            break
    return 0
    #similarly in milk case
    #Milk-Case
    #Milk  products are recommended only if the customer has bought milk products
def milks(M):
    while(m>0):
        #in milk secction we have only 3 unique milk buffalo,toned,cow so I though to recommend all other than the bought milk
        mi=list(milk['product'])
        mr=[items for items in mi if items not in Items]
        #if the ist mr is empty means the whole milk products are already bought.
        #then there is no need of recommending it again
        if(mr==[]):
            continue
        else:
            if(m < 55):
                return (mr)
                break
            else:
                return (mr)
                break
    return 0
    #Rice-Case
    #rice products are recommended only if the customer has bought rice products
def rices(R):
    while(r>0):
        #similar to fruits/vegetable case
        ri=list(rice['product'])
        ra=[items for items in ri if items not in Items]
        if(r < 45):
            return (ra[-3:-1]) 
            break
        
        else:
            return (ra[0:3])
            break
    return 0

st.write("""
         # Fuzzy Application
         """)

txt = st.text_input("Items bought by the customer")

Items,f,v,m,r = Items_Bought_by_Customer()
F, V, M, R = fuzzy(f,v,m,r)
a = fruit(F)
b = vegetable(V)
c = milks(M)
d = rices(R)
#######
st.write("""
         ### choose items from below
         """)
txt=[]
frts = st.multiselect("Fruits",options=fruits["product"])
for i in frts:
    txt.append(i)
vgs = st.multiselect("Vegetables", options=veggies['product'])
for i in vgs:
    txt.append(i)
milkk = st.multiselect("Milk products", options=milk['product'])
for i in milkk:
    txt.append(i)
rce = st.multiselect("Rice products", options = rice['product'])
for i in rce:
    txt.append(i)

dep = st.button("Submit")

txxt=[]
if(dep):
    txxt = ",".join(txt)

Items,f,v,m,r = Items_Bought_by_Customer()
F, V, M, R = fuzzy(f,v,m,r)
a = fruit(F)
b = vegetable(V)
c = milks(M)
d = rices(R)
#######
s=[]
while(txxt != s):
    st.write("""
             We recommend you some of these
             """)

    if(a != 0):
        st.write("""
                 ## Fruits
                 """)
        for i in a:
            st.write(i,"\t")

    if(b != 0):
        st.write("""
                 ## Vegetables
                 """)
        for i in b:
            st.write(i)
    
    if(c != 0):
        st.write("""
                 ## Milk products
                 """)
        for i in c:
            st.write(i)

    if(d != 0):
        st.write("""
                 ## Rice products
                 """)
        for i in d:
            st.write(i)
    break
