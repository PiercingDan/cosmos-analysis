pro calc_kcorr
    showplots=0
    
;    alldata=mrdfits("/home/mbalogh/projects/CNOC2/hiz/cats/Final_nodups_10A.fits",1)
;    alldata=mrdfits("/home/mbalogh/projects/CNOC2/hiz/cats/Final_nodups_11A.fits",1)
;    alldata=mrdfits("/home/mbalogh/projects/CNOC2/hiz/cats/Final_nodups_all.fits",1)
    alldata=mrdfits("/home/mbalogh/projects/CNOC2/hiz/cats/withmips.fits",1)
;    alldata=mrdfits("/home/mbalogh/projects/CNOC2/hiz/cats/zCOSMOS/photoz_zml_vers1.8_250909.fits",1)
;redshift
;    alldata.z
;    or alldata.photoz
; Read magnitudes
;    alldata.FUV,NUV,MAG_U,B,V,R,I,Z,J,K,IC,IA,I1,I2,I3,I4
;    Aug 16, 2012: finally checking limiting mags but plotting number
;    counts for each filter.
;    FUV: 26.5
;    NUV: 25
;    U: 26
;    B: 26
;    V: 26.5
;    G: 26
;    R: 26.5 
;    I: 26
;    Z: 26
;    J: 24
;    K: 24
;    IC: 24
;    I1: 23.5
;    I2: 23.5
;    I3: 22.5
;    I4: 22.5
;
; Read in flags
;    N/A
; Read in errors
;    alldata.DMAG_FUV etc.

    mags=[transpose(alldata.FUV),transpose(alldata.NUV),transpose(alldata.MAG_U),transpose(alldata.MAG_B),transpose(alldata.MAG_V),transpose(alldata.MAG_G),transpose(alldata.MAG_R),transpose(alldata.MAG_I),transpose(alldata.MAG_Z),transpose(alldata.MAG_J),transpose(alldata.MAG_K),transpose(alldata.MAG_IC),transpose(alldata.MAG_I1),transpose(alldata.MAG_I2),transpose(alldata.MAG_I3),transpose(alldata.MAG_I4)]
    mags_err=[transpose(alldata.DMAG_FUV),transpose(alldata.DMAG_NUV),transpose(alldata.DMAG_U),transpose(alldata.DMAG_B),transpose(alldata.DMAG_V),transpose(alldata.DMAG_G),transpose(alldata.DMAG_R),transpose(alldata.DMAG_I),transpose(alldata.DMAG_Z),transpose(alldata.DMAG_J),transpose(alldata.DMAG_K),transpose(alldata.DMAG_IC),transpose(alldata.DMAG_I1),transpose(alldata.DMAG_I2),transpose(alldata.DMAG_I3),transpose(alldata.DMAG_I4)]
    redshift=transpose(alldata.z)
;    redshift=transpose(alldata.photoz)
;    minerrs=[.05, .02, 0.02, 0.03, 0.2, .02, 0.02, 0.02, 0.03, .05]
    filterlist=['galex1500.par','galex2500.par','u_cfht.par','B_subaru.par','V_subaru.par','g_subaru.par','r_subaru.par','i_subaru.par','z_subaru.par','J_wfcam.par','wircam_Ks.par','i_cfht.par','irac_ch1.par','irac_ch2.par','irac_ch3.par','irac_ch4.par']
;     rm galex1500.par ; cat cosmosheader > galex1500.par ; awk 'NR>1 {print "KFILTER",$1,$2}' zCOSMOS_filters/galex1500.res >> galex1500.par
    extrafilters=filterlist
    badmags=where(mags lt 0 or mags gt 30) 
    maglim=[26.5,25,26,26,26.5,26,26.5,26,26,24,24,24,23.5,23.5,23.5,23.5]
    mags_new=mags
    mags_err_new=mags_err
    mags_new[badmags]=0
    mags_err_new[badmags]=9999
    for i=0L, n_elements(filterlist)-1L do begin
        nondetect=where(mags[i,*] gt maglim[i])
;        mags_new[i,nondetect]=0
        mags_err_new[i,nondetect]=9999
    end
    mags_err_new[where(mags_err_new lt 0.001)]=0.001
    goodmags=mags_err_new*0
    goodmags[where(mags_err_new lt 1000)]=1
    dof=total(goodmags,1)
;    obslambda=10000*[megalambdas,tklambdas,2.22]
;    width=10*[megawidth,tkwidth,Kwidth]
;    perHztoperA=2.998e18/(obslambda)^2
    if (showplots eq 0) then begin
;        openw, outunit, "/home/mbalogh/projects/CNOC2/hiz/cats/zCOSMOS/photoz_zml_vers1.8_250909_kcorr_0.9", /GET_LUN
;        openw, outunit, "/home/mbalogh/projects/CNOC2/hiz/cats/kcorr11A_0.9", /GET_LUN
	openw, outunit, "/home/mbalogh/projects/CNOC2/hiz/cats/kcorr_0.0_all", /GET_LUN
        band_shift=0.0
        kcorrect, mags_new,mags_err_new,redshift,kcorrect, minerrors=minerrs,/magnitude, /stddev, filterlist=filterlist,chi2=chi2,band_shift=band_shift,vmatrix=vmatrix,lambda=lambda,coeffs=coeffs,rmaggies=rmaggies
        redchi2=chi2/dof
        redchi2m1=chi2/(dof-1)
        badchisq=where(dof lt 4 or redshift le 0.0001,count)
        if count ne 0 then redchi2[badchisq]=99
        if count ne 0 then redchi2m1[badchisq]=99
        printf, outunit, format='(19(f10.3,1x))',[redshift,kcorrect,transpose(redchi2),transpose(redchi2m1)]
        close, outunit
; additional script to output k-corrected magnitudes
	k_projection_table, out_rmatrix, vmatrix, lambda, out_zvals, extrafilters, zmin=0.,zmax=3.,nz=2000
	k_reconstruct_maggies,coeffs,replicate(band_shift,n_elements(redshift)),reconstruct_maggies,rmatrix=out_rmatrix,zvals=out_zvals
	reconstruct_maggies=reconstruct_maggies/(1.+band_shift)
	obands=lindgen(n_elements(extrafilters))#replicate(1L, n_elements(redshift))
; Kcorrect to the closest band
    lambda_in=k_lambda_eff(filterlist=filterlist)
    lambda_out=k_lambda_eff(filterlist=extrafilters, band_shift=band_shift)
    for i=0L, n_elements(redshift)-1L do begin
        for j=0L, n_elements(lambda_out)-1L do begin
            dmin=min(abs(lambda_in/(1.+redshift[i])-lambda_out[j]), imin)
            obands[j, i]= imin
        endfor
    endfor
;
	kcorrect_extra=fltarr(n_elements(extrafilters), n_elements(redshift))
	for i=0L, n_elements(redshift)-1L do $
	for j=0L, n_elements(extrafilters)-1L do $
	kcorrect_extra[j,i]=reconstruct_maggies[j,i]/ rmaggies[obands[j,i],i]
	kcorrect_extra=2.5*alog10(kcorrect_extra)
	mags_extra_mod=fltarr(n_elements(extrafilters),n_elements(redshift))
	mags_extra=fltarr(n_elements(extrafilters),n_elements(redshift))
	for i=0L, n_elements(extrafilters)-1L do begin
          mags_extra_mod[i,*]=-2.5*alog10(reconstruct_maggies[i,*])
          for j=0L, n_elements(redshift)-1L do begin
              mags_extra[i,j]=mags_new[obands[i,j],j]-kcorrect_extra[i,j]
          endfor
          endfor
	openw, outunit, "/home/mbalogh/projects/CNOC2/hiz/cats/extramags_kcorr_v3.dat", /GET_LUN
;        printf, outunit, format='(33(f10.3,1x))',[redshift,kcorrect_extra,obands]
;        printf, outunit, format='(33(f10.3,1x))',[redshift,mags_extra,obands]
        printf, outunit, format='(33(f10.3,1x))',[redshift,mags_extra,mags_new]
	close, outunit	 
	close, /ALL
	openw, outunit, "/home/mbalogh/projects/CNOC2/hiz/cats/extramags_v3.dat", /GET_LUN
        printf, outunit, format='(17(f10.3,1x))',[redshift,mags_extra_mod]
	close, outunit	 
	close, /ALL
; end addition
    endif else begin
        for i=14L,n_elements(redshift)-1 do begin
            if (redshift[i] gt 0. and dof[i] gt 3) then begin
                print, i
                print, redshift[i]
                print, obslambda
                print, [mags_new[*,i]]
                print, [mags_err_new[*,i]]
                kcorrect, mags_new[*,i],mags_err_new[*,i],redshift[i],kcorrect, minerrors=minerrs,/magnitude, /stddev, filterlist=filterlist,chi2=chi2,band_shift=0.0,vmatrix=vmatrix,lambda=lambda,coeffs=coeffs,rmatrix=rmatrix,zvals=zvals
                plot, lambda, vmatrix#coeffs, xra=[2000., 12000.]  
                redchi2=chi2/dof[i]
                redchi2m1=chi2/(dof[i]-1)
                print, [dof[i],redchi2,redchi2m1]
                yy=3.631e-20*perHztoperA*10.^(-0.4*mags_new[*,i])
                dy=yy*0.4*alog(10.)*sqrt(mags_err_new[*,i]*mags_err_new[*,i]+minerrs*minerrs)
                plot, lambda*(1.+redshift[i]), vmatrix#coeffs/(1.+redshift[i]), xra=[3000., 25000.], psym=-3, xstyle=1
                oplot, obslambda, yy,psym=4
                oploterrx, obslambda, yy, width/2
                oploterr, obslambda, yy, dy
                read, junk
                xx1=temporary(vmatrix)
                xx2=temporary(lambda)
                xx3=temporary(coeffs)
                xx4=temporary(zvals)
            endif
        endfor
    endelse

end 

