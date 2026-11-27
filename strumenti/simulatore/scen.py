import asyncio, vclock, simlib, fakevmc
from simlib import *
VMC = fakevmc.VMC
SPEED_SVC = {0:'vmc_master_velocita_0',1:'vmc_master_velocita_1',2:'vmc_master_velocita_2',3:'vmc_master_velocita_3',4:'vmc_master_velocita_4',5:'vmc_master_iperventilazione',6:'vmc_master_notturna',7:'vmc_master_freecooling'}
SENS = dict(te='sensor.sim_te', ti='sensor.sim_ti', ue='sensor.sim_ue', ui='sensor.sim_ui', co2='sensor.sim_co2')
ENV = dict(te=10.0, ti=20.0, ue=30.0, ui=50.0, co2=500.0)
def env(**kw):
    for k,v in kw.items():
        ENV[k]=v
        unit = {'te':'°C','ti':'°C','ue':'%','ui':'%','co2':'ppm'}[k]
        dc = {'te':'temperature','ti':'temperature','ue':'humidity','ui':'humidity','co2':'carbon_dioxide'}[k]
        setsensor(SENS[k], v, unit, dc)
async def base_setup():
    env(**ENV)
    for k, sel in [('te','temp_external'),('ti','temp_internal'),('ue','humidity_external'),('ui','humidity_internal'),('co2','co2_internal')]:
        e = f'input_select.vmc_master_selected_{sel}_entity'
        await svc('input_select','set_options',{'entity_id':e,'options':[SENS[k]]})
        await svc('input_select','select_option',{'entity_id':e,'option':SENS[k]})
    for o in ['temp_interna','temp_esterna','umidita_interna','umidita_esterna','co2','voc','verifica_impiego_vmc']:
        await svc('input_number','set_value',{'entity_id':f'input_number.vmc_master_offset_{o}','value':0})
    for sw in ['co2_e_voc','pdr','umidita']:
        await svc('input_boolean','turn_on',{'entity_id':f'input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_{sw}'})
    await svc('input_select','select_option',{'entity_id':'input_select.vmc_master_speed_umidita','option':'Velocità 2'})
    await svc('homeassistant','update_entity',{'entity_id':'sensor.vmc_master_sensori'})
MON = ['sensor.vmc_master_status_ventola_lettura_codice_interpretato','sensor.vmc_master_alert_monitoraggio_co2','sensor.vmc_master_punto_di_rugiada_verifica_confronto',
       'sensor.vmc_master_alert_monitoraggio_umidita','sensor.vmc_master_congelamento_verifica_soglia','sensor.vmc_master_delta_temp_verifica_soglia','sensor.vmc_master_status_ip_interfaccia']
def dump():
    for m in MON: print('  ', m.replace('sensor.vmc_master_',''), '=', st(m))
async def main():
    hass = await boot('cfg')
    await base_setup(); await wait(120)
    dump()
    print('--- CO2 alert from V0'); VMC.set_speed(0,'user'); await wait(60); dump()
    t0=vclock._V[0]; VMC.log.clear()
    env(co2=1500); await wait(90); dump()
    env(co2=500); await wait(90); dump()
    for l in VMC.log: print(round(l[0]-t0,2), l[1:])
if __name__ == "__main__":
    loop = vclock.VLoop(); asyncio.set_event_loop(loop); loop.run_until_complete(main())
