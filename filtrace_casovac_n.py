# 8 nastavenych casu  input_datetime.filtrace_t_n, n = 1..3
# 8 delek v minutach, nesmi byt > 59 input_datetime.filtrace_casovac_vypunti_n, n = 1..3
# 
# nedostatek znalosti: 
# from datetime import datetime - nelze pouzit

# pocet cyklu za 24 hodin = 'n'
POCET_CYKLU = 3

# nastaveny pocatecni cas
# entity musi byt definovane takto input_datetime.filtrace_t_1, input_datetime.filtrace_t_2 ... az do POCET_CYKLU
ENTITY_FILTRACE_T = 'filtrace_t'


# doba behu, musi byt mensi nez 59 - nehlidano(!)
# entity musi byt input_number.filtrace_casovac_vypnuti_1, input_number.filtrace_casovac_vypnuti_2 ... az do POCET_CYKLU
ENTITY_DOBA_BEHU = 'filtrace_casovac_vypnuti'

# co se spusti nebo vypne sluzbou input_boolean.turn_on nebo input_boolean.turn_off
ENTITY_AKCE = 'filtrace_zapni'

# aktualni datum, cas
praveTed = datetime.datetime.now()    

hledam = True
i = 1

while hledam and i <= POCET_CYKLU :

    sI = str(i)

    # vrati string
    sCasovac = hass.states.get("input_datetime." + ENTITY_FILTRACE_T + "_" + sI).state

    # hodila by se funkce strptime, ale bez sance
    # casovac = datetime.strptime(sCasovac, '%H:%M:%S') 
    # vrati chybu __import__
    # casovac = datetime.datetime.strptime(sCasovac, '%H:%M:%S') 
    #
    # toto vrati chybu, ze neni povoleno pouzit strptime
    # casovac = datetime.strptime(sCasovac, '%H:%M:%S') 

    # takze potupne parsovani a prevod na objekt
    hodina = int(sCasovac[0:2])
    minuta = int(sCasovac[3:5])
    vterina = int(sCasovac[7:9])
    # vlastni prevod
    casovac = praveTed.replace(hour=hodina, minute=minuta, second=vterina)

    # ten float je tam z duvodu, desetinne tecky, jinak to blbne
    dobaMinut = int(float(hass.states.get("input_number." + ENTITY_DOBA_BEHU + "_" + sI).state))

    doCasu = casovac + datetime.timedelta(minutes = dobaMinut)

    # konecne porovnani
    if (praveTed >= casovac) and (praveTed <= doCasu):        
        # aktivni cas a nasel jsem
        hledam = False
    i = i + 1
# end while
# konec hledani casoveho intervalu, pokud je aktivni ma 'hledam' hodnotu false        

if hledam :
    toDo = "turn_off"    
else:
    toDo = "turn_on"

# pro ucely ladeni
# logger.info(toDo)

hass.services.call("input_boolean", toDo, { "entity_id": "input_boolean." + ENTITY_AKCE }, False)                   
