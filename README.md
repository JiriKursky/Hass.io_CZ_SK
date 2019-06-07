If you need english manual, let me know via [Home Assistant community](https://community.home-assistant.io/) or *Facebook community Home Assistant - Hassio chytrý dům CZ/SK*

# Časovač pro řízení filtrace nebo čehokoli během dne
Uvedený postup by měl zajistit spuštění switche *switch.filtrace* ve třech různých cyklech.

Uvedený návod funguje pro Sonoff s flashem Tasmota a rozeběhlým MQTT. Předpokládají se jen základní znalosti, mělo by to fungovat, když jen dodržíte uvedený postup. Na 99% jsem se někde sekl, budu rád za připomínky.

Kdy se filtrace zapíná, naleznete v *filtrace_t_x* a jak dlouho poběží v minutách v *filtrace_casovac_vypnuti_x*

Aby fungovalo níže popsané, musí se zadefinovat entita *filtrace_zapni*, která je třeba vrazit někam do *configuration.yaml*:

```yaml
input_boolean:
  filtrace_zapni:
    name: Ovládání filtrace
``` 
*input_boolean* slouží jako pamatovák, ve kterém stavu se filtrace nachází, důvodem je, že pokud čistím bazén, potřebuju aby mi to případně nevypínalo. Zapnu přímo sonoff, ne prostřednictvím input_boolean.
zapnutí *switch.filtrace* a vypnutí se řídí automatizací, je k dispozici dole

příklad defince switche v *configuration.yaml*
```yaml
input_switch: 
- platform: mqtt
  name: "Filtrace"
  state_topic: "stat/sonoff-xx/POWER"
  command_topic: "cmnd/sonoff-xx/POWER"
  payload_on: "ON"
  payload_off: "OFF"
  payload_available: "ON"
  payload_not_available: "OFF"
  optimistic: false
  qos: 0
  retain: true
``` 

pak přidat do *configuration.yaml*
```yaml
input_datetime: !include casovace.yaml 
input_number: !include input_number.yaml  
```

zkontrolujte, máte-li v *configuration.yaml* pofporu python scriptů, hledejte a případně přidejte
```yaml
python_script:
```


vytvořit nebo přidat do *casovace.yaml*
```yaml
both_date_and_time:
  name: Input with both date and time
  has_date: true
  has_time: true
only_date:
  name: Input with only date
  has_date: true
  has_time: false
only_time:
  name: Input with only time
  has_date: false
  has_time: true
############################
# Definice spusteni filtrace
filtrace_t_1:
    name: Filtrace 1
    has_date: false
    has_time: true
    initial: '06:10'
filtrace_t_2:
    name: Filtrace 2
    has_date: false
    has_time: true
    initial: '10:10'
filtrace_t_3:
    name: Filtrace 3
    has_date: false
    has_time: true
    initial: '12:00'
```
vytvořit nebo přidat do *input_number.yaml* jak dlouho filtrace poběží
```yaml
filtrace_casovac_vypnuti_1:
  name: Filtrace časovač vypnutí
  min: 0
  max: 59
  step: 5
  mode: box
filtrace_casovac_vypnuti_2:
  name: Filtrace časovač vypnutí
  min: 0
  max: 59
  step: 5
  mode: box
filtrace_casovac_vypnuti_3:
  name: Filtrace časovač vypnutí
  min: 0
  max: 59
  step: 5
  mode: box
```  
přidat do *automations.yaml*
```yaml
- id: casovac_minuta
  alias: Časovač minuta
  trigger:
  - minutes: /1
    platform: time_pattern
    seconds: '0'
  action:
  - service: python_script.filtrace_casovac_n
  initial_state: true
 - id: 'filtrace_zapni'
  alias: Zapnutí filtrace input booleanem
  trigger:
  - entity_id: input_boolean.filtrace_zapni
    platform: state
    to: 'on'
  condition: []
  action:
  - data:
      entity_id: switch.filtrace
    service: switch.turn_on
  initial_state: true
- id: 'filtrace_vypni'
  alias: Vypnutí filtrace input booleanem
  trigger:
  - entity_id: input_boolean.filtrace_zapni
    platform: state
    to: 'off'
  condition: []
  action:
  - data:
      entity_id: switch.filtrace
    service: switch.turn_off
  initial_state: true
```
a pak do adresáře config/python_scripts (není-li, je třeba python_scripts vytvořit) nakopírovat soubor filtrace_casovac_n
v souboru filtrace_casovac_n můžete změnit POCET_CYKLU = 3 na hodnotu, která vám vyhovuje, ale pak musíte přidat nebo ubrat v souborech
(*casovace.yaml* a *input_number.yaml*) případné entity.
Do HA si naskládejte entity 

```yaml
entities:
  - entity: input_datetime.filtrace_t_1
  - entity: input_number.filtrace_casovac_vypnuti_1
```
umožní vám nastavit čas začátku a délku trvání.

Toť vše.
