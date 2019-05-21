# Časovač pro řízení filtrace

přidat do *configuration.yaml*
```yaml
input_datetime: !include casovace.yaml 
input_number: !include input_number.yaml  
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
###################
# Definice filtrace
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
vytvořit nebo přidat do *input_number.yaml*
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
```
a pak do adresáře config/python_scripts (není-li, je třeba python_scripts vytvořit) nakopírovat soubor filtrace_casovac_n
v souboru filtrace_casovac_n můžete změnit POCET_CYKLU = 3 na hodnotu, která vám vyhovuje, ale pak musíte přidat nebo ubrat v souborech
(*casovace.yaml* a *input_number.yaml*) případné entity.
