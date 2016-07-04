import numpy as np
from astropy.table import MaskedColumn


#I want to prepare the columns of balogh_data2 in the same order as in balogh_data1 while masking values not in balogh_data2.

#match col1 of cat1 to cot2 of cat2 based on a shared ID, the result will be a column of the values of col1 arranged to be adjoined to cat2, masked potentially

#Downside: converts all masked elements to the same element, not good for columns of different dtypes returns column with len of cat2
def matchcolumn(cat1, idcol1, col1, cat2, idcol2, holdvalue):
    #These will tell me what order to arrange col1 the smaller column
    #holdvalue is the value assigned to masked parts
    valuearray = []
    maskarray = []   
    
    #cat1 could have masked entries as well, so we must take that into account, otherwise, the entries will become unmasked as they are transfered
    
    for i in range(len(cat2)):
        matchrow = np.where(cat1[idcol1]==cat2[idcol2][i])
        
        #Checking to see if the entry from cat1 is masked
        try:
            entrymask = cat1[col1][matchrow[0][0]].mask
        except (AttributeError, IndexError):
            #Two things could happen: either it is not masked because the column itself is not a masked column (has not attribute mask) or matchrow is the null array in the case there is no match. Naturally, entrymask is false.
            entrymask = False
            
        #if it is not the null array, which occurs when there is no match
        if len(matchrow[0])!=0 and entrymask==False:
            maskarray.append(0)
            valuearray.append(cat1[col1][matchrow[0][0]])
        else:
            maskarray.append(1)
            valuearray.append(holdvalue)
    
    return astropy.table.MaskedColumn(valuearray,name=col1 , mask=maskarray)

#Base Generating Functions for catalogues
#Generates all useable values in ultravista, takes zbounds as a list, same restrictions as in Muzzin et al. 2013

def genlen(gen):
    k = 0
    for i in gen:
        k+=1
    return(k)
            
            
            
    


    

            
            
        

    
    
                
    
    