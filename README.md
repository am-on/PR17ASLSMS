## PR17ASLSMS
#### Podatkovno rudarjenje
# Projektna naloga:

#### Člani
- Luka Stopar 63150272 (@Tuskle)
- Amon Stopinšek 63150273 (@am-on)
- Matevž Špacapan 63150283 (@Pur3Bolt)
## Ob kateri uri je največ/najmanj linijskih prevozov?
### Pregled celotnega dneva
Na podlagi podatkov je v Sloveniji vsak dan aktivnih 1717 linij, ki
obiščejo 10040 različnih avtobusnih postajah. Vsak dan se zgodi
191295 avtobusnih prihodov. Povprečna postaja ima dnevno 19 avtobusnih
prihodov.

Spodnja slika prikazuje vse aktivne postaje. *Velikost in barva posamezne postaje
je odvisna od števila avtobusov, črte med postajami pa označujejo linije.*

![Zemljevid avtobusnih postaj in linij v Sloveniji](map/mapFinal.png)

Iz slike lahko vidimo, da so najbolj aktivne postaje v večjih mestih ali njihovi
bližini. Vidimo lahko tudi, da večina linij vodi v večja mesta, predvsem iz
Ljubljane pa je veliko direktnih linij med večjimi in tudi manjšimi mesti.

Postaja | Kraj | Število prihodov
------- | ---- | ----------------
[Avtobusna postaja Ljubljana](https://www.google.si/maps/search/46.05783284945171+14.508785575367) | Ljubljana | 1872
[Avtobusna postaja Maribor](https://www.google.si/maps/search/46.5595273032238+15.6557885112761) | Maribor | 802
[Avtobusna postaja Kranj](https://www.google.si/maps/search/46.2458155547791+14.3545303477911) | Kranj | 776
[Avtobusna postaja Celje](https://www.google.si/maps/search/46.23254801171479+15.268426387920401) | Celje | 565
[Stadion](https://www.google.si/maps/search/46.0694054750977+14.510482618162301) | Ljubljana | 559
[Kamnik](https://www.google.si/maps/search/46.2253862737911+14.613738841732099) | Kamnik | 541
[City center](https://www.google.si/maps/search/46.559209084974+15.6512855330615) | Maribor | 491
[Grosuplje](https://www.google.si/maps/search/45.955762604002196+14.652992226675698) | Grosuplje | 491
[Domžale](https://www.google.si/maps/search/46.1389885722632+14.594263506596802) | Domžale | 460
[Avtobusna postaja Ptuj](https://www.google.si/maps/search/46.4214378477102+15.8766981201461) | Ptuj | 455

Tabela potrjuje ugotovitve s slike. Vse postaje izmed prvih deset najbolj aktivnih postaj se nahajajo v večjih mestih ali njihovi neposredni bližini.

### Število postankov po urah

![Število postankov po urah](hourStat/hourBarPlot.png)

Graf prikazuje število postankov v posamezni uri. Največ postankov se zgodi med 6. in 7. uro in sicer 20148. Druga najbolj aktivna ura je med 14. in 15. uro, ko se zgodi  19938 prihodov.

Najmanj prihodov se zgodi od 1. do 4. ure zjutraj, ko je skupno le 34 prihodov. Spodnji zemljevid prikazuje aktivne avtobusne postaje in linije v tem času.

![Število postankov med 1. in 3. uro](hourStat/map/01:00:00&#32;-&#32;03:59:59.png)

### Podroben pregled ure z največ prihodi
Največ avtobusnih prihodov se zgodi med 6. in 7. uro. V tem času je aktivnih 948 linij (*55% vseh linij*), ki opravijo
20148 prihodov (*10% vseh prihodov*) na 6810 različnih postajah (*68% vseh postaj*).

Postaja | Kraj | Število prihodov
------- | ---- | ----------------
[Avtobusna postaja Ljubljana](https://www.google.si/maps/search/46.05783284945171+14.508785575367) | Ljubljana | 163
[Avtobusna postaja Kranj](https://www.google.si/maps/search/46.2458155547791+14.3545303477911) | Kranj | 92
[Avtobusna postaja Maribor](https://www.google.si/maps/search/46.5595273032238+15.6557885112761) | Maribor | 78
[Avtobusna postaja Celje](https://www.google.si/maps/search/46.23254801171479+15.268426387920401) | Celje | 68
[Avtobusna postaja Ptuj](https://www.google.si/maps/search/46.4214378477102+15.8766981201461) | Ptuj | 59

Zemljevid aktivnih avtobusnih postaj in linij med 6. in 7. uro izgleda precej podoben zemljevidu ki zajema obdobje celotnega dneva. Opazimo lahko, da je ob tej uri manj aktivnih postaj v manjših krajih, oddaljenih od večjih mest v primerjavi z zemljevidom za celoten dan.

![Število postankov med 6. in 7. uro](hourStat/map/06:00:00&#32;-&#32;06:59:59.png)


### Podroben pregled ure z najman prihodi
Najmanj avtobusnih prevozov se zgodi med 2. in 3. uro ponoči. V tem času sta
aktivni dve liniji (*Vrtojba Drive In - N. Gorica IZC Park - N. Gorica IZC Perla - Solkan H. Sabotin - Vrtojba Drive In,  Ljubljana - Murska Sobota*).

# Dodatki
![Animacija postaj in linij po urah](hourStat/map/hour-fast.gif)
