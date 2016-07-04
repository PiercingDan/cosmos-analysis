import numpy as np
import kcorrect as kc
import astropy.table


kc.load_templates()
kc.load_filters(f='myfilter.dat')

catalogues={}

#=======================================================================
balogh_data2 = astropy.table.Table.read('/home/dannyluo/cosmosdata/balogh_data2bands.csv', format='ascii.csv')

catalogues['balogh_data2'] = balogh_data2
print('Imported Balogh Datatable 2 as balogh_data2')

#=======================================================================
ultravista = astropy.table.Table.read('/home/dannyluo/cosmosdata/UVISTA_final_v4.1_modified.csv', format='ascii.csv')

catalogues['ultravista'] = ultravista
print('Imported Ultravista Final v.4.1 MODIFIED as ultravista')

#=======================================================================
ultravista_main = astropy.table.Table.read('/home/dannyluo/cosmosdata/UVISTA_Main.csv', format='ascii.csv')

catalogues['ultravista_main'] = ultravista_main
print('Imported Ultravista Main as ultravista_main')
#=======================================================================

bands = ['ch1', 'J', 'V', 'zp']
bd = np.empty((len(balogh_data2), len(bands)))
bdivar = np.empty((len(balogh_data2), len(bands)))
uv = np.empty((len(ultravista_main), len(bands)))
uvivar = np.empty((len(ultravista_main), len(bands)))

bd = np.array([ultravista_main[band][balogh_data2['ultravista_match']].data for band in bands]).T
bdivar = (np.array([ultravista_main['e'+band][balogh_data2['ultravista_match']].data for band in bands]).T)**(-2)

uv = np.array([ultravista_main[band].data for band in bands]).T
uvivar = np.array([ultravista_main['e'+band].data for band in bands]).T**(-2)

#uv = []
#this way to ensure no decimal funny business
for i in range(len(bands)):
 #uv.append(ultravista_main[bands[i]].data)
 uv[:, i] = ultravista_main[bands[i]].data
 uvivar[:, i] = (ultravista_main['e'+bands[i]].data)**(-2)
 bd[:, i] = ultravista_main[bands[i]][balogh_data2['ultravista_match']].data
 bdivar[:, i] = (ultravista_main['e'+bands[i]][balogh_data2['ultravista_match']].data)**(-2)

bdzp = balogh_data2['zp'].data
bdzs = balogh_data2['zs'].data
#Not the same as 'zp' in ultravista_main, which is the band flux
uvzp = ultravista['zp'].data
#balogh_data2 photometric kcorrection
bdpkc = np.zeros((len(balogh_data2), len(bands)))
#balogh_data2 spectroscopic kcorrection
bdskc = np.zeros((len(balogh_data2), len(bands))) 
#ultravista kcorrection
uvkc = np.zeros((len(ultravista), len(bands)))

#performing kcorrection------------------------------------------------------
for i in range(len(bdzp)):
 coeffs = kc.fit_nonneg(bdzp[i], bd[i], bdivar[i])
 rm = kc.reconstruct_maggies(coeffs)
 rm0 = kc.reconstruct_maggies(coeffs, redshift=0.9)
 kcorrection = -2.5*np.log10(rm[1:]/rm0[1:])
 bdpkc[i] = kcorrection

for i in range(len(bdzs)):
 coeffs = kc.fit_nonneg(bdzs[i], bd[i], bdivar[i])
 rm = kc.reconstruct_maggies(coeffs)
 rm0 = kc.reconstruct_maggies(coeffs, redshift=0.9)
 kcorrection = -2.5*np.log10(rm[1:]/rm0[1:])
 bdskc[i] = kcorrection

for i in range(len(uvzp)):
 coeffs = kc.fit_nonneg(uvzp[i], uv[i], uvivar[i])
 rm = kc.reconstruct_maggies(coeffs)
 rm0 = kc.reconstruct_maggies(coeffs, redshift=0.9)
 kcorrection = -2.5*np.log10(rm[1:]/rm0[1:])
 uvkc[i] = kcorrection

#General Bad Flag, If at least one filter flux is -99.99
uv_flag = ((uv==-9.9999e+1).sum(axis=1)!=0)
#Same for balogh_data2
bdzp_flag = ((bd==-9.9999e+1).sum(axis=1)!=0)
#But include, for spectrocospic data, null zs values
bdzs_flag = bdzp_flag+(bdzs==-99.99)

#Setting null entries
uvkc[uv_flag] = -99.99
bdpkc[bdzp_flag] = -99.99
bdskc[bdzs_flag] = -99.99

print('There are ', (uv_flag==0).sum(), ' good entries out of ', len(ultravista_main), ' for ultravista')
print('There are ', (bdzp_flag==0).sum(), ' good entries out of ', len(balogh_data2),' for balogh_data photometric redshifts')
print('There are ', (bdzs_flag==0).sum(), ' good entries out of ', len(balogh_data2), ' for ultravista spectroscopic redshifts')

#Writing Data---------------------------------------------------------------
astropy.table.Table(bdpkc, names=['kc_'+band for band in bands]).write('balogh_data2_kczp', format='ascii')
astropy.table.Table(bdskc, names=['kc_'+band for band in bands]).write('balogh_data2_kczs', format='ascii')
astropy.table.Table(uvkc, names=['kc_'+band for band in bands]).write('ultravista_kczp', format='ascii')
                    







