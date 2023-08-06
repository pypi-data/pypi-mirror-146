
from urllib.request import urlopen


# Dixon’s Q test with a 90% confidence for removing outliers before calculating the average value
def dixon_test(list):
    list.sort()
    if len(list) >= 3:
        Gap1 = float(list[1]) - float(list[0])
        Gap2 = float(list[-1]) - float(list[-2])
        Range = float(list[-1]) - float(list[0])
        if len(list) == 3:
            DixonTable = 0.941
        elif len(list) == 4:
            DixonTable = 0.765
        elif len(list) == 5:
            DixonTable = 0.642
        elif len(list) == 6:
            DixonTable = 0.56
        elif len(list) == 7:
            DixonTable = 0.507
        elif len(list) == 8:
            DixonTable = 0.468
        elif len(list) == 9:
            DixonTable = 0.437
        elif len(list) == 10:
            DixonTable = 0.412
        if Gap1 > Gap2:
            DixonQ = Gap1 / Range
            if DixonQ > DixonTable:
                list.remove(list[0])
        elif Gap1 < Gap2:
            DixonQ = Gap2 / Range
            if DixonQ > DixonTable:
                list.remove(list[-1])

    return list




def cas_to_smiles_nih(cas):
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + cas + '/smiles'
        smiles = urlopen(url).read().decode('utf8')
        return smiles
    except:
        return 'No data found'


