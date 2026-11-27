# Onset / end actions of each alert
A_ON = {
 'CONG':  [('env',{'te':-20.0})],
 'DELTA': [('env',{'te':-5.0})],
 'CO2':   [('env',{'co2':1500.0})],
 'VOC':   [('voc',500)],
 'PDR':   [('env',{'ue':99.0,'te':19.5})],
 'UMIDA': [('env',{'ui':80.0})],
 'UMIDS': [('env',{'ui':30.0,'ue':30.0})],
 'BO':    [('online',False)],
}
A_OFF = {
 'CONG':  [('env',{'te':10.0})],
 'DELTA': [('env',{'te':10.0})],
 'CO2':   [('env',{'co2':500.0})],
 'VOC':   [('voc',50)],
 'PDR':   [('env',{'ue':30.0,'te':10.0})],
 'UMIDA': [('env',{'ui':50.0})],
 'UMIDS': [('env',{'ui':50.0})],
 'BO':    [('online',True)],
}
SW = {'CO2':'input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc','VOC':'input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc',
      'PDR':'input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr','UMIDA':'input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita',
      'UMIDS':'input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita'}
def free_setup(mode):
    hm = ('Novembre','Febbraio') if mode=='H' else ('Marzo','Maggio')
    cm = ('Giugno','Agosto') if mode=='H' else ('Dicembre','Febbraio')
    sw = 'freeheating' if mode=='H' else 'freecooling'
    return [('select','input_select.vmc_master_mese_1_fascia_freeheating',hm[0]),('select','input_select.vmc_master_mese_2_fascia_freeheating',hm[1]),
            ('select','input_select.vmc_master_mese_1_fascia_freecooling',cm[0]),('select','input_select.vmc_master_mese_2_fascia_freecooling',cm[1]),
            ('switch',f'input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_{sw}',True),
            ('env',{'te':22.0 if mode=='H' else 10.0})]
FREE_UNFAV = {'H':[('env',{'te':10.0})], 'C':[('env',{'te':25.0})]}
FREE_FAV = {'H':[('env',{'te':22.0})], 'C':[('env',{'te':10.0})]}
