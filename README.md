# DecidimIntegrat

Hi ha 2 blocs amb 2 objectius diferenciats:

1. MODEL INTEGRAT: Adapta el projecte DecidimOptim (Autor: Marc Serramia) al Model Integrat d'Optimització que inclou l'Alineació amb Valors 
   (value alignement). Aquesta part inclou els programes:  DecidimOptim.py, DecidimPlot.py, i DecidimProblemBuilder.py 

- Per cada districte de la ciutat de Barcelona es genera un arxiu per poder comparar el Mètode de Rank and Select i el d'Optimització

- Per generar els arxius cal donar run a DecidimPlot.py i seleccionar un dels noms clau de districte, a saber: 
    CiutatVella, Eixample, Gracia, HortaGuinardo, lesCorts, NouBarris, SantAndreu,SantMarti SantsMontjuic i SarriaSantGervasi

- Els arxius de sortida generats estan a ExperimentData/nomDistricte/Omega que poden ser carregats en Excel. Cada linea de l'arxiu correspon al resultat de 
   la selecció de propostes amb diferents sistemes: 
	-les 2 primeres línees pel mètode rank and select (una amb satisfacció ciutadana i l'altre amb l'alineació amb valors)
	-les 11 següents son pel mètode d'optimització (linea per cada valor del paramtre de pes de satisfacció ciutadana: 0,0.1,0.2, ... i 1.)

- A ExperimentData/nomDistricte/nomDistricte.txt hi ha les dades corresponents als pressupostos participatius de cada districte.

2. SIMULACIÓ: Dona suport a l'enquesta sobre pressupostos participatius del IMOP mitjançant la simulació de la casuistica així com la comprovació 
   de la bondat dels resultats. Els components d'aquesta part són: Simulacio.py, SimulacioAudit.py i SimulacioDecidimOptimAudit.py

- Per simular l'enquesta es genera per cada cas un arxiu de simulació.

- Per generar les comprobacions cal donar run a Simulacio.py i triar l'opció del cas que es vol simular: 
                1-Escenaris 3 i 4 No coincidents
                2-Escenaris 1 i 2 No coincidents
                3-Escenaris 3 i 4 Si coincidents
                4-Escenaris 1 i 2 Si coincidents 

- Els arxius de sortida de la simulacio de les respostes deixen a la carpeta Simulacio

- Per efectuar la comprovació de la bondat de les dades de la simulació s'ha de donar run a SimulacioAudit.py

- A Simulacio/simulacio.txt hi ha les dades del pressupost pariticipatiu fictici que es fa servir per l'enquesta

(*) REQUISITS: CPLEX IBM versió 22.1.0.0 o superior y Python versió 3.