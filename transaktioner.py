import sys
import csv
import re
import numpy as np

def main():
    if len(sys.argv) == 2:
        sys.exit("Usage py transaktioner.py fortnox.txt transaktioner.csv")
    #Create dictionarys
    fortnox = arrange_txt(sys.argv[1])
    bank = arrange_csv(sys.argv[2])
    #Check for errors. The function can be improved and get smarter. At the moment very easy check.
    (lst_date,lst_sum,lst_wrong) = check_total(fortnox,bank)
    #Save to a csv to work with
    data = np.asarray([lst_date,lst_sum,lst_wrong],dtype=object)
    np.savetxt("data.csv", data, fmt='%s')

def arrange_txt(file):
    """ Takes the txtfile and arranges the data to be analyzed """
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
        #If something that is a verification
        if len(fortnox[key]) > 2:
            #Is not a date (xxxx-xx-xx)
            if not len(fortnox[key][1]) == 10:
                #Remove, since it is a project number
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
    f.close()
    fortnox = arrange_date_txt(fortnox)
    return fortnox

def arrange_csv(file):
    """ Reads the csv and arranges the data to be analyzed """
    with open(file,'r') as f:
        reader = csv.reader(f)
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
    f.close()
    bank = arrange_date_csv(rows)
    return bank

def arrange_date_txt(txtfile):
    """The fnc will arrange the data with TheDate : [(transaction, total sum),(transaction,total sum)]... """
    datedict = dict()
    item_old = None
    for key,item in txtfile.items():
        item[3] = parseNumber(item[3])
        item[4] = parseNumber(item[4])
        if not ispositive(item_old,item):
            item[3] = -item[3]
        if not item[1] in datedict:
            datedict[f"{item[1]}"] = []
            datedict[item[1]].append((item[3],item[4]))
        else:
            datedict[item[1]].append((item[3],item[4]))
        item_old = item
    return datedict

def arrange_date_csv(csvfile):
    """Arranges the transactions in the bank file in dates """
    datedictcsv = dict()
    for key,value in csvfile.items():
        value[3] = parseNumber(value[3])
        value[4] = parseNumber(value[4])
        if not value[1] in datedictcsv:
            datedictcsv[value[1]] = []
            datedictcsv[value[1]].append((value[3],value[4]))
        else:
            datedictcsv[value[1]].append((value[3],value[4]))
    return datedictcsv

def ispositive(olditem,newitem):
    """Assuming the first number as negative for know. Will find out if the sign of the transaction is negative or positive """
    if olditem is None:
        return False
    last_total = olditem[4]
    new_total = newitem[4]
    sign = new_total - last_total
    if sign > 0:
        return True
    else:
        return False

def check_total(accounting,real):
    """ Takes two dictionaries and checks if the two matches. """
    check_date = []
    check_sum = []
    wrong_date = []
    for key,value in real.items():
        if key not in accounting:
            check_date.append(key)
        else:
            sum_real = 0
            for transaction in value:
                sum_real += transaction[0]
            lst_accounting = accounting[key]    
            sum_accounting = 0
            for transaction in lst_accounting:
                sum_accounting += transaction[0]
            if not sum_real == sum_accounting:
                check_sum.append(key)
    for key,value in accounting.items():
        if key not in real:
            wrong_date.append(key)
    return check_date,check_sum,wrong_date

def parseNumber(text):
    """ Function copied from github """
    # First we return None if we don't have something in the text:
    if text is None:
        return None
    if isinstance(text, int) or isinstance(text, float):
        return text
    text = text.strip()
    if text == "":
        return None
    # Next we get the first "[0-9,. ]+":
    n = re.search("-?[0-9]*([,. ]?[0-9]+)+", text).group(0)
    n = n.strip()
    if not re.match(".*[0-9]+.*", text):
        return None
    # Then we cut to keep only 2 symbols:
    while " " in n and "," in n and "." in n:
        index = max(n.rfind(','), n.rfind(' '), n.rfind('.'))
        n = n[0:index]
    n = n.strip()
    # We count the number of symbols:
    symbolsCount = 0
    for current in [" ", ",", "."]:
        if current in n:
            symbolsCount += 1
    # If we don't have any symbol, we do nothing:
    if symbolsCount == 0:
        pass
    # With one symbol:
    elif symbolsCount == 1:
        # If this is a space, we just remove all:
        if " " in n:
            n = n.replace(" ", "")
        # Else we set it as a "." if one occurence, or remove it:
        else:
            theSymbol = "," if "," in n else "."
            if n.count(theSymbol) > 1:
                n = n.replace(theSymbol, "")
            else:
                n = n.replace(theSymbol, ".")
    else:
        # Now replace symbols so the right symbol is "." and all left are "":
        rightSymbolIndex = max(n.rfind(','), n.rfind(' '), n.rfind('.'))
        rightSymbol = n[rightSymbolIndex:rightSymbolIndex+1]
        if rightSymbol == " ":
            return parseNumber(n.replace(" ", "_"))
        n = n.replace(rightSymbol, "R")
        leftSymbolIndex = max(n.rfind(','), n.rfind(' '), n.rfind('.'))
        leftSymbol = n[leftSymbolIndex:leftSymbolIndex+1]
        n = n.replace(leftSymbol, "L")
        n = n.replace("L", "")
        n = n.replace("R", ".")
    # And we cast the text to float or int:
    n = float(n)
    if n.is_integer():
        return int(n)
    else:
        return n

if __name__ == "__main__":
    main()
