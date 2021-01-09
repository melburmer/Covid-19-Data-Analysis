# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 15:16:19 2020

@author: Pc
"""
import warnings
warnings.filterwarnings('ignore')
import pandas as pd 
import numpy as np
import math


df_line = pd.read_csv(r"dataset/COVID19_line_list_data.csv")

df_open = pd.read_csv(r"dataset/COVID19_open_line_list.csv")

df_line.columns

# dataframe'i temizleyelim

df_line = df_line.iloc[:,:-6]


df_line.columns


df_line.drop(['Unnamed: 3',"source","link"],axis=1,inplace=True)


# Hastalıktan ölenlerin yaş ortalaması 

deaths = df_line[df_line["death"]!="0"]

print("Average death age: " + str(deaths["age"].mean()))

# Hastalıktan ölenlerin cinsiyeti

male_number = deaths["gender"].value_counts()["male"]

female_number = deaths["gender"].value_counts()["female"]

total = female_number  + male_number

print("% of deaths by gender => Male: %{0}, Female: %{1}".format(int(round(male_number*100/total)),int(round(female_number*100/total))))

# semptomplar başladıktan kaç gün sonra ölüyorlar

only_death_date = deaths[df_line["death"]!="1"]

only_death_date.dropna(subset=['symptom_onset'],inplace=True)

only_death_date.reset_index(inplace=True)

only_death_date["death_time(day)"] = (pd.to_datetime(only_death_date['death']) - pd.to_datetime(only_death_date['symptom_onset']))

only_death_date["death_time(day)"] = only_death_date["death_time(day)"].apply(lambda x: int(x.days))


only_death_date = only_death_date[["location","country","gender","age","symptom_onset","death","symptom","death_time(day)"]]

only_death_date.drop(["location"],axis=1,inplace=True)
# diğer df ile birleştirelim

df_open["outcome"] = df_open["outcome"].apply(lambda x:"death" if x== "died" else x)

deaths_df2 = df_open[df_open["outcome"]=="death"]
deaths_df2.dropna(subset=['date_death_or_discharge',"date_onset_symptoms"],inplace=True)

deaths_df2 = deaths_df2[["province","country","sex","age","date_onset_symptoms","symptoms",'date_death_or_discharge']]
deaths_df2.reset_index(inplace=True)

deaths_df2['date_death_or_discharge'][0] = "02.09.2020"
deaths_df2["death_time(day)"] = (pd.to_datetime(deaths_df2['date_death_or_discharge']) - pd.to_datetime(deaths_df2['date_onset_symptoms']))
deaths_df2["death_time(day)"] = deaths_df2["death_time(day)"].apply(lambda x: int(x.days))

deaths_df2["country"][2] =deaths_df2["province"][2]
deaths_df2.drop(["index","province"],axis=1,inplace=True)


deaths_df2.columns = ["country","gender","age","symptom_onset","symptom","death","death_time(day)"]

only_death_date = only_death_date.append(deaths_df2)
only_death_date.reset_index(inplace=True)

only_death_date.drop(["index"],axis=1,inplace=True)



only_death_date = only_death_date[['country','age','gender','symptom_onset','death','death_time(day)','symptom']]
only_death_date.head()

temp = only_death_date.groupby("gender").mean()["death_time(day)"]

print("Average death time after symptom onset by gender (Note: There is not enough data to make a good inference.)\n=> male:{} days, female:{} days"
      .format(int(only_death_date.groupby("gender").mean()["death_time(day)"]["male"]),int(only_death_date.groupby("gender").mean()["death_time(day)"]["female"])))



# tedavi olanların yaş ortalaması 
recovered = df_line[df_line["recovered"] != "0"]

print("Average recovered age: " + str(round(recovered["age"].mean())))

# tedavi olanların cinsiyeti

male_number = recovered["gender"].value_counts()["male"]

female_number = recovered["gender"].value_counts()["female"]

total = female_number  + male_number

print("% of recovered by gender => Male: %{0}, Female: %{1}".format(int(round(male_number*100/total)),int(round(female_number*100/total))))


# tedavi kaç hafta sürüyor


recovered = recovered[recovered["recovered"] != "1"]

recovered = recovered[[ 'reporting date', 'country', 'gender', 'age','recovered','symptom']]

# deleting wrong entries (like recovered date: 12/30/1899 etc.)
recovered.reset_index(inplace=True,drop=True)

for index,date in enumerate(recovered["recovered"].values):
    if(date.split("/")[2] == "1899"):
        recovered.drop(index,axis=0,inplace=True)

    
recovered["recover_time"] = (pd.to_datetime(recovered['recovered']) - pd.to_datetime(recovered['reporting date']))
recovered["recover_time"] = recovered["recover_time"].apply(lambda x: int(x.days))


#  some fixes
recovered = recovered[recovered["recover_time"]>=0]

recovered["recover_time"] = recovered["recover_time"].apply(lambda x: 1 if x== 0 else x)

recovered = recovered[['country', 'gender', 'age','reporting date', 'recovered','recover_time', 'symptom']]


print("Average treatment time(days): {0}".format(round(recovered["recover_time"].mean())))


print("\nAverage treatment time(days) (by gender) => Male: {0} Female: {1}"
      .format(round(recovered.groupby("gender").mean()["recover_time"]["male"])
      ,round(recovered.groupby("gender").mean()["recover_time"]["female"])))

recovered_by_country = recovered.groupby("country").mean()

recovered_by_country["age"] = recovered_by_country["age"].apply(lambda x:int(x) if(math.isnan(x)==False) else x)

recovered_by_country["recover_time"] = recovered_by_country["recover_time"].apply(lambda x:int(x) if(math.isnan(x)==False) else x)

recovered_by_country.rename(columns={'age':"avarage age","recover_time":"avarage recover time(days)"},inplace=True)


# recover time by age


def set_interval(age):
    if(age>0 and age<=10):
        return "0-10"
    elif(age> 10 and age<=18):
        return "10-18"
    elif(age>18 and age <30 ):
        return "18-30"
    elif(age>=30 and age <60):
        return "30-60"
    elif(math.isnan(age)):
        return np.nan
    else :
        return "60+"
    

recovered["age_interval"] = recovered["age"].apply(set_interval)

recover_by_age = recovered.groupby("age_interval").mean()["recover_time"]

recover_by_age = recover_by_age.astype(int)

recover_by_age = pd.DataFrame(recover_by_age.values,index =recover_by_age.index,columns=["avg recover time(days)"])
recover_by_age.head()


# semptomlara göre bakma
# lets use df2

symptoms = df_open.copy()
symptoms.dropna(subset=['symptoms'],inplace=True)

symptoms.drop(11233,axis=0,inplace=True)

# some symptoms

symp_dict = {"fever":0,"cough":0,"pneumonia":0,"fatigue":0,"headache":0,
             "chills":0,"sputum":0,"joint_pain":0,"diarrhea":0,
             "runny_nose":0,"malaise":0,"vomiting":0,"nausea":0}



for sym in symptoms['symptoms'].values:
    if("fever" in sym.lower()):
        symp_dict["fever"]+=1
    if("cough" in sym.lower()):
        symp_dict["cough"]+=1 
    if("pneumonitis" in sym.lower() or "pneumonia" in sym.lower() ):
        symp_dict["pneumonia"]+=1        
    if("fatigue" in sym.lower()):
        symp_dict["fatigue"]+=1 
    if("headache" in sym.lower()):
        symp_dict["headache"]+=1    
        
    if("chills" in sym.lower()):
        symp_dict["chills"]+=1 
    if("sputum" in sym.lower()):
        symp_dict["sputum"]+=1
    if("joint" in sym.lower()):
        symp_dict["joint_pain"]+=1
        
    if("diar" in sym.lower()):
        symp_dict["diarrhea"]+=1 
        
    if("runny" in sym.lower()):
        symp_dict["runny_nose"]+=1 
        
    if("mala" in sym.lower()):
        symp_dict["malaise"]+=1 
       
    if("vomit" in sym.lower()):
        symp_dict["vomiting"]+=1      
    if("nau" in sym.lower()):
        symp_dict["nausea"]+=1         

sympts = pd.DataFrame(data = symp_dict.items(),columns=["symptom","symptom_count"])

sympts.set_index("symptom",inplace=True)
        
sympts["Occurance Rate"] = sympts["symptom_count"]/symptoms.shape[0]*100


sympts["Occurance Rate"] = sympts["Occurance Rate"].apply(lambda x: "% "+str(int(round(x))))




# semptomlar çıktıktan kaç gün sonra hastaneye başvuruyorlar

after_days = df_open.dropna(subset=["date_onset_symptoms","date_admission_hospital"])


after_days = after_days[["country","age","sex","outcome","date_onset_symptoms","date_admission_hospital"]]


after_days.drop([476,477,478,479,480,1379,101],inplace=True,axis=0) # deleting some rows

after_days["hospital_admission_time"]  = (pd.to_datetime(after_days["date_admission_hospital"],utc=True,dayfirst=True) - pd.to_datetime(after_days["date_onset_symptoms"],utc=True,dayfirst=True))

after_days["hospital_admission_time"] = after_days["hospital_admission_time"].apply(lambda x: int(x.days))


after_days = after_days[after_days["hospital_admission_time"]>=0]
after_days.reset_index(inplace=True,drop=True)

after_days["hospital_admission_time"] = after_days["hospital_admission_time"].apply(lambda x: 1 if x==0 else x)


# ortalama hastaneye gitme süresi

print("\nAverage hospital admission time(days) after symptoms on set:{0} ".format(int(round(after_days["hospital_admission_time"].mean()))))

# hastanaye gitme sürelerinin ülkeye karşılaştırılması
admission_by_country = after_days.groupby("country").mean()["hospital_admission_time"].apply(lambda x: str(int(round(x))) + " days")






