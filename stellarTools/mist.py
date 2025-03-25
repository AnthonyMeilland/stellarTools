# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 18:38:54 2025

@author: ame
"""
from  pathlib import Path 
import numpy as np
from tqdm import tqdm

dir0 = Path(__file__).parent
dirmodel=dir0 / "MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS"


def _read(file):
    f=open(file)
    data=f.read()
    f.close()
    data=[di.split() for di in data.split("\n")][1:]
    colnames=data[10][1:]
    data=np.array(data[11:-1],dtype=float)
    return colnames,data

_phaseName=['PMS','MS','SubG','RGB','CHeB', 'EAGB','TPAGB', 'postAGB','BS','BHB','WR']

_phaseNameLong=['Pre Main Sequence',
                'Main Sequence',
                'Sub Giant',
                'Red Giant Branch',
                'Red horizontal branch / red clump (core He burning)',
                'Early asymptotic giant branch',
                'Thermally-pulsating AGB (composition sets C-rich vs. O-rich)', 
                'Post-AGB',
                'Blue stragglers',
                'Blue horizontal branch',
                'Wolf-Rayet (composition sets WC vs. WN)']



class mist:
    def __init__(self):
        filenames=list(dirmodel.glob("*.eep"))
        mass=[]
        datas=[]
        print(f"Loading MIST database {dirmodel.name}")
        for i in tqdm(range(len(filenames))):
            colnames,datai=_read(filenames[i])
            
            datas.append(datai)
            mass.append(datai[0,colnames.index("star_mass")])
        self.grid_mass = np.array(mass)
        self.grid = datas
        self.colnames = colnames
        
    @staticmethod
    def phaseName(phases,long=False):
        phases=np.array(phases)
        if long :
            phaseName=_phaseNameLong    
        else:
            
            phaseName=_phaseName    
        if len(phases.shape)==0:
            return phaseName[int(phases)+1]
        return [phaseName[phasesi+1] for phasesi in np.array(phases).astype(int)]
    
    def evolutionnaryTrack(self,M,log=False):
        
        idx = np.argmin((self.grid_mass-M)<0)-1
        p=(M-self.grid_mass[idx])/(self.grid_mass[idx+1]-self.grid_mass[idx])

        
        age1=np.array(self.grid[idx][:,self.colnames.index("star_age")])
        log_lum1=np.array(self.grid[idx][:,self.colnames.index("log_L")])
        log_teff1=np.array(self.grid[idx][:,self.colnames.index("log_Teff")])
        log_radius1=np.array(self.grid[idx][:,self.colnames.index("log_R")])
        phase1 = np.array(self.grid[idx][:,self.colnames.index("phase")])
     
        age2=np.array(self.grid[idx+1][:,self.colnames.index("star_age")])
        log_lum2=np.array(self.grid[idx+1][:,self.colnames.index("log_L")])
        log_teff2=np.array(self.grid[idx+1][:,self.colnames.index("log_Teff")])
        log_radius2=np.array(self.grid[idx+1][:,self.colnames.index("log_R")])
        phase2 = np.array(self.grid[idx+1][:,self.colnames.index("phase")])
     
        age=np.sort(np.append(age1,age2))
        
        log_lum1b=np.interp(age,age1,log_lum1)
        log_teff1b=np.interp(age,age1,log_teff1)
        log_radius1b=np.interp(age,age1, log_radius1)
        phase1b=np.interp(age,age1,phase1)
        
        log_lum2b=np.interp(age,age2,log_lum2)
        log_teff2b=np.interp(age,age2,log_teff2)
        log_radius2b=np.interp(age,age2, log_radius2)
        phase2b=np.interp(age,age2,phase2)
        
        log_lum= (1-p)*log_lum1b+p*log_lum2b
        log_teff= (1-p)*log_teff1b+p*log_teff2b
        log_radius= (1-p)*log_radius1b+p*log_radius2b
        phase= np.round((1-p)*phase1b+p*phase2b)
        
        if log==True:
            return age,log_teff,log_lum,log_radius,phase
        else:
            return age,10**log_teff,10**log_lum,10**log_radius,phase


