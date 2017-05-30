## PR17ASLSMS
#### Podatkovno rudarjenje
# Projektna naloga: Analiza javnega prevoza v Sloveniji

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

## Finančno stanje prevoznika in ponujeni prevozi...

Ko pomislimo na ponudnike javnih prevozov, se zavedamo, da imajo nekateri boljši finančno stanje kot drugi. Zakaj je temu tako? Ima to kakšno povezavo s ponujenimi prevozi ali je to zgolj le dobro načrtovanje in poraba danih sredstev?

### ...V primerjavi s številom linij

Na prvem mestu izpostavimo, da se v podatkih najde nekaj robnih primerov: podjetja, ki imajo izredno visok dobiček in izredno malo prevozov. Razlog za to so nepopolni podatki in za boljše razumevanje povezave med financami in številom ponujenih linij so tej prevozniki (Slovenske železnice, Avtoprevozništvo Kraševec Sandi S.P., Pohorje turizem in AP prevoz oseb Špik Miroslav S.P.) izločeni iz analize.
Opazi se, da prevozniki, ki so bolj dobičkonosni ne ponujajo toliko ponujenih prevozov kot tisti, ki niso. Na grafu je prikazan dobiček za opravljeno povezavo.
![Finance proti številom linij](finance/dobicek-vs-povezave.png)

Zgornji Zavratnik d.o.o. je bil celo preveč optimističen in je šel v izgubo (skupno -21.000€), JP LPT pa se komaj da prebije z nekaj dobička (37€ na povezavo), najbolj donosni izmed upoštevanih pa so AP Rižana d.o.o. in Arriva Štajerska d.d., ki imajo donos krepkih 4.500€ na linijo.

### ...V primerjavi s številom prevoženih kilometrov

Zanimivo je, da je slika popolnoma drugačna v primerjavi s prevoženim številom kilometrov, kjer pri istih prevoznikih ni nobene povezave. Spet lahko opazimo nekaj izstopanj, kjer so prevozniki izjemno dobičkonosni za vsak prevožen kilometer. Najboljši donesejo okoli 200€/km, najslabši pa pod 10€/km. Zgornji Zavratnik ima pa izgubo 46€ za vsak prevožen kilometer.
![Finance proti številom linij](finance/dobicek-vs-km.png)

## Je potovanje z avtomobilom hitrejše od javnega prevoza?

Potovanje je v veliki večini primerov hitrejše z avtomobilom, v nekaterih primerih je potovanje enako hitro. V zelo redkih primerih se je izkazalo, da je potovanje hitrejše z javnim prevozom (še to je k večjemu, ker je lahko del poti avtomobilom nedostopen ali pa rezerviran samo za javni prevoz).
Če bi na relacijah potovali z avtomobilom, bi v povprečju prevozili 53km/h; če bi se na iste relacije odpravili z javnim prevozom, bi pa potovali s hitrostjo 31km/h. Iz tega lahko razberemo, da z avtomobilom dosežemo željeno destinacijo 1.7-krat hitreje (seveda bi bilo potrebno pri javnem prevozu tudi upoštevati, da se pogosto moramo presesti iz ene relacije na drugo).

# Dodatki
![Animacija postaj in linij po urah](hourStat/map/hour-fast.gif)
