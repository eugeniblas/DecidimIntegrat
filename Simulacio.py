##################################################################################################
#                                                                                                #
#   AUTHOR: Eugeni Blas                                                                          #
#                                                                                                #
#   [Simulació Casos per Enquesta Pressupostos Participatius IMOP]                               #
#                                                                                                #
##################################################################################################

import time
import cplex
import os
import csv

class Simulacio: 
      
    ##############################################################################
    #
    # ESCENARIOS 3 & 4 - NO COINCIDENTES
    # (METODO IA - NO Seleccionadas)
    #
    ##############################################################################
    def sim1(self):  
        print("****************************************************************")
        print("* ESCENARIOS 3 & 4 - NO COINCIDENTES")
        print("****************************************************************")
        wd = os.getcwd()
        nameFile = "IA_NOS_ALE"
        datafile = wd +"/Simulacio/"+ "/" + nameFile + ".txt"
        output = open(datafile, "w")
        # csv file
        datafile = wd +"/Simulacio/"+ "/" + nameFile + ".csv"         
        csvfile = open(datafile, 'w', newline='') 
        #csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter = csv.writer(csvfile)
        importP=[8.5,7.25,7,6.5,5.5,5.25,5,4.75,4.5,3.25]
        ctrl=[0,0,0,0,0,0,0,0,0,0]
        seleccio=[0,0,0,0,0,0,0,0,0,0]
        ctrlS=[0,0,0,0,0,0,0,0,0,0]
        for i1 in range(0,10):          
            for i2 in range(i1+1,10):
                for i3 in range(i2+1,10):

                    #propostas enquestat no seleccionades 
                    ctrl[i1]=1
                    ctrl[i2]=1
                    ctrl[i3]=1
                    seleccio[7]=i1
                    seleccio[8]=i2
                    seleccio[9]=i3

                    #proposta exces ("fer salt") #######
                    for i4 in range(10):
                        if ctrl[i4]==0:
                            ctrl[i4]=1
                            seleccio[3]=i4 
                            break       

                    #propostes 4 seleccionades (3+1: al mig l'exces 3+E+1)
                    #  seleccio previa de les 6 lliures
                    explorar=[0,0,0,0,0,0]
                    ctrl2 = [0,0,0,0,0,0,0,0,0,0]
                    for kk in range(10):
                        ctrl2[kk] = ctrl[kk]
                    for j1 in range(6):
                        for j2 in range(10):
                            if ctrl2[j2]==0:
                                explorar[j1]=j2
                                ctrl2[j2]=1
                                break
                    #   obtencio 4 millors ##
                    sum = 0
                    for k1 in range(6):
                        for k2 in range(k1+1,6):
                            for k3 in range(k2+1,6):
                                for k4 in range(k3+1,6):
                                    sumP = importP[explorar[k1]]+importP[explorar[k2]]+importP[explorar[k3]]+importP[explorar[k4]]
                                    #if (sumP > 23-importP[seleccio[3]] and sumP <= 23):
                                    if (sumP > sum and sumP <= 23):                                     
                                        seleccion2=[explorar[k1],explorar[k2],explorar[k3],explorar[k4]]
                                        sum = sumP
                                        
                    sumEXC = importP[explorar[0]]+importP[explorar[1]]+importP[explorar[2]]
                    if sumEXC+importP[seleccio[3]] > 23:  # 3 es l'exces
                        # amb 4 es sufiecent
                        ctrl[seleccion2[0]] = 1
                        ctrl[seleccion2[1]] = 1
                        ctrl[seleccion2[2]] = 1
                        ctrl[seleccion2[3]] = 1                    
                        seleccio[0] = seleccion2[0]
                        seleccio[1] = seleccion2[1]
                        seleccio[2] = seleccion2[2]
                        seleccio[4] = seleccion2[3] # fem salt per l'exces
                        lliures = 2
                        ctrlS[0]=1
                        ctrlS[1]=1
                        ctrlS[2]=1
                        ctrlS[4]=1
                    else:
                        # amb 4 es NO sufiecent -> necessitem 5  
                        sum = 0
                        for k1 in range(6):
                            for k2 in range(k1+1,6):
                                for k3 in range(k2+1,6):
                                    for k4 in range(k3+1,6):
                                        for k5 in range(k4+1,6):                                    
                                            sumP = importP[explorar[k1]]+importP[explorar[k2]]+importP[explorar[k3]]+importP[explorar[k4]]+importP[explorar[k5]]
                                            if (sumP > sum and sumP <= 23):
                                                seleccion3=[explorar[k1],explorar[k2],explorar[k3],explorar[k4],explorar[k5]]
                                                sum = sumP
                        seleccio[4] = seleccio[3]
                        ctrl[seleccion3[0]] = 1
                        ctrl[seleccion3[1]] = 1
                        ctrl[seleccion3[2]] = 1
                        ctrl[seleccion3[3]] = 1 
                        ctrl[seleccion3[4]] = 1                   
                        seleccio[0] = seleccion3[0]
                        seleccio[1] = seleccion3[1]
                        seleccio[2] = seleccion3[2]
                        seleccio[3] = seleccion3[3]
                        seleccio[5] = seleccion3[4] # fem salt 4+E+1
                        lliures = 1
                        ctrlS[0]=1
                        ctrlS[1]=1
                        ctrlS[2]=1
                        ctrlS[3]=1
                        ctrlS[5]=1
                
                    # omplir lliures 8i9 o nomes 9
                    for l1 in range(lliures):
                        for l2 in range(10):
                            if ctrl[l2]==0:
                                ctrl[l2]=1
                                seleccio[(7-lliures)+l1]=l2
                                break

                    # ALEATORITZACIO (0,1,2,3,4,5,6,7,8,9)==>(2,0,1,3,4,5,6,9,7,8)
                    aux0 = seleccio[0]
                    aux1 = seleccio[1]
                    aux2 = seleccio[2]
                    aux7 = seleccio[7]
                    aux8 = seleccio[8] 
                    aux9 = seleccio[9]
                    seleccio[0]=aux2
                    seleccio[1]=aux0
                    seleccio[2]=aux1
                    seleccio[7]=aux9
                    seleccio[8]=aux7
                    seleccio[9]=aux8

                    #s1 = importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]
                    if lliures==1:
                        s1 = importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]+importP[seleccio[3]]
                        sOK = s1 + importP[seleccio[5]]
                        sEX = s1 + importP[seleccio[4]]
                    else: 
                        s1 = importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]
                        sOK = s1 + importP[seleccio[4]]
                        sEX = s1 + importP[seleccio[3]]
                    avisSOK = " "
                    # comprovar que la suma es menor o igual que 23 i que no podem agafar mes prop.
                    if sOK > 23 or sOK+3.25 < 23:
                        avisSOK = "ERROR-SUM"
                    avisSEX = " "
                    if sEX <= 23:
                        avisSEX = "ERROR-EXC"

                    sOKcsv = int(sOK*1000000)
                    if lliures == 1:
                        s34primeras = int((importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]+importP[seleccio[3]])*1000000)
                        propExc = int(importP[seleccio[4]]*1000000)
                        sExces = int((s1 + importP[seleccio[4]])*1000000)
                        propOk = int(importP[seleccio[5]]*1000000)
                        sOkey = int((s1 + importP[seleccio[5]])*1000000)

                    else:
                        s34primeras = int((importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]])*1000000)  
                        propExc = int(importP[seleccio[3]]*1000000)
                        sExces = int((s1 + importP[seleccio[3]])*1000000)
                        propOk = int(importP[seleccio[4]]*1000000)
                        sOkey = int((s1 + importP[seleccio[4]])*1000000)

                    # normalizacion 0..9 a 1..10
                    seleccioP = [0,0,0,0,0,0,0,0,0,0]
                    for kk in range(10):
                        seleccioP[kk] = seleccio[kk]+1
                    #linea  = str(aux7+1)+" "+str(aux8+1)+" "+str(aux9+1)+" "+str(seleccioP)+" "+str(sOK)+ " " + str(sEX) + " " +avisSEX+ " " + avisSOK+" lliures: "+str(lliures)
                    linea  = str(aux7+1)+" "+str(aux8+1)+" "+str(aux9+1)+" "+str(seleccioP)+" "+str(ctrlS)+" imp.sel.: "+str(sOK)                   
                    output.write(linea+"\n")
                    print(linea)
                   
                    seleccioCSV=[aux7+1,aux8+1,aux9+1,seleccioP[0],seleccioP[1],seleccioP[2],seleccioP[3],seleccioP[4],seleccioP[5],seleccioP[6],seleccioP[7],seleccioP[8],seleccioP[9],lliures,sOKcsv,s34primeras,propExc,sExces,propOk,sOkey]
                    csvwriter.writerow(seleccioCSV)
                    
                   
                    ctrl=[0,0,0,0,0,0,0,0,0,0]
                    ctrlS=[0,0,0,0,0,0,0,0,0,0]


    ##############################################################################
    #
    # ESCENARIOS 1 & 2 - NO COINCIDENTES
    # (METODO R&S - NO Seleccionadas)  
    #
    ##############################################################################
    def sim2(self):  
        print("****************************************************************")
        print("* ESCENARIOS 1 & 2 - NO COINCIDENTES")
        print("****************************************************************")
        wd = os.getcwd()
        nameFile = "RS_NOS_ALE"
        datafile = wd +"/Simulacio/"+ "/" + nameFile + ".txt"
        output = open(datafile, "w")
        # csv file
        datafile = wd +"/Simulacio/"+ "/" + nameFile + ".csv"         
        csvfile = open(datafile, 'w', newline='') 
        #csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter = csv.writer(csvfile)
        importP=[8.5,7.25,7,6.5,5.5,5.25,5,4.75,4.5,3.25]
        ctrl=[0,0,0,0,0,0,0,0,0,0]
        seleccio=[0,0,0,0,0,0,0,0,0,0]
        ctrlS=[0,0,0,0,0,0,0,0,0,0]
        for i1 in range(0,10):          
            for i2 in range(i1+1,10):
                for i3 in range(i2+1,10):

                    #propostas enquestat no seleccionades 
                    ctrl[i1]=1
                    ctrl[i2]=1
                    ctrl[i3]=1
                    seleccio[7]=i1
                    seleccio[8]=i2
                    seleccio[9]=i3

                    # propostes 3/4 seleccionades i 4/3 lliures
                    k = -1
                    sumP = 0
                    lliures=0
                    tope=0 # control que ja s'ha provocat un exces -> ja no podem seleccionar mes
                    for i4 in range(10):
                        # no esta afagat i cap a 23
                        if ctrl[i4]==0: 
                            k += 1
                            ctrl[i4]=1     
                            seleccio[k] = i4
                            if tope==0:
                                if sumP+importP[i4] <= 23:
                                    sumP += importP[i4]  
                                    ctrlS[k]=1
                                else:
                                    tope = 1 # ja tenim 3/4 sense exces
                                    lliures +=1 
                            else:
                                lliures +=1          

                    # ALEATORITZACIO (0,1,2,3,4,5,6,7,8,9)==>(2,0,1,3,4,5,6,9,7,8)
                    aux0 = seleccio[0]
                    aux1 = seleccio[1]
                    aux2 = seleccio[2]
                    aux7 = seleccio[7]
                    aux8 = seleccio[8] 
                    aux9 = seleccio[9]
                    seleccio[0]=aux2
                    seleccio[1]=aux0
                    seleccio[2]=aux1
                    seleccio[7]=aux9
                    seleccio[8]=aux7
                    seleccio[9]=aux8

                    # control resultado seleccion
                    s1 = importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]
                    if lliures==4:                
                        sOK = s1  
                        sEX = s1 + importP[seleccio[3]]
                    elif lliures==3: 
                        s1 += importP[seleccio[3]]
                        sOK = s1 
                        sEX = s1 + importP[seleccio[3]]+importP[seleccio[4]]
                  
                    avisSOK = " "
                    if sOK > 23:
                        avisSOK = "ERROR-SUM"
                    avisSEX = " "
                    if sEX <= 23:
                        avisSEX = "ERROR-EXC"

                    sOKcsv = int(sOK*1000000)
                    if lliures == 3:
                        sOkey = int((importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]+importP[seleccio[3]])*1000000)
                        propExc = int(importP[seleccio[4]]*1000000)
                        sExces = int(sOkey + importP[seleccio[4]]*1000000)     
                    else: # lliures==4
                        sOkey = int((importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]])*1000000)  
                        propExc = int(importP[seleccio[3]]*1000000)
                        sExces = int(sOkey + importP[seleccio[3]]*1000000)                        
                    

                    # normalizacion 0..9 a 1..10
                    seleccioP = [0,0,0,0,0,0,0,0,0,0]
                    for kk in range(10):
                        seleccioP[kk] = seleccio[kk]+1
                    #linea  = str(aux7+1)+" "+str(aux8+1)+" "+str(aux9+1)+" "+str(seleccioP)+" "+str(sOK)+ " " + str(sEX) + " " +avisSEX+ " " + avisSOK+" lliures: "+str(lliures)
                    linea  = str(aux7+1)+" "+str(aux8+1)+" "+str(aux9+1)+" "+str(seleccioP)+" "+str(ctrlS)+ " imp.sel.: "+str(sOK)
                    output.write(linea+"\n")
                    print(linea)
                   
                    seleccioCSV=[aux7+1,aux8+1,aux9+1,seleccioP[0],seleccioP[1],seleccioP[2],seleccioP[3],seleccioP[4],seleccioP[5],seleccioP[6],seleccioP[7],seleccioP[8],seleccioP[9],lliures,sOKcsv,sOkey,propExc,sExces]
                    csvwriter.writerow(seleccioCSV)
                    
                    ctrl=[0,0,0,0,0,0,0,0,0,0]
                    ctrlS=[0,0,0,0,0,0,0,0,0,0]

    ##############################################################################
    #
    # ESCENARIOS 3 & 4 - SI COINCIDENTES
    # (METODO IA - SI Seleccionadas)
    #
    ##############################################################################
    def sim3(self):  
        print("****************************************************************")
        print("* ESCENARIOS 3 & 4 - SI COINCIDENTES")
        print("****************************************************************")
        wd = os.getcwd()
        nameFile = "IA_SEL_ALE"
        datafile = wd +"/Simulacio/"+ "/" + nameFile + ".txt"
        output = open(datafile, "w")
        # csv file
        datafile = wd +"/Simulacio/"+ "/" + nameFile + ".csv"         
        csvfile = open(datafile, 'w', newline='') 
        #csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter = csv.writer(csvfile)
        importP=[8.5,7.25,7,6.5,5.5,5.25,5,4.75,4.5,3.25]
        ctrl=[0,0,0,0,0,0,0,0,0,0]
        seleccio=[0,0,0,0,0,0,0,0,0,0]
        ctrlS=[0,0,0,0,0,0,0,0,0,0]

         
        for i1 in range(0,10):          
            for i2 in range(i1+1,10):
                for i3 in range(i2+1,10):
                    #propostas enquestat Seleccionades 
                    ctrl[i1]=1
                    ctrl[i2]=1
                    ctrl[i3]=1
                    seleccio[0]=i1
                    seleccio[1]=i2
                    seleccio[2]=i3
                    ctrlS[0] = 1
                    ctrlS[1] = 1
                    ctrlS[2] = 1
                  
                    selcontrol = 0
                    #comprovar si 3 és la maxima selecció
                    for i4 in range(10):    
                        #if i1==0 and i2==3 and i3==9:
                        #    print("++9++ "+ str(i1)+str(i2)+str(i3)+ " " + str(i4) + " " + str(importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]+importP[i4]))
                        if ctrl[i4]==0:
                            if importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]+importP[i4]<=23:
                                ctrl[i4]=1
                                seleccio[3]=i4 
                                selcontrol = 1
                                break      

                    if  selcontrol == 0: #nomes poden haver 3 seleccionades ==>  no hi salt
                        #omplir no seleccionades
                        nonSelect = 2
                        for i5 in range(10): 
                            if ctrl[i5]==0:
                                ctrl[i5]=1
                                nonSelect += 1
                                seleccio[nonSelect]=i5 
                    else: 
                        # comprovar si 4 es la maxima seleccio 
                        for i6 in range(10):                        
                            if ctrl[i6]==0:
                                if importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]+importP[seleccio[3]]+importP[i6]<=23:
                                    ctrl[i6]=1
                                    seleccio[4]=i6 
                                    selcontrol = 2
                                    break  
                        if  selcontrol == 1: #nomes poden haver 4 seleccionades ==>  hi salt
                            # agafar la mes petita de les 3 triada i canviarla per la 4.
                            if seleccio[3] < seleccio[2]: # c(3) > c(2):  0123 a 013-2
                                seleccio[4] = seleccio[2] # omplir 5a amb més baixa 
                                seleccio[2] = seleccio[3] # fer salt
                                ctrlS[4] = 1
                            else: # no canviar pero fer salt 0123 a 012-3
                                seleccio[4] = seleccio[3] # fer salt
                                ctrlS[4] = 1
                            #else: no cal fer res la 4a es mes petita que les 3 triades
                            
                            # buscar salt        
                            for i7 in range(10):
                                if ctrl[i7]==0:
                                    ctrl[i7]=1
                                    seleccio[3]=i7  #salt non select
                                    break   

                            #if i1==0 and i2==3 and i3==9:
                            #    print("++10++ " + " " + str(seleccio) + " " + str(ctrlS))
                            
                            #omplir no seleccionades
                            nonSelect = 4
                            for i8 in range(10):
                                if ctrl[i8]==0:
                                    ctrl[i8]=1
                                    nonSelect += 1
                                    seleccio[nonSelect]=i8       
                        else: # podem seleccionar 5
                            # agafar la mes petita de les 4 triades i canviarla per la 4.
                            if seleccio[4] < seleccio[3]: #la 3 es la mes petita que la 4
                                if seleccio[3] < seleccio[2]: # la 3 es mes GRAN que les 3 triades => la 2 la mes petita                                     #01234 a 01
                                    #01234 a 0134-2
                                    seleccio[5] = seleccio[2] # omplir 5 amb més baixa (fet el salt a 4)
                                    seleccio[2] = seleccio[3]
                                    seleccio[3] = seleccio[4]                                        
                                    ctrlS[3] = 1
                                    ctrlS[5] = 1
                            # buscar salt        
                            for i7 in range(10):
                                if ctrl[i7]==0:
                                    ctrl[i7]=1
                                    seleccio[4]=i7  #salt non select
                                    break   
                            #omplir no seleccionades
                            nonSelect = 5
                            for i8 in range(10):
                                if ctrl[i8]==0:
                                    ctrl[i8]=1
                                    nonSelect += 1
                                    seleccio[nonSelect]=i8  

                                              
                    # ALEATORITZACIO (0,1,2,3,4,5,6,7,8,9)==>(2,0,1,3,4,5,6,9,7,8)
                    aux0 = seleccio[0]
                    aux1 = seleccio[1]
                    aux2 = seleccio[2]
                    aux7 = seleccio[7]
                    aux8 = seleccio[8] 
                    aux9 = seleccio[9]
                    seleccio[0]=aux2
                    seleccio[1]=aux0
                    seleccio[2]=aux1
                    seleccio[7]=aux9
                    seleccio[8]=aux7
                    seleccio[9]=aux8

                    # control resultado seleccion                   
                    sOK=0
                    sEX=0
                    avisSEX=""
                    avisSOK=""
                    if selcontrol==0: # 3 sense salt                        
                        s1 = importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]
                        sOK = s1 
                    #    sEX = s1 + importP[seleccio[4]]
                    elif selcontrol==1: # 4 amb salt
                        s1 = importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]
                        sOK = s1 + importP[seleccio[4]] # salt 3
                    else: 
                       s1 = importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]
                       sOK = s1 + importP[seleccio[3]]+ importP[seleccio[5]] #salt 4
                    
                    #3    sEX = s1 + importP[seleccio[3]]
                    #avisSOK = " "

                    # comprovar que la suma es menor o igual que 23 i que no podem agafar mes prop.
                    #if sOK > 23 or sOK+3.25 < 23:
                    #    avisSOK = "ERROR-SUM"
                    #avisSEX = " "
                    #if sEX <= 23:
                    #    avisSEX = "ERROR-EXC"

                    #sOKcsv = int(sOK*1000000)
                    #if lliures == 1:
                    #    s34primeras = int((importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]+importP[seleccio[3]])*1000000)
                    #    propExc = int(importP[seleccio[4]]*1000000)
                    #    sExces = int((s1 + importP[seleccio[4]])*1000000)
                    #    propOk = int(importP[seleccio[5]]*1000000)
                    #    sOkey = int((s1 + importP[seleccio[5]])*1000000)

                    #else:
                    #    s34primeras = int((importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]])*1000000)  
                    #    propExc = int(importP[seleccio[3]]*1000000)
                    #    sExces = int((s1 + importP[seleccio[3]])*1000000)
                    #    propOk = int(importP[seleccio[4]]*1000000)
                    #    sOkey = int((s1 + importP[seleccio[4]])*1000000)

                    # normalizacion 0..9 a 1..10
                    seleccioP = [0,0,0,0,0,0,0,0,0,0]
                    for kk in range(10):
                        seleccioP[kk] = seleccio[kk]+1
                    #linea  = str(i1+1)+" "+str(i2+1)+" "+str(i3+1)+" "+str(seleccioP)+" "+str(ctrlS)+" imp.sel.: "+str(sOK)+ " " + str(sEX) + " " +avisSEX+ " " + avisSOK+" lliures: "+str(selcontrol)
                    linea  = str(i1+1)+" "+str(i2+1)+" "+str(i3+1)+" "+str(seleccioP)+" "+str(ctrlS)+" imp.sel.: "+str(sOK)
                    output.write(linea+"\n")
                    print(linea)
                   
                    seleccioCSV=[i1+1,i2+1,i3+1,seleccioP[0],seleccioP[1],seleccioP[2],seleccioP[3],seleccioP[4],seleccioP[5],seleccioP[6],seleccioP[7],seleccioP[8],seleccioP[9],selcontrol]
                    csvwriter.writerow(seleccioCSV)
                    
                    seleccio=[0,0,0,0,0,0,0,0,0,0]
                    ctrl=[0,0,0,0,0,0,0,0,0,0]
                    ctrlS=[0,0,0,0,0,0,0,0,0,0]

    ##############################################################################
    #
    # ESCENARIOS 1 & 2 - SI COINCIDENTES    
    # (METODO R&S - SI Seleccionadas)  
    #
    ##############################################################################
    def sim4(self):  
        print("****************************************************************")
        print("* ESCENARIOS 1 & 2 - SI COINCIDENTES")
        print("****************************************************************")
        wd = os.getcwd()
        nameFile = "RS_SOL_ALE"
        datafile = wd +"/Simulacio/"+ "/" + nameFile + ".txt"
        output = open(datafile, "w")
        # csv file
        datafile = wd +"/Simulacio/"+ "/" + nameFile + ".csv"         
        csvfile = open(datafile, 'w', newline='') 
        #csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter = csv.writer(csvfile)
        importP=[8.5,7.25,7,6.5,5.5,5.25,5,4.75,4.5,3.25]
        ctrl=[0,0,0,0,0,0,0,0,0,0]
        seleccio=[0,0,0,0,0,0,0,0,0,0]
        ctrlS=[0,0,0,0,0,0,0,0,0,0]
        for i1 in range(0,10):          
            for i2 in range(i1+1,10):
                for i3 in range(i2+1,10):

                    #propostas enquestat no seleccionades 
                    ctrl[i1]=1
                    ctrl[i2]=1
                    ctrl[i3]=1
                    seleccio[0]=i1
                    seleccio[1]=i2
                    seleccio[2]=i3
                    ctrlS[0]=1
                    ctrlS[1]=1
                    ctrlS[2]=1

                    # propostes 3/4 seleccionades i 4/3 lliures
                    k = -1
                    sumP = importP[i1]+importP[i2]+importP[i3]
                    lliures=0
                    tope=0 # control que ja s'ha provocat un exces -> ja no podem seleccionar mes
                    for i4 in range(10):
                        # no esta afagat i cap a 23
                        if ctrl[i4]==0: 
                            k += 1
                            ctrl[i4]=1     
                            seleccio[3+k] = i4
                            if tope==0: # control no hi hagut cap exces
                                if sumP+importP[i4] <= 23:
                                    sumP += importP[i4]  
                                    ctrlS[3]=1 # es selecciona per combinacio 
                                else:
                                    tope = 1 # ja tenim 3/4 sense exces: s'ha produit l'exces
                                    lliures +=1 
                            else:
                                lliures +=1          

                    # ALEATORITZACIO (0,1,2,3,4,5,6,7,8,9)==>(2,0,1,3,4,5,6,9,7,8)
                    aux0 = seleccio[0]
                    aux1 = seleccio[1]
                    aux2 = seleccio[2]
                    aux7 = seleccio[7]
                    aux8 = seleccio[8] 
                    aux9 = seleccio[9]
                    seleccio[0]=aux2
                    seleccio[1]=aux0
                    seleccio[2]=aux1
                    seleccio[7]=aux9
                    seleccio[8]=aux7
                    seleccio[9]=aux8

                    # control resultado seleccion
                    s1 = importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]
                    if lliures==7:                
                        sOK = s1  
                        sEX = s1 + importP[seleccio[3]]
                    elif lliures==6: 
                        s1 += importP[seleccio[3]]
                        sOK = s1 
                        sEX = s1 + importP[seleccio[3]]+importP[seleccio[4]]
                  
                    avisSOK = " "
                    if sOK > 23:
                        avisSOK = "ERROR-SUM"
                    avisSEX = " "
                    if sEX <= 23:
                        avisSEX = "ERROR-EXC"

                    sOKcsv = int(sOK*1000000)
                    if lliures == 6:
                        sOkey = int((importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]]+importP[seleccio[3]])*1000000)
                        propExc = int(importP[seleccio[4]]*1000000)
                        sExces = int(sOkey + importP[seleccio[4]]*1000000)     
                    else: # lliures==7
                        sOkey = int((importP[seleccio[0]]+importP[seleccio[1]]+importP[seleccio[2]])*1000000)  
                        propExc = int(importP[seleccio[3]]*1000000)
                        sExces = int(sOkey + importP[seleccio[3]]*1000000)                        
                    

                    # normalizacion 0..9 a 1..10
                    seleccioP = [0,0,0,0,0,0,0,0,0,0]
                    for kk in range(10):
                        seleccioP[kk] = seleccio[kk]+1
                    #linea  = str(aux0+1)+" "+str(aux1+1)+" "+str(aux2+1)+" "+str(seleccioP)+" imp-sel: "+str(sOK)+ " " + str(sEX) + " " +avisSEX+ " " + avisSOK+" lliures: "+str(lliures) 
                    linea  = str(aux0+1)+" "+str(aux1+1)+" "+str(aux2+1)+" "+str(seleccioP)+" "+str(ctrlS) +" imp-sel: "+str(sOK)
                   
                    output.write(linea+"\n")
                    print(linea)
                   
                    seleccioCSV=[aux0+1,aux1+1,aux2+1,seleccioP[0],seleccioP[1],seleccioP[2],seleccioP[3],seleccioP[4],seleccioP[5],seleccioP[6],seleccioP[7],seleccioP[8],seleccioP[9],lliures,sOKcsv,sOkey,propExc,sExces]
                    csvwriter.writerow(seleccioCSV)
                    
                    ctrl=[0,0,0,0,0,0,0,0,0,0]
                    ctrlS=[0,0,0,0,0,0,0,0,0,0]



def main():
    problem = Simulacio()
    opcio = "0"
    opcio = input("Teclegi Opcio:\n")
    if opcio=="1":
        problem.sim1() # ESCENARIOS 3y4 - NO Coincidentes
    elif opcio=="2":
        problem.sim2() # ESCENARIOS 1y2 - NO Coincidentes
    elif opcio=="3":
        problem.sim3() # ESCENARIOS 3y4 - SI Coincidentes
    elif opcio=="4":
        problem.sim4() # ESCENARIOS 1y2 - SI Coincidentes 
    elif opcio=="99":
        problem.sim1() # TODOS LOS ESCENARIOS  &  SI/NO Coincidentes
        problem.sim2()  
        problem.sim3()
        problem.sim4()
    else: 
        print("ERROR OPCIO")

if __name__ == "__main__":
    main()
