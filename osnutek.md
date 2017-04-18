### Člani skupine
- Luka Stopar 63150272
- Amon Stopinšek 63150273
- Matevž Špacapan 63150283

# Opis problema
Pri projektni nalogi se bomo lotili podatkovnega rudarjenja linijskih odsekov in voznih redov javnega potniškega prometa.

V okviru naloge bomo poskusili odgovoriti na naslednja vprašanja:
- obstaja povezava med finančnim stanjem prevoznika in številom linij/prevoženih kilometrov?
- ob kateri uri je največ/najmanj linijskih prevozov?
- obstaja povezava med številom prebivalcev v mestu in pogostostjo linijskih voženj?
- je potovanje z avtomobilom hitrejše od potovanja z javnim potniškim prometom?


# Opis podatkov

Viri podatkov: [OPSI - Register linijskih odsekov](https://podatki.gov.si/dataset/register-linijskih-odsekov), [Statistični urad RS](http://pxweb.stat.si/pxweb/Database/Dem_soc/05_prebivalstvo/10_stevilo_preb/20_05C40_prebivalstvo_obcine/20_05C40_prebivalstvo_obcine.asp), [Google Maps - Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/), [Stop neplačniki](http://www.stop-neplacniki.si/)

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
