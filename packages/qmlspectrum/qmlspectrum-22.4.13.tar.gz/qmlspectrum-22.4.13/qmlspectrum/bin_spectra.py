import numpy as np
import qmlspectrum
import pandas as pd
'''
A module containing functions for various types of binning.
'''
def bin_spectra_uniform(spec_path, read_P, file_P, wavelength_min, wavelength_max, N_bin):
    '''
    A function for binning spectra using a uniform bin width
    '''
    spec_files=qmlspectrum.read_files(spec_path)
    if read_P:
        dlambda = (wavelength_max - wavelength_min)/N_bin
        lam=[]
        for i_bin in range(N_bin):
            lam.append( (i_bin+1.0/2.0)*dlambda )
        Int_lam = np.load(file_P)

    else:
        print('binning spectra')

        dlambda = (wavelength_max - wavelength_min)/N_bin
        lambda_min=[]
        lambda_max=[]
        lam=[]
        for i_bin in range(N_bin):
            lambda_min.append( (i_bin)*dlambda )
            lambda_max.append( (i_bin+1)*dlambda )
            lam.append( (i_bin+1.0/2.0)*dlambda )
        N_file=len(spec_files)
        i_file=0
        Int_lam=np.zeros([N_file,N_bin])
        for spec_csv in spec_files:
            if np.mod(i_file, 100) == 0:
                print(i_file,' out of ', N_file, ' done')
            spec_data=pd.read_csv(spec_path+'/'+spec_csv, names=['wavelength_nm', 'osc_strength'])
            wavelength=np.array(spec_data['wavelength_nm'])
            f=np.array(spec_data['osc_strength'])
            for i_bin in range(N_bin):
                sum_f=0.0
                for i_state in range(f.shape[0]):
                    if wavelength[i_state] > lambda_min[i_bin] and wavelength[i_state] <= lambda_max[i_bin]:
                        sum_f=sum_f+f[i_state]
                Int_lam[i_file,i_bin]=sum_f
            i_file=i_file+1
        np.save(file_P, Int_lam)
        print('data saved in ', file_P)

    return lam, Int_lam
