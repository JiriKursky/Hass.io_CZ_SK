# 8 nastavenych casu  input_datetime.filtrace_t_n, n = 1..8
# 8 delek v minutach, nesmi byt > 59 input_datetime.filtrace_casovac_vypunti_n, n = 1..8
# 
# me trapeni: 
# from datetime import datetime - nelze pouzit

# aktualni datum, cas
praveTed = datetime.datetime.now()    

hledam = True
i = 1

while hledam and i<=8 :

    sI = str(i)

    # vrati string
    sCasovac = hass.states.get("input_datetime.filtrace_t_" + sI).state

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

    # ten float je tam z duvou, desetinne tecky, jinak to blbne
    dobaMinut = int(float(hass.states.get("input_number.filtrace_casovac_vypnuti_" + sI).state))

    doCasu = casovac + datetime.timedelta(minutes = dobaMinut)

    # konecne porovnani
    if (praveTed >= casovac) and (praveTed <= doCasu):        
        # aktivni cas a nasel jsem
        hledam = False
    i = i + 1
# konec hledani casoveho intervalu        

if hledam :
    toDo = "turn_off"    
else:
    toDo = "turn_on"
# logger.info(toDo)
hass.services.call("input_boolean", toDo, {"entity_id": "input_boolean.filtrace_zapni"}, False)                   
