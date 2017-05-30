import pandas as pd
import csv


def read(location):
    return pd.read_csv(location)


agency = read('./data/google_feed/agency.txt')
agency.drop(['agency_url', 'agency_timezone', 'agency_phone', 'agency_lang'], axis=1, inplace=True)
n = {'agency_A20_531': 455, 'agency_A31_531': 17, 'agency_A44_531': 10, 'agency_A13_531': 66, 'agency_A15_531': 1509,
     'agency_A33_531': 25, 'agency_A14_531': 707, 'agency_A39_531': 150, 'agency_A22_531': 1525, 'agency_A51_531': 6,
     'agency_A10_531': 154, 'agency_A03_531': 278, 'agency_A19_531': 1573, 'agency_A23_531': 16, 'agency_A56_531': 10,
     'agency_A60_531': 3, 'agency_A24_531': 43, 'agency_A58_531': 8, 'agency_A95_531': 4, 'agency_A34_531': 100,
     'agency_A48_531': 45, 'agency_A07_531': 97, 'agency_A11_531': 411, 'agency_A30_531': 14, 'agency_A32_531': 15,
     'agency_A42_531': 10, 'agency_A57_531': 39, 'agency_A09_531': 87, 'agency_A18_531': 771, 'agency_A36_531': 24,
     'agency_A97_531': 9, 'agency_A55_531': 26, 'agency_A12_531': 1341, 'agency_A01_531': 741, 'agency_A21_531': 392}
d = {'agency_A20_531': 17965.205000000034, 'agency_A31_531': 429.3400000000001, 'agency_A44_531': 322.384,
     'agency_A13_531': 1298.4039999999993, 'agency_A15_531': 25769.389999999934, 'agency_A33_531': 323.941,
     'agency_A14_531': 16162.857999999966, 'agency_A39_531': 3652.601000000001, 'agency_A22_531': 33132.990000000034,
     'agency_A51_531': 450.961, 'agency_A10_531': 3511.2430000000027, 'agency_A03_531': 6101.735999999994,
     'agency_A19_531': 32536.080999999976, 'agency_A23_531': 1258.3349999999998, 'agency_A56_531': 97.343,
     'agency_A60_531': 132.312, 'agency_A24_531': 2112.2999999999997, 'agency_A58_531': 199.38000000000002,
     'agency_A95_531': 449.49699999999996, 'agency_A34_531': 3256.4399999999996, 'agency_A48_531': 239.64500000000004,
     'agency_A07_531': 2738.3239999999987, 'agency_A11_531': 5144.404999999992, 'agency_A30_531': 602.672,
     'agency_A32_531': 517.894, 'agency_A42_531': 324.3040000000001, 'agency_A57_531': 1166.931,
     'agency_A09_531': 3951.5129999999995, 'agency_A18_531': 27172.553000000087, 'agency_A36_531': 146.70000000000002,
     'agency_A97_531': 122.39699999999999, 'agency_A55_531': 391.19500000000005, 'agency_A12_531': 29728.257999999914,
     'agency_A01_531': 22595.730000000036, 'agency_A21_531': 12123.522999999983}
arr = []
#makes data from dict prettier and saves it to a csv
for k, v in n.items():
    for i in range(len(n.keys())):
        if agency[i:i + 1]['agency_id'].values[0] == k:
            arr.append([agency[i:i + 1]['agency_name'].values[0].replace("Š", "S").replace("Ž", "Z").replace("Č", "C"), #prevoznik
                        v, #stevilo linij
                        d[k], #stevilo km
                        int(agency[i:i + 1]['dobicek'].values[0].replace('.', ''))]) #dobicek

with open("racunaj.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(arr)
