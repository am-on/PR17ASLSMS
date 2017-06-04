## PR17ASLSMS
#### Podatkovno rudarjenje
# Projektna naloga: Analiza javnega prevoza v Sloveniji

#### Člani
- Luka Stopar 63150272 (@Tuskle)
- Amon Stopinšek 63150273 (@am-on)
- Matevž Špacapan 63150283 (@Pur3Bolt)

# 1. Uvod
Pri projektni nalogi smo se lotili podatkovnega rudarjenja linijskih odsekov in voznih redov javnega potniškega prometa.

V okviru naloge smo odgovorili na naslednja vprašanja:
- ob kateri uri je največ/najmanj linijskih prevozov?
- obstaja povezava med finančnim stanjem prevoznika in številom linij/prevoženih kilometrov?
- je potovanje z avtomobilom hitrejše od potovanja z javnim potniškim prometom?
- obstaja povezava med številom prebivalcev v mestu in pogostostjo linijskih voženj?

# 2. Opis podatkov

Viri podatkov: [OPSI - Register linijskih odsekov](https://podatki.gov.si/dataset/register-linijskih-odsekov), [Statistični urad RS](http://pxweb.stat.si/pxweb/Database/Dem_soc/05_prebivalstvo/10_stevilo_preb/20_05C40_prebivalstvo_obcine/20_05C40_prebivalstvo_obcine.asp), [Google Maps - Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/), [Stop neplačniki](http://www.stop-neplacniki.si/),[GeoNames](http://download.geonames.org/export/dump/)


Množico podatkov sestavljajo vsi podatki, ki jih Google uporablja za storitev [Maps Transit](https://maps.google.com/landing/transit/index.html). Ti podatki zajemajo seznam prevoznikov, koordinate in opis postaj, linije in posamezne linijske odseke, posamezne čase prihodov in odhodov s postaj, in podatke za izris linijskih odsekov.

### Podroben opis podatkov

- `LINIJSKI_ODSEKI.dbf` vsebuje podatke o linijskih odsekih:
    - začetna postaja,
    - končna postaja,
    - id začetne postaje,
    - id končne postaje,
    - dolžina odseka

- `LINIJSKI_ODSEKI.prj` `LINIJSKI_ODSEKI.fix` `LINIJSKI_ODSEKI.shp`
`LINIJSKI_ODSEKI.shx` podatki v formatu [Shapefile](https://en.wikipedia.org/wiki/Shapefile#Shapefile_shape_format_.28.shp.29)

- `agency.txt` vsebuje podatke o prevoznikih
    - id prevoznika,
    - naziv prevoznika

- `calendar.txt` splošni vozni red
    - id linije
    - dnevi v tednu ko je linija aktivna *(1 - linija aktivna, 0 - linija ni aktivna)*
    - začetek in konec veljavnosti koledarja

- `calendar_dates.txt` izjeme v voznem redu
    - id linije
    - datum
    - vrsta izjeme *(1 - linija aktivna, 0 - linija ni aktivna)*

- `routes.txt` opisi linij  
    - id linije
    - id prevoznika
    - ime linije

- `shapes.txt` podatki za risanje odsekov

- `stops.txt` podatki o postajah
    - id postaje
    - ime postaje
    - koordinate

- `stop_times.txt` podatki o prihodih in odhodih
    - id odseka
    - čas prihoda
    - čas odhoda
    - id postaje

- `trips.txt` opisi odsekov
- `si.csv` opisi krajev
    - ime kraja
    - koordinate
    - št. prebivalcev
    - nadmorska višina

# 3. Metode

### Priprava podatkov
Podatki se nahajajo v več ločenih datotekah in se med seboj navezujejo preko
ujemajočih se id-jev. Podatke smo zato združili iz različnih datotek v en
`DataFrame`. Pri tem smo si pomagali s knjižico
[pandas](http://pandas.pydata.org/). Med združevanjem podatkov smo izločili še
odvečne in prazne atribute.

```python
def read(location):
    return pd.read_csv(location)

# read data, drop unnecessary cols
agency = read('./data/google_feed/agency.txt')
agency.drop(['agency_url', 'agency_timezone', 'agency_phone', 'agency_lang'],axis=1,inplace=True)

routes = read('./data/google_feed/routes.txt')
routes.drop(['route_short_name', 'route_desc', 'route_url', 'route_color', 'route_text_color'],axis=1,inplace=True)

trips = read('./data/google_feed/trips.txt')
trips.drop(['trip_headsign', 'block_id'],axis=1,inplace=True)

stopTimes = read('./data/google_feed/stop_times.txt')
stopTimes.drop(['stop_headsign'],axis=1,inplace=True)

stops = read('./data/google_feed/stops.txt')
stops.drop(['stop_desc', 'zone_id', 'stop_url'],axis=1,inplace=True)

# merge data into one df
df = pd.merge(agency, routes, on='agency_id')
df = pd.merge(df, trips, on='route_id')
df = pd.merge(df, stopTimes, on='trip_id')
df = pd.merge(df, stops, on='stop_id')
```

### Izdelava zemljevida
Za izdelavo zemljevida smo uporabili knjižico [Matplotlib Basemap](http://matplotlib.org/basemap/).

Nastaviti je bilo potrebno meje za zemljevid. Površino Slovenije smo orisali z uporabo `shapefile`
datoteke, ki je vsebovala vse meje držav v Evropi.

Risanje postaj je bilo z uporabo knjižice zelo preprosto. Podati je bilo potrebno
le koordinate postaje, barvo ter velikost. Barvo in velikost smo določili na podlagi
števila avtobusov na postaji v danem časovnem obdobju. Barvo smo glede na velikost
izračunali s pomočjo barvnega sistema `HSV` in jo nato pretvorili v `RGB`.

```python
def heatMapColorForValue(self, value):
  h = (1.0 - value) * 240
  return (h/360, 1, 0.5)

def getStopStyle(self, size):
    scale = 4
    size = size / max(20, self.maxStopN*0.2)
    h, s, v = self.heatMapColorForValue(min([size, 1]))
    color = colorsys.hsv_to_rgb(h, s, v)
    size = 1 + (size * scale) ** 1.1
    return (size, color)

def plot_stops(self, row):
    x, y = row.name
    x, y = self.m(x, y)
    size, color = self.getStopStyle(row['stop_id'])
    self.m.plot(x, y, 'o', markersize=size, color=color, alpha=0.3, markeredgewidth=0.0)
```

Risanje povezav med postajami je predstavljalo kar nekaj preglavic. Risanje črt
je že v osnovi počasnejše od risanja točk, narisati pa je bilo potrebno približno
200 000 povezav, kar je 20× več kot postaj. Risanje je zaradi tega bilo zelo
počasno, v prvi verziji kode bi vse skupaj trajalo več kot 10 ur. V
uradni dokumentaciji nismo našli ničesar kar bi nam pomagalo pohitriti risanje.
Z iskanjem po spletu smo našli ustrezno pohitritev. Povezave je bilo potrebno
predstaviti v seznamu koordinat in jih narisati naenkrat.

### Delo s časom
Tudi pri delu s časom smo si pomagali s knjižico pandas. Najprej je bilo potrebno
čas pretvoriti v ustrezen format. Pri tem smo naleteli na nekaj napačnih podatkov,
kjer so bile v podatkih zapisane napačne ure (npr. 27:00). Po odpravi napačnih
podatkov smo čas v ustrezen format pretvorili s pomočjo funkcije `pd.to_datetime()`.

### Google Maps Distance Matrix API
Podatke o razdalji in času vožnje z avtomobilom ali javnim prevozom se je pridobilo iz
Google Maps preko Distance Matrix API. Omejitev (za brezplačno uporabo) je do 2.500
poizvedb na dan, ker pa smo imeli podatkov več, smo pridobili celotno množico podatkov
skozi več dni.

```python
gmaps = googlemaps.Client(key='AIzaSyAjAw1bVBU1KncV-zg2RS9QrhbSAA_0aag')

def calculate_time(start_lat, start_lon, dep_time, end_lat, end_lon, mode):
    time = datetime.strptime(date + ' ' + dep_time, '%d.%m.%Y %H:%M:%S')
    try:
        directions = gmaps.directions(origin=str(start_lat) + ',' + str(start_lon),
                                      destination=str(end_lat) + ',' + str(end_lon),
                                      mode=mode,
                                      departure_time=time)
    except:
        return 0, 1
    try:
        return (directions[0].get('legs')[0].get('distance').get('value') / 1000,
                int(directions[0].get('legs')[0].get('duration').get('value') / 60))
    except IndexError:
        return 0, 1
```
Pri poizvedbi se lahko pridobi napačne podatke ali pa povezava ne obstaja; te primere
se obravnava s pomočjo izjem. Vrhnji izsek kode izračuna razdaljo in trajanje povezave
med danima točkama ob izbranem času.

### Delo s kraji
Podatke krajev se je s pomočjo knjižnice Rtree shranilo v index,preko katerega se je z NearestNeighbour iskanjem vsako povezavo priredilo pripadajočemu kraju. Vendar pa, ker so kraji opisani kot točke,ter ker so lahko tudi enako oddaljeni od določene točke,so lahko nekatere postaje štete k napačnemu kraju.

# 4. Rezultati

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

Spodaj na grafu je še primerjava koliko časa se potrebuje za opraviti relacije. Tudi tukaj je opazno, da se z avtomobilom pride precej bolj hitro kot pa z javnim prevozom (ne nujno pa vedno).
![Finance proti številom linij](finance/cas_avto_vs_jp.png)

## Krajevna statistika
Kot zanimivost smo si zadali ugotoviti, če število povezav narašča/pada z številom prebivalcev in nadmorsko višino. Začetni sklep je bil, da naj bi se število povezav manjšalo z nadmorsko višino,ter dokaj linearno večalo z številom prebivalcev.

### Nadmorska višina
Ob obdelavi podatkov smo ugotovili,da se kraji z majhnim številom(~5) povezav nahajajo na celotnem spektru nadmorskih višin,kraji z velikim številom(200+) pa na odseku 150-400m nadmorske višine.Naša hipoteza je bila tudi delno potrjena,saj se nad 1000m pojavljajo večinoma kraji z malim številom povezav.
![Število povezav v odvisnosti nadmorske višine](stats/foo.png)
### Število prebivalcev
Izkazalo se je,da si prvi dve največji slovenski mesti sledita linearno(Ljublana in Maribor),drugi kraji pa so razporejeni bolj kaotično.
![Število povezav v odvisnosti števila prebivalcev](stats/prebs.png)
Kot zanimivost smo še pogledali,če se graf spremeni če primerjamo kakšen delež vseh povezav ima določeno mesto v odvisnosti od deleža prebivalcev v tistem mestu.Graf se je izkazal za drastično različnega od prejšnjih in je pokazal, ima dosti manjših mest disproporcionalno veliko povezav,večja mesta pa so dokaj normalizirala.
![Število povezav v odvisnosti števila prebivalcev](stats/hei.png)
# Dodatki
![Animacija postaj in linij po urah](hourStat/map/hour-fast.gif)
