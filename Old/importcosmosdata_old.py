#Importing Cosmos Data
#init imports all relevant modules

import numpy as np
import astropy.table
from astropy import units as u
from astropy.table import Column
from astropy.coordinates import SkyCoord
from astropy.coordinates import match_coordinates_sky
from astropy.coordinates.distances import Distance
from astropy import cosmology


#Initializing dict of morphology catalogues names
catalogues = {}

#Initializing dict of balogh_data1 matching indexes

#Initializing tables, adding dictionry values, making separate SkyCoord object for easy access in command module

#Cassata Morphology 1.1 in csv
#morph_cassata = astropy.table.Table.read('COSMOSdata/astropy_data/cosmos_morph_cassata_1.1.csv', format='ascii.csv')
#morph_cassata_coord = SkyCoord(ra=morph_cassata['RA']*u.degree, dec=morph_cassata['DEC']*u.degree)

#catalogues['morph_cassata'] = morph_cassata
#print ('Imported COSMOS Morphology Cassata 1.1 as morph_cassata')

##Tasca Morphology 1.1 in csv
#morph_tasca = astropy.table.Table.read('COSMOSdata/astropy_data/cosmos_morph_tasca_1.1.csv', format='ascii.csv')
#morph_tasca_coord = SkyCoord(ra=morph_tasca['RA']*u.degree, dec=morph_tasca['DEC']*u.degree)

#catalogues['morph_tasca'] = morph_tasca
#print ('Imported COSMOS Morphology Tasca 1.1 as morph_tasca')

##Zamjoski Morphology 1.0 in csv
#morph_zamojski = astropy.table.Table.read('COSMOSdata/astropy_data/cosmos_morph_zamojski_1.0.csv', format='ascii.csv')
#morph_zamojski_coord = SkyCoord(ra=morph_zamojski['RA']*u.degree, dec=morph_zamojski['DEC']*u.degree)

#catalogues['morph_zamojski'] = morph_zamojski
#print ('Imported COSMOS Morphology Zamojski 1.0 as morph_zamojski')

#Zurich Morpohology 1.0 in csv
morph_zurich = astropy.table.Table.read('COSMOSdata/astropy_data/cosmos_morph_zurich_1.0.csv', format='ascii.csv')
morph_zurich_coord = SkyCoord(ra=morph_zurich['RA']*u.degree, dec=morph_zurich['DEC']*u.degree)

catalogues['morph_zurich'] = morph_zurich
print ('Imported COSMOS Morphology Zurich 1.0 as morph_zurich')

#COSMOS Morphology 2005 in csv
#morph_2005 = astropy.table.Table.read('COSMOSdata/astropy_data/cosmos_morphology_2005.csv', format='ascii.csv')
#morph_2005_coord = SkyCoord(ra=morph_2005['RA']*u.degree, dec=morph_2005['DEC']*u.degree)

#catalogues['morph_2005'] = morph_2005
#print ('Imported COSMOS Morphology 2005 as morph_2005')

##COSMOS Photometric Redshifts in csv
#photo_z = astropy.table.Table.read('COSMOSdata/astropy_data/cosmos_zphot_mag25.csv', format='ascii.csv')
#photo_z_coord = SkyCoord(ra=photo_z['RA']*u.degree, dec=photo_z['DEC']*u.degree)

#catalogues['photo_z'] = photo_z
#print ('Imported COSMOS Photometric Redshifts as photo_z')

#Balogh Datatable 1 in txt
balogh_data1 = astropy.table.Table.read('COSMOSdata/astropy_data/balogh_datatable_2014_1.csv', format='ascii.csv')
balogh_data1_coord = SkyCoord(ra=balogh_data1['RA']*u.degree, dec=balogh_data1['DEC']*u.degree)

catalogues['balogh_data1'] = balogh_data1
print ('Imported Balogh Datatable 1 as balogh_data1')

##Balogh Datatable 2 in txt
#balogh_data2 = astropy.table.Table.read('COSMOSdata/astropy_data/balogh_datatable_2014_2.txt', fill_values=('nan', '0', -99.99, 0.0), format='ascii')

##No RA/DEC fpr Balogh Datatable 2
#catalogues['balogh_data2'] = balogh_data2
#print ('Imported Balogh Datatable 2 as balogh_data2')

#Balogh Combined Data Table in txt
balogh_data2 = astropy.table.Table.read('COSMOSdata/astropy_data/fullgroupmembertable_ascii.csv', format='ascii.csv')
balogh_data2_coord = SkyCoord(ra=balogh_data2['RA']*u.degree, dec=balogh_data2['DEC']*u.degree)

catalogues['balogh_data2'] = balogh_data2
print('Imported Balogh Datatable 2 as balogh_data2')

#Balogh GEEC Master Table in fits
geec2 = astropy.io.fits.open('COSMOSdata/astropy_data/GEEC2_master.fits')[1].data
geec2_coord = SkyCoord(ra=geec2['RA']*u.degree, dec=geec2['DEC']*u.degree)
catalogues['geec2'] = geec2
print('Imported GEEC2 Master as geec2')

#balogh Photo z catalog
#balogh_photoz = astropy.table.Table.read('COSMOSdata/astropy_data/photoz_danny_acsii.csv', format='ascii.csv')
#catalogues['balogh_photoz'] = balogh_photoz
#print('Imported Balogh Photo-z as balogh_photoz')

#Ultravista Catalogues================================================
#Main
ultravista = astropy.table.Table.read('COSMOSdata/astropy_data/UVISTA_final_v4.1_modified.csv', format='ascii.csv')
ultravista_coord = SkyCoord(ra=ultravista['RA']*u.degree, dec=ultravista['DEC']*u.degree)

catalogues['ultravista'] = ultravista
print('Imported Ultravista Final v.4.1 MODIFIED as ultravista')

#U-V & V-J============================================================
#ultravista_UVJ = astropy.table.Table.read('COSMOSdata/astropy_data/UVISTA_final_v4.1.UVJ.csv', fill_values=('nan', '-999999'), format='ascii.csv')

##No RA/DEC but is indexed the same as Ultravista(main)
#catalogues['ultravista_UVJ'] = ultravista_UVJ
#print('Imported Ultravista Final v.4.1 U-V & V-J as ultravista_UVJ')

#Main Catalogue Uncut===============================================
ultravista_Main = astropy.table.Table.read('COSMOSdata/astropy_data/UVISTA_Main.csv', format='ascii.csv')
ultravista_Main_coord = SkyCoord(ra=ultravista_Main['RA']*u.degree, dec=ultravista_Main['DEC']*u.degree)

catalogues['ultravista_Main'] = ultravista_Main
print('Imported ultravista_Main Final v.4.1 MODIFIED as ultravista_Main')

#Griffith COSMOS catalogue=================================================
griffith = astropy.io.fits.open('COSMOSdata/astropy_data/griffith_cosmos_2.0.fits.gz')[1].data
catalogues['griffith'] = griffith
print('Imported Griffiths COSMOS 2.0 as griffith')

#------------------------------------------------------------------
#names of catalogues that I want 
match1_catalogues = ['balogh_data1', 'balogh_data2', 'ultravista', 'morph_zurich']
match2_catalogues = [['ultravista', 'griffith'], ['morph_zurich', 'griffith', 'ultravista'], ['morph_zurich', 'griffith'], ['griffith']]

#name1 is matching catalogue, name2 represents catalogues that are matched to name1
for name1 in match1_catalogues:
    gen = (name2 for name2 in match2_catalogues[match1_catalogues.index(name1)])
    for name2 in gen:
        tempcoord1 = SkyCoord(ra=catalogues[name1]['RA']*u.degree, dec=catalogues[name1]['DEC']*u.degree)
        tempcoord2 = SkyCoord(ra=catalogues[name2]['RA']*u.degree, dec=catalogues[name2]['DEC']*u.degree)
        tempmatch = match_coordinates_sky(tempcoord1, tempcoord2)
        
        #1(TRUE) it is bad match, 0 (FALSE) is good match
        tempflag = np.array(tempmatch[1]>=1.0*u.arcsec)
        
        #for d2d in tempmatch[1]:
            #if d2d >= 1.0*u.arcsec:
                #tempflag = np.append(tempflag, 0)
            #else:
                #tempflag = np.append(tempflag, 1)
               
        catalogues[name1].add_column(Column(name=name2+'_match', data=tempmatch[0]))
        catalogues[name1].add_column(Column(name=name2+'_d2d', data=tempmatch[1].to(u.arcsec)))
        catalogues[name1].add_column(Column(name=name2+'_flag', data=tempflag))
        
        print()
        print('Matched '+name2+' to '+name1)
        print(name1 + ' and ' + name2 + ' have', (tempflag==0).sum(), 'good matches (d2d < 1.0 arcsec) out of ', len(catalogues[name1]), ' entries in ' + name1)
        print('Index, d2d and Flag columns added to ' + name1)

#Catalogue Functions===================================================
#def ultravistagen (zlow=None, zupp=None):
    #if zlow is None and zupp is None:
        #for i in range(len(ultravista)):
            #if ultravista['star'][i] != 1 and\
               #ultravista['K_flag'][i] <= 4 and\
               #ultravista['contamination'][i] != 1 and\
               #ultravista['nan_contam'][i] <= 3 and\
               #ultravista['Ks_tot'][i] < 23.4:
                #yield (i)
    #else:
        #for i in range(len(ultravista)):
            #if ultravista['star'][i] != 1 and\
               #ultravista['K_flag'][i] <= 4 and\
               #ultravista['contamination'][i] != 1 and\
               #ultravista['nan_contam'][i] <= 3 and\
               #ultravista['Ks_tot'][i] < 23.4 and\
               #ultravista['zp'][i]>=zlow and\
               #ultravista['zp'][i]<=zupp:
                #yield (i)
                
#def UminusVmag(i):
    #return -2.5*np.log10(ultravista_UVJ['L153'][i]/ultravista_UVJ['L155'][i])
        
#def VminusJmag(i):
    #return -2.5*np.log10(ultravista_UVJ['L155'][i]/ultravista_UVJ['L161'][i])    

#takes the catalogue into name  
#catname is the name of the catalogue in string format, columns is a list of column names to be used, 
#Flag, if True then BAD, if False then GOOD
#def flag(catname, columns, i):
    #cat = catalogues[catname]
    ##General Bad Indication
    #if catname == 'balogh_data1' or catname == 'balogh_data2' or catname =='balogh_photoz':
        ##No General Indicators
        #for col in columns:
            ##We want it to return true if any column has this flag so let us check for the flag and not the absence of the flag
            #if cat[col][i] == -99.99 or cat[col][i] == '-':
                #return True
        ##ALL the columns are good values    
        #return False    
            
    #elif catname == 'ultravista':
        ##General Indicators
        ##Since we only computed Class for those that were good objects in the catalogue as defined in Muzzin et al 2013, we can simply refer to the class column, 0 is BAD Value, 1 is GOOD value 
        #if cat['USE2'][i] == 0:
            ##No Specific column flags yet
            #return True
        #else:
            #for col in columns:
                #if cat[col][i] == -999.999:
                    #return True
            #return False
        
    #elif catname == 'morph_zurich':
        ##Using their Stellarity Column
        #if cat['JUNKFLAG'][i] != 0 or cat['STELLARITY'][i] != 0 or cat['ACS_CLEAN'][i]!= 1:
            ##It is not a good object
            #return True
        #else:
            #for col in columns:
                ##-999999 means no measurement
                #if cat[col][i] == -999999.0:
                    #return True
                    ##Specifically for individual column Flags, right now we will only worry about Petrosian Flag
                ##elif col == 'RPET' and cat['FLAGRPET'][i] != 0:
                    ##Multiple Radii Detected, Noisy
                    ##return True
            #return False 
    #elif catname == 'griffith':
        #for col in columns:
            #if cat[col][i] == -999.0:
                #return True
        #return False    
    #else: 
        #raise NameError(catname+' is not covered by the function flag')
    
#Flag Column Function
def flagcolumn(catname, columns):
    cat = catalogues[catname]
    tempflagcol = np.zeros(len(cat))
    #General Bad Indication
    #tempflagcol indicates BAD VALUES = 1
    if catname == 'balogh_data2':
        tempflagcol = (cat['groupdist'] >= cat['R200'])
        for col in columns:
            #We want it to return true if any column has this flag so let us check for the flag and not the absence of the flag
            tempflagcol += (cat[col] == -99.99) + (cat[col] == '-')
        #ALL the columns are good values  
        
    elif catname == 'balogh_data1' or catname == 'balogh_photoz':
        for col in columns:
            #We want it to return true if any column has this flag so let us check for the flag and not the absence of the flag
            tempflagcol += (cat[col] == -99.99) + (cat[col] == '-')
        #ALL the columns are good values          
            
    elif catname == 'ultravista':
        #General Indicators
        #Since we only computed Class for those that were good objects in the catalogue as defined in Muzzin et al 2013, we can simply refer to the class column, 0 is BAD Value, 1 is GOOD value 
        tempflagcol = (cat['USE2'] == 0)
        for col in columns:
            tempflagcol += (cat[col] == -999.999)
        
    elif catname == 'morph_zurich':
        #Using their Stellarity Column
        tempflagcol = (cat['JUNKFLAG'] != 0) + (cat['STELLARITY'] != 0) + (cat['ACS_CLEAN'] != 1)
            #It is not a good object
        for col in columns:
            #-999999 means no measurement
            tempflagcol += (cat[col] == -999999.0)
                #Specifically for individual column Flags, right now we will only worry about Petrosian Flag
            #elif col == 'RPET' and cat['FLAGRPET'][i] != 0:
                #Multiple Radii Detected, Noisy
                    #return True
                    
    elif catname == 'griffith':
        #Remember, addition is 'or', multiplication is 'and'
        tempflagcol = (cat['FLAG_GALFIT_HI']==1)+(cat['MU_HI'] > 26.0) * (cat['RE_GALFIT_HI'] * 0.05 > 0.03)
        for col in columns:
            tempflagcol += (cat[col] == -999.0) + (cat[col] == np.inf)
            
    else: 
        raise NameError(catname+' is not covered by the function flagcolumn')
    return tempflagcol
    
#generates the entries for iteration   
#takes catname, matcatname as strings in catalogues, takes columns 
#zcol is the name of the redshift column in the catalogue, zrange = [zlower, zupper]
def genentries(catname, columns, matchcatname=None, matchcolumns=None,zcol=None, zrange=None):
    cat = catalogues[catname]
    #tempflagcol 1 is BAD value, 0 is GOOD value
    if matchcatname is None or matchcatname == catname:
        #If no matching name is specified or if it's matching to itself. This feature is implemented so we can easily compare results between different catalogues while keeping the same code structure
        if zrange is None or zrange == []:
            #zrange, matcatname do NOT exist
            tempflagcol = flagcolumn(catname, columns)
            for i in range(len(cat)):
                if tempflagcol[i] == False:
                #They are good values!
                    yield i
        else:    
            #zrange is SOME Object, matchcatname does NOT exist
            #REMEMBER tempflag represents the BAD values, it is the negation of all our DESIRED conditional statements
            tempflagcol = flagcolumn(catname, columns)+(cat[zcol] < zrange[0])+(cat[zcol] > zrange[1])
            for i in range(len(cat)):
                #They are in between the zrange
                if tempflagcol[i] == False:
                    yield i
    else:  
        tempmatchindexcol = np.array(cat[matchcatname+'_match'])
        if zrange is None or zrange == []:
        #matchcatname is SOME Object, zrange does NOT exist
        #Adding the match flag and the match cat flag
            tempflagcol = flagcolumn(catname, columns)+(cat[matchcatname+'_flag'])
            tempmatchflagcol = flagcolumn(matchcatname, matchcolumns)
            for i in range(len(cat)):
            #check if it is a good match and if the match columns are good
                if tempflagcol[i] == False and\
                   tempmatchflagcol[tempmatchindexcol[i]] == False:
                    yield i
        else:    
        #zrange, matcatname are SOME objects
            tempflagcol = flagcolumn(catname, columns)+(cat[zcol] < zrange[0])+(cat[zcol] > zrange[1])+(cat[matchcatname+'_flag'])
            tempmatchflagcol = flagcolumn(matchcatname, matchcolumns)
            for i in range(len(cat)):
            #check if it is a good match and if the match columns are good
                if tempflagcol[i] == False and\
                   tempmatchflagcol[tempmatchindexcol[i]] == False:
                    yield i  
                    
#generates all the indices for a given genentries
def genindex(catname, columns, matchcatname=None, matchcolumns=None,zcol=None, zrange=None):
    cat = catalogues[catname]
    index = np.arange(len(cat))
    #tempflagcol 1 is BAD value, 0 is GOOD value
    if matchcatname is None or matchcatname == catname:
        #If no matching name is specified or if it's matching to itself. This feature is implemented so we can easily compare results between different catalogues while keeping the same code structure
        if zrange is None or zrange == []:
            #zrange, matcatname do NOT exist
            tempflagcol = flagcolumn(catname, columns)
            
        else:    
            #zrange is SOME Object, matchcatname does NOT exist
            #REMEMBER tempflag represents the BAD values, it is the negation of all our DESIRED conditional statements
            tempflagcol = flagcolumn(catname, columns)+(cat[zcol] < zrange[0])+(cat[zcol] > zrange[1])
            
    else:  
        tempmatchindexcol = np.array(cat[matchcatname+'_match'])
        if zrange is None or zrange == []:
        #matchcatname is SOME Object, zrange does NOT exist
        #Adding the match flag and the match cat flag
            tempflagcol = flagcolumn(catname, columns)+(cat[matchcatname+'_flag'])
            tempmatchflagcol = flagcolumn(matchcatname, matchcolumns)
            tempflagcol = tempflagcol + tempmatchflagcol[tempmatchindexcol]
    
        else:    
        #zrange, matcatname are SOME objects
            tempflagcol = flagcolumn(catname, columns)+(cat[zcol] < zrange[0])+(cat[zcol] > zrange[1])+(cat[matchcatname+'_flag'])
            tempmatchflagcol = flagcolumn(matchcatname, matchcolumns)
            tempflagcol = tempflagcol + tempmatchflagcol[tempmatchindexcol]
            
    return tempflagcol == False
                    
def genlen(gen):
    k=0
    for i in gen:
        k+=1
    return k    

def goodvalues(catname, columns=None): 
    if columns is None:
        count = genlen(genentries(catname, []))
    else:
        count = genlen(genentries(catname, columns))
    print ('There are ', count, ' good values out of ', len(catalogues[catname]))  

