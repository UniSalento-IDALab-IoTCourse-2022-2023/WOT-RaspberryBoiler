# WOT-RaspberryBoiler

## Descrizione del progetto
Il progetto è basato sulla manutenzione delle caldaie, considerando la pericolosità dei processi che utilizzano (come la combustione del gas) e l'impatto ambientale che possono avere.

Si propone un sistema innovativo che sfrutta le tecnologie IoT (Internet of Things) per monitorare il funzionamento delle caldaie e rilevare eventuali anomalie in tempo reale. Un'importante componente di questo sistema è una board prototipale, in grado di acquisire dati simili a quelli che vengono monitorati all'interno di una caldaia.
I dati acquisiti dalla board prototipale vengono quindi inviati a un dispositivo centrale, chiamato gateway, che ha la capacità di elaborare i dati in loco. Il gateway analizza i dati ricevuti e rileva eventuali anomalie nel funzionamento della caldaia, come ad esempio una temperatura o una pressione anomale, o un'alta emissione di gas.

In caso di rilevamento di un problema, il sistema è in grado di generare alert, avvisando gli utenti o il personale tecnico responsabile della manutenzione della caldaia. Questo consente un intervento tempestivo per risolvere il problema prima che si manifestino effetti indesiderati o pericolosi.
Inoltre, il sistema comunica con un sistema esterno per il monitoraggio dei consumi energetici e dell'inquinamento generato dalla caldaia. Questo permette di avere una visione completa sull'efficienza energetica e sull'impatto ambientale del dispositivo, consentendo eventuali interventi mirati per ottimizzare l'uso delle risorse e ridurre l'inquinamento.

Infine, tutte le informazioni raccolte e i dati elaborati vengono visualizzati in una dashboard che fornisce una panoramica completa dello stato e delle prestazioni della caldaia. Questo permette agli utenti di monitorare facilmente il funzionamento del dispositivo e di avere una chiara comprensione dei consumi energetici e delle emissioni.

## Architettura del sistema
L'architettura della soluzione proposta prevede un Raspberry Pi che metterà a disposizione la sua computazione ed il suo modulo bluetooth per poter, tramite il protocollo OpenTherm, acquisire i dati di temperatura, pressione, flusso, emissioni di gas, ecc. Questa acquisizione di dati verrà effettuata ogni minuto in modo da non avere problemi di ritardo nella segnalazione di anomalie.
Successivamente i dati arrivati alla board prototipale verranno inviati ad un gateway locale, che sarà in grado di ricevere i dati per poter effettuare un’analisi di anomalie. Questo processo viene eseguito in locale per favorire la rapidità di intervento in caso di guasti pericolosi all’utenza, infatti permetteranno di effettuare un'analisi preliminare sulle anomalie rilevate nei dati della caldaia.
Una volta che sono state effettuate le analisi locali il gateway, tramite il protocollo MQTT, si occupa di inviare al back-end del cloud, su due queue diverse, sia i dati grezzi che i dati di allarme e quindi delle anomalie riscontrate.
Infine l’utente potrà visionare e monitorare l’andamento della caldaia grazie ad una pratica dashboard presente sulla webapp.

![](./img%20readme/architettura%202.png)

## Collegamento agli altri componenti
I collegamenti con tutti i componenti del progetto sono:
- [WOT-RaspberryBoile](https://github.com/UniSalento-IDALab-IoTCourse-2022-2023/WOT-RaspberryBoile)
- [WOT-Gateway](https://github.com/UniSalento-IDALab-IoTCourse-2022-2023/WOT-Gateway)
- [WOT-monitoring-be](https://github.com/UniSalento-IDALab-IoTCourse-2022-2023/WOT-monitoring-be)
- [WOT-monitoring-fe](https://github.com/UniSalento-IDALab-IoTCourse-2022-2023/WOT-monitoring-fe)

## Descrizione del componente corrente
Il componente corrente è il Raspberry, il quale permetterà, una volta avviato tutto il sistema, di acquisire i dati che gli arrivano dal protocollo OpenTherm e dai sensori per poi passarli al Gateway. Nel nosto caso, dato che stiamo simulando la presenza di una caldaia e dei sensori ad essa assocaiti, i dati sono generati da degli script python.
