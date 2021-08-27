import sys
import csv


def main():
    if len(sys.argv) == 2:
        sys.exit("Usage py fortnox.txt transaktioner.csv")
    
    #Create dictionarys
    fortnox = arrange_txt(sys.argv[1])
    bank = arrange_csv(sys.argv[2])
    print(fortnox)
    print(bank)

def arrange_txt(file):
    with open(file, "r") as f:
        lines = f.readlines()
    f.close()
    count = 0
    fortnox = dict()
    for line in lines:
        fortnox[f"{count}"] = line
        count += 1
    for i in range(0,13):
        del fortnox[f"{i}"]
    for key,value in fortnox.items():
        fortnox[key] = fortnox[key].replace('\t','\xa0')
        fortnox[key] = fortnox[key].replace('\n','\xa0')
        fortnox[key] = fortnox[key].split('\xa0')
        fortnox[key] = list(filter(None,fortnox[key]))
        if len(fortnox[key]) > 2:
            if not len(fortnox[key][1]) == 10:
                fortnox[key].remove(fortnox[key][1])
    last = list(fortnox)[-1]
    list_clean = []
    list_clean.append(last)
    for i in range(1,7):
        number = int(last) - i
        list_clean.append(number)
    for key in list_clean:
        del fortnox[f'{key}']
    #Här slutar fix med att ordna txt-fil från fortnox
    
    return fortnox

def arrange_csv(file):
    with open(file,'r') as f:
        reader = csv.reader(f)
    f.close()
        rows = dict()
        count = 0
        for row in reader:
            rows[f'{count}'] = row
            count += 1
        
        for i in range(0,2):
            del rows[f'{i}']
        
        for key,value in rows.items():
            list_rm = rows[f'{key}'][1:7]
            list_rm.append(rows[f'{key}'][9])
            for rm in list_rm:
                if rm in value:
                    value.remove(rm)
    
    return rows

def arrange_date():
    hello = 21
    #Suppose to arrange the data by date
    #Förslag: datum : [[betalning,betalning,betalning],total summa]

def check_total():
    hello = 22
    #Suppose to check if the total number matches for a certain date

if __name__ == "__main__":
    main()
