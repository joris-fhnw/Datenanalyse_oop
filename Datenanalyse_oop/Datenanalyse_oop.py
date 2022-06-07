# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 13:49:16 2021

@author: jo_st
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time

class data_analyse():


    def __init__(self,name,info):
        
        """
        Importiert ein Excel file so, dass direkt mit den namen der headers 
        gearbeitet werden kann. Bsp. Auf die Daten von x_O2_dry kann über 
        self.x_O2_dry zugegriffen werden
        
        Parameters
        ----------
        name: string des Namens der Excel datei mit Datei endung
                Bsp.: 'my_excel.xlsx'
        
        """
        self.info = info
        self.df = pd.read_excel(name, header=6)
        self.df = self.df.drop(0) #Spalte 0 löschen (enthält die Namen der NI-Karte)
        self.df = self.df.reset_index(drop = True)
        
        def change_header_name(header): 
            """
            header so bearbeiten, dass nur erster Teil verwendet wird
            Bsp.: Temp [°C] wird zu Temp
            so kann direkt mit den headers ohne [] gearbeitet werden 
            
            Parameters
            ----------
            header = array mit allen namen die Verwendet werden sollen
            """
            names = np.empty(len(header),dtype=object)
            z = 0       
            for i in header:               
                if ' ' in i:
                    temp = i.rsplit()
                    names[z] = temp[0]
                else:
                    names[z]=i#header
                z += 1    
            return names  
  
        names = change_header_name(self.df.columns)
        self.df.columns = names #DIe header wurden überschrieben
        #self.programm = self.xlsx(col)
        
        z = 0
        for i in names: 
            #Damit nicht mit self.df.T_Regler sondern direkt
            #self.T_Regler auf die Messwerte zugegriffen werden kann
            setattr(self,'{}'.format(names[z]),self.df[i])#Erzeugen der neuen Atribute
            z += 1
            
        #erzeugen der Absolut Zeit in Sekunden    
        start = datetime(202,12,8,self.Time[0].hour,self.Time[0].minute\
                         ,self.Time[0].second) #Referenz erstellen, damit mit Time gerechnet werden kann. Mit datetime.time kann nicht gerechnet werden, da kein 0Punkt vorhanden. Dieser muss erstellt werden
        diff = np.zeros(len(self.Time))    
        for i in range(0,len(diff)):    
            tmp = datetime.combine(start, self.Time[i]) - start 
            diff[i] = tmp.seconds
        self.time_abs = diff
   
    
    def delet_rows(self,header,start,end):
        """
        Werte von start bis ende werden gelöscht
        

        Parameters
        ----------
        header: Array aller Namen die verwendet werden sollen 
        start:  Start der zu löschenden Daten, muss int sein
        ende:   End der zulöschenden Daten, muss int sein
        """
        
        z = 0
        self.df = self.df.drop(self.df.index[start:end])
        self.df = self.df.reset_index(drop = True)
        for i in header:
            #self.df[i] = self.df[i][start:end] # Überschreiben des Parameters i
            delattr(self,'{}'.format(i))
            setattr(self,'{}'.format(i), self.df[i]) # Überschreiben des Parameters i
            z += 1   
        
    def stat(self,header,start,end):
        """
        Aus T_Regler wird T_Regler_stat erzeugt
        enthält nur die stationären Werte 
        
        Parameters
        ----------
        header: Array aller Namen die verwendet werden sollen 
        start:  Start Zeitpunkt des stationären Zustands
        ende:   Ende des Stationären Zustands
        """
        names = np.empty(len(header),dtype=object)
        z = 0
        for i in header:
            #locals() [i+'_norm'] = i[start:end]
            names[z] = i+'_stat'
            tmp = self.df[i][start:end]
            tmp = tmp.reset_index(drop = True)
            
            setattr(self,'{}'.format(names[z]),tmp) #setattr(self,'{}'.format(names[z]),self.df[i][start:end]) # Tatsächliche Werte übergen und nciht nur Header
            z += 1   
        
    
    def norm(self,x,M,x_O2_dry):
        """
        Erzegut norm Werte der Abgasanalyse
        Daten können über self.x_norm abgerufen werden
        
        Parameters
        ----------

        x:  
        M:  
        x_O2_dry: 
        
        Returns
        -------
        None.

        """
        p_norm = 101325 #[Pa]
        T_norm = 273.15 #[Ka]
        R = 8.314 #[J/(mol*K)]

        def roh_norm(M):
            """
            Parameters
            ----------
            M : Molmasse der Gasspezie [kg/kmol]

            Returns
            -------
            roh_norm : normdichte der Gasspezie.

            """
            roh_norm = p_norm * M /(R * T_norm)
            return roh_norm
        
        def xi_norm(x_O2_dry,x_i,M):
            """
            Parameters
            ----------
            x_O2_dry : Sauerstoffgehalt im Abges
                .
            x_i : eindimensionaler array der Gasspezie mit den 
                  dazugehörigen Werten  
                .
            M : Molmassen der Gasspezie

            Returns
            -------
            xi_norm: array der Normgrössen

            """
            x_norm = np.zeros(len(x_O2_dry))
            for i in range(len(x_O2_dry)):
                x_norm[i] = x_i[i] * roh_norm(M) * (21-10)\
                /(21-x_O2_dry[i])*1e-3 #[mg/Nm3]
            return x_norm        
       
        names = np.empty(len(x),dtype=object)
        
        for z in range(len(x)):
            names[z] = x[z].name+'_norm'            
            setattr(self,'{}'.format(names[z]),xi_norm(x_O2_dry, x[z], M[z]))

        
        

        
        
        
        #https://stackoverflow.com/questions/38264987/create-properties-in-class-from-list-attribute-in-init



#data = pd.read_csv('output_list.txt', header = None)pd.read_csv(name, header = None)

#pd.tail() = 5 Letzten Werte des ganzen Excels

#v1.xlsx.loc[0] # gibt spalte 0
