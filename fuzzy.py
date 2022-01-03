import pandas as pd

#EDA on data set

Data=pd.read_excel("I:/innodatics intern/Customer_Data_PROJECT.xlsx")

profile_report = Data.iloc[:,4:].profile_report(html={"style": {"full_width": True}})
profile_report.to_file("I:/innodatics intern/fuzzdat/first.html")
#reading the main dataset Customer data for the project
#copiying the fruits column into a variable fruits_data
fruits_data=Data["order_fruits"]
#copiying the vegetable column into a variable veg_data
veg_data=Data["order_vegetables"]
#copiying the rice column into a variable rice_data
rice_data=Data["order_rice"]
#copiying the milk column into a variable milk_data
milk_data=Data["order_milk"]


#########
###EDA###
#########
Data.isna().sum()#610 null values
#picking the unique items in each section(eg: kamiyapapaya, kesarmango,etc in fruits)
# (eg: brocoli,gajar etc in vegetable)
#similarily from other section
#removes null vaues in the columns extracted from Data
#drops na values in fruits_data,veg_data,rice_data,milk_data and stores them into variables => fruits,vegetables,rice,milk
fruits = fruits_data.dropna()
vegetables = veg_data.dropna()
rice = rice_data.dropna()
milk = milk_data.dropna()

#defining a function to clean the data EDA main part 
def clean(x):
    #converting the arguments passed into lower cased string
    data = x.str.lower()
    #found that there are lots of values like those in the list sw.And those are quantity details. They are not needed so those will be removed
    sw = [' ','-100g','-200g','-250g','-0.25kg','-500g','-0.5kg','-0.50kg','-750g','-0.75kg','-1kg','-1.5kg','-2kg','-2.5kg','-3kg','-3.5kg','-4kg','-4.5kg','-5kg','-6kg','-7kg','-7.5kg','-8kg','-9kg','-10kg','-11kg','-12kg','-13kg','-14kg','-15kg','-1pc','-2pc','-3pc','-4pc','5pc','6pc','-1kg-2pc','-0.25l','-0.5l','-0.75l','-1l','-1.5l','-2l','-2.5l','-3l','-3.5l','-4l','-']
    #replacing the strings in sw present in data with ""
    data = data.replace(sw,"",regex=True)
    #also found misspelled pomograntes,pomogranetes. So they are also replaced else it would be like 2 different items
    f = ['pomograntes','pomegranetes']
    data = data.replace(f,"pomogranates",regex=True)
    #this function is to find unique items in each sections so removes all duplicates
    basket_item=[item for item in data]
    basket_items_list=[]
    for i in basket_item:
        basket_items_list.append(i.split(","))
    all_items=[i for item in basket_items_list for i in item]
    no_of_items=pd.DataFrame(list(set(all_items)))
    no_of_items.columns = ["product"]
    return no_of_items
#get cleaned and unique items in each sections
fruits = clean(fruits)
veg = clean(vegetables)
rice = clean(rice)        
milk = clean(milk)

#I'm going to generate some random points for products in all the 4 sectors.(In real world we can make this points based on the value of profit that the product provide to the enterprise/ based on how it is highly relevant to the customer)
import numpy as np
#generating some random points from 1-10 into the unique items in each section: fruits,vegetables,rice,milk
fruits["Points"] = np.random.randint(1, 10, fruits.shape[0])
veg["Points"] = np.random.randint(1,10,veg.shape[0])
rice["Points"] = np.random.randint(1,10,rice.shape[0])
milk["Points"] = np.random.randint(1,10,milk.shape[0])
#saving those into csv file so that can be used for further use/ those random points may change thats why saving them to new files
fruits.to_csv("fruits.csv")
veg.to_csv("vegetables.csv")
rice.to_csv("rice.csv")
milk.to_csv("milk.csv")

#defining a function to calculate points for each customer based on the items bought by him/her. taking points from those previously created csv
def get_customer_data(x):
    lst = []
    fp=0
    vp=0
    mp=0
    rp=0
    items = str(x)
    lst.append(items.split(","))
    all_items=[i for item in lst for i in item]
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
    return fp,vp,mp,rp

#creating new dataset to show the ||customer's bought items||fruit points||vegetable points||milk points||rice points|| 
Main = pd.DataFrame(columns=(['Items_bought','fruit_points','vegetable_points','milk_points','rice_points']))
#the bought items would come under the column "items_bought"
Main['Items_bought']=Data['basket']
#here I dont drop null instead fill na with "". Dropping can cause losing 610 rows.
Main['Items_bought']=Main['Items_bought'].fillna("")
#here defining a function to clean the total items bought. here we dont need the things to be unique we need all the rows of items bought by the customer
def clean2(x):
    #converting the arguments passed into lower case string
    data = x.str.lower()
    #found that there are lots of values like those in the list sw.And those are quantity details. They are not needed so those will be removed
    sw = [' ','-100g','-200g','-250g','-0.25kg','-500g','-0.5kg','-0.50kg','-750g','-0.75kg','-1kg','-1.5kg','-2kg','-2.5kg','-3kg','-3.5kg','-4kg','-4.5kg','-5kg','-6kg','-7kg','-7.5kg','-8kg','-9kg','-10kg','-11kg','-12kg','-13kg','-14kg','-15kg','-1pc','-2pc','-3pc','-4pc','5pc','6pc','-1kg-2pc','-0.25l','-0.5l','-0.75l','-1l','-1.5l','-2l','-2.5l','-3l','-3.5l','-4l','-']
    data = data.replace(sw,"",regex=True)
    #also found misspelled pomograntes,pomogranetes. So they are also replaced else it would be like 2 different items
    f = ['pomograntes','pomegranetes']
    #replacing the items in f( if present in our data ) with "pomogranates"
    data = data.replace(f,"pomogranates",regex=True)
    return data
Main["Items_bought"] = clean2(Main['Items_bought'])

#the function get_customer_data returns points based on the items purchased, which will be stored in respective/corresponding columns(1=>fruit_points,2=>vegetable_points,3=>milk points,4=>rice_points)
#appliying the get_customer_data function only for the first 10000 rows only for now
for i in range(10001):
    Main.iloc[i,[1,2,3,4]]=get_customer_data(Main.iloc[i,0])

#Taking only the rows with points calculated
Main_data= Main.iloc[0:10000,:]
#EDA on Main_data(got after cleaning it and providing points to the corresponding customer based on the products bought by him)
Df=pd.read_csv("I:/innodatics intern/fuzzdat/fuzzydat.csv")
#pip install pandas-profiling
import pandas_profiling
from pandas_profiling.utils.cache import cache_file
#Df.profile_report()
profile_report = Df.profile_report(html={"style": {"full_width": True}})
profile_report.to_file("I:/innodatics intern/fuzzdat/example.html")
#saving the main data as a new file for further process
Main_data.to_csv("fuzzydat.csv")


#Calculating an average score from each section
#so that i can pass it to the fuzzy sets 
#which takes average value as center and compare it with the inputs
"Average Score at each section"
Main.iloc[:,[1,2,3,4]].mean()


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
def Items_Bought_by_Customer(t):
    #input("Items bought")
    Items=t
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

Items,f,v,m,r = Items_Bought_by_Customer(txxt)
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
