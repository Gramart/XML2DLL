#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as etree
import re
import argparse
tables = {}
counter = {}
relations = {}
pkfk = {}
def makeargs():
    parser = argparse.ArgumentParser(description="Process arguments of xtd.py") #, add_help=False)
    parser.add_argument('--input', action="store", dest="input",help='input file')
    parser.add_argument('--output', action="store", dest="output",help='output file')
    parser.add_argument('--header', action="store", dest="header",help='header of ddl')
    parser.add_argument('--etc', action="store", dest="n",help='max columns from underelements')
    parser.add_argument('-a', action="store_true", dest="a", help='no columns from attributes file')
    parser.add_argument('-b', action="store_true", dest="b", help='only one underelement file')
    parser.add_argument('-g', action="store_true", dest="g",help='output will be xml file')
    #parser.add_argument('--help', action="store_true", dest="help",help='help of programm')
    args = parser.parse_args()


    if len(sys.argv) > len(set(sys.argv)):
        print('Arguments must be unique')
        quit(1)

    #if args.n < 0:
     #   print("n parameter must be greater then 0\n",file=sys.stderr)
     #   exit(1)
#    if len(args.input) == 0:
 #       print("wrong input file\n",file=sys.stderr)
  #      exit(1)
  #  if len(args.output) == 0:
   #     print("wrong output file\n",file=sys.stderr)
   #     exit(1)
    #if args.g and args.help:
     #   print("cannot combine -g and --help\n", file=sys.stderr)
      #  exit(1)

    return args
    
def __getitem__(self, key):
    return getattr(self, key)

def make_relations(tables):
    print (pkfk)
    relations = {}
    zmena = True
    for table in pkfk.keys(): # prochazime tabulky
        #if table not in relations: ## pridame tabulku
            print (table)
            relations[table] = {}
    for table in pkfk.keys():
        for key in pkfk[table]: # prochazime sloupce
            #print ("key "+key)
            if 'prk_' in key:
                relations[table][key] = "1:1"
                #print (table+' '+tables[key]
            else: # 'value' not in key and "_id" in key: # and str(table[key]) == "INT":
                #key = key[:-4]
                #print ("key"+key)
                if key in relations.keys():
                    if table in relations[key].keys():
                        relations[table][key] = "N:M"
                        relations[key][table]= "N:M"
                    # tabulky se odkazuji vzajemne
                    else:
                        relations[key][table] = "1:N"
                        relations[table][key] = "N:1"

                # pro tabulku i jeste neni zaznam
                else:
                  #  print("klic"+key[-1])
                  #  if (key[-3] is int):
                  #      pass
                  #  else:
                    #    print("table "+table+"key "+key)
                    try:
                        relations[table][key] = "N:1"
                #    print("pridavam key"+key)
                        relations[key]= {}
                        relations[key][table] = "1:N"
                    except KeyError:
                        pass
    tmp = {}
    print(relations)
    while zmena:
        zmena = False
        print("jedu znova")
        printxml(relations)
        for table in relations: # prochazim tabulky
                for fk in relations[table]:# a->b
                    if relations[table][fk] == "N:1": #tranzitivita
                            fk = fk.replace("prk_","").replace("_id","")
                        #if fk in relations: #hledam c->b v druhe tabulce
                            for value in relations[fk]:
                                if relations[fk][value] == "N:1": #tranzitivita
                                    value = value.replace("prk_","").replace("_id","")
                                    if value not in relations[table]:
                                        if table not in tmp:
                                            tmp[table] = {}
                                        tmp[table][value] = "N:1"
                                    
                        #except:
                        #    pass
                    elif relations[table][fk] == "1:N":
                        fk = fk.replace("prk_","").replace("_id","")
                      #if fk in relations: #hledam c->b v druhe tabulce
                        for value in relations[fk]:
                                if relations[fk][value] == "1:N": #tranzitivita
                                    value = value.replace("prk_","").replace("_id","")
                                    if value not in relations[table]:
                                        if table not in tmp:
                                            tmp[table] = {}
                                        tmp[table][value] = "1:N"
                    
                    if relations[table][fk] != "1:1":
                        #print (relations[table][fk])
                        fk = fk.replace("prk_","").replace("_id","")
                        #print (fk)
                      #if fk in relations: #hledam c->b v druhe tabulce
                        for value in relations[fk]:                       
                                if relations[fk][value]: #tranzitivita
                                    if value.replace("prk_","").replace("_id","") not in relations[table]:
                                        value = value.replace("prk_","").replace("_id","")
                                        if table not in tmp:
                                            tmp[table] = {}
                                        if value not in tmp:
                                            tmp[value] = {}
                                        if value != table:
                                            tmp[table][value] = "N:M"
                                            tmp[value][table] = "N:M"
                    
                    
                       
                    
                                    
        print("tmp: "+str(tmp))
        for table in tmp:
                    for fk in tmp[table]:
                        if table in pkfk:
                            if fk in tmp[table]:
                                relations[table][fk] = tmp[table][fk]
                            else:
                                relations[table][fk] = tmp[table][fk]
                        else:
                            relations[table] = {}
                            relations[table][fk] = tmp[table][fk]
        if tmp.keys():
            #print(tmp)
            #print (relations)
            zmena = True
        tmp = {}
        break
     
    #print ("tmp")
    #print (tmp)
      
    """
                print ("\t\t\t"+key)
                if key in tables:
                    relations[table][key] = {"N:M"}
                elif key not in tables:
                    relations[table][key] = {"N:1"}
                else:
                    relations[table][key] = {"1:N"}
    
            
    for relation in relations.keys():
        print (relation)
        print(relations[relation])
    """
    return relations
    

def countFK(root):
    # funkce pro nalezeni maximalniho poctu podelementu jednoho elementu
    # vysledek bude vyuzit pri parametru etc
    for child in root:
        tag = child.tag.lower()
        countone = {}
        for element in child.getchildren():
           childname = element.tag.lower()
           if (childname not in countone.keys()):
                countone[childname] = 1
           else:
                countone[childname] += 1
        #print (counter)
        for i in countone:
            if i not in counter.keys():
                counter[i] = countone[i]
            else:
                if counter[i] < countone[i]:
                    counter[i] = countone[i]
        countFK(child)

    
def getweight(value):
    value = value.replace(" ","")
    if value == "BIT":
        return int(0)
    elif value == "INT":
        return int(10)
    elif value == "FLOAT":
        return int(20)
    elif value =="NVARCHAR":
        return int(30)
    elif value == "NTEXT":
        return int(40)

def gettype(value,attr):
    #print (value)
    if (value == '1') or (value == '0') or (value == '') or (value.lower() == 'true') or (value.lower() == 'false'):
        return "BIT"
    try:
        int(value)
        return "INT"
    except:
        pass
    try:
        float(value)
        return "FLOAT"
    except:
        pass
    if attr:
        return "NVARCHAR"
    else:
        return "NTEXT"

def parsexml(root,args):
    for child in root:
        tag = child.tag.lower()
       # counter = {} #counter of underelements

        if tag not in tables.keys(): # create primary key
            #print (dir(tag))
            tables[tag] = {"prk_"+tag+"_id":" INT PRIMARY KEY"}
            pkfk[tag] = {"prk_"+tag:""}
        #elif "INT PRIMARY KEY" not in tables[tag]:
         #   tables[tag] = {"prk_"+tag+"_id":" INT PRIMARY KEY"}

            
#-----------------------------ATTRIBUTES---------------------------------------#
        if not args.a:  # a do not work with attributes  
            if child.attrib: #create columns from attributes
                for attr in child.attrib.keys():
                    if attr.lower() in tables[tag].keys():
                        #check and change type if lower
                        if getweight(gettype(child.attrib[attr],True)) > getweight(tables[tag][attr.lower()]):
                            tables[tag][attr.lower()] = " "+gettype(child.attrib[attr],True)
                    else:
                        tables[tag][attr.lower()] = " "+gettype(child.attrib[attr],True)
#-----------------------------VALUES-------------------------------------------#

        if child.text and child.text.strip():
            #if "value" in tables[tag].keys(): # not in tables[tag]:
            if 'value' not in tables[tag].keys():
                tables[tag]['value'] = " "+gettype(child.text,False)
                #tables[tag].add("value " + gettype(child.text,False))
            else:
                #print("check"+str(child.text))
                if getweight(gettype(child.text,False)) > getweight(tables[tag]['value']):
                        tables[tag]['value'] = " "+gettype(child.text,False)
#-----------------------------COUNT CHILDREN-----------------------------------#
        """ 
        for underchild in child.getchildren():
            childname = underchild.tag.strip()
            for i in root.findall(childname):
                print ("findall"+i)
            print (counter)
            if (childname not in counter.keys()):
                counter[childname] = 1
            else:
                counter[childname] += 1
        """
#-----------------------------FK-----------------------------------------------#
        for val in child.getchildren():
                val = val.tag
                #print(str(val)+' '+str(counter[val])+' '+str(args.n)))
                #print(args.n)
                if (args.n < 0) or (counter[val] <= int(args.n)):
                    if ((counter[val] == 1 and val+'1' not in tables[tag].keys())) or args.b:
                  #      print (tag+' '+val+'_d')
                        #if "prk_"+val+"_id" in tables[tag]: nejsem si jist
                        #    print("error: colision primary key and foreign key",file=sys.stderr)
                        #   exit(90)
                        tables[tag][val+"_id"] = " INT"
                        pkfk[tag][val] = ""
                    #print (str(counter[val])+" "+str(val))
                    else:
                        while (counter[val] > 0):
                            #pkfk[tag][val] = ""
                            tables[tag][val+str(counter[val])+"_id"] = " INT" # zmena
                            #tables[tag].add(val+str(counter[val])+"_id INT")
                            counter[val] = counter[val] - 1
                    #print (tables[tag])
                else:
                     
                    if (counter[val] > int(args.n)): #pocet podelementu je vetsi nez etc
                        if val not in tables.keys():
                                tables[val] = { "prk_"+val+"_id": " INT PRIMARY KEY" }
                                pkfk[val] = {"prk_"}
                        tables[val][tag+"_id"] = " INT"
                        pkfk[val][tag] = ""
                    
                  
                    else:
                     print ("counter in else"+str(counter[val]))
                     for found in child.findall(val):
                            print (found.tag)
                            if found.tag not in tables.keys():
                                tables[found.tag] = { "prk_"+found.tag+"_id": " INT PRIMARY KEY" }
                            print ("    dd"+str(tables[found.tag]))
                            tables[found.tag][tag+"+id"] = " INT"
                            print ("    po"+str(tables[found.tag]))
                           
    

        if args.g: # xml
            pass

        parsexml(child,args)
                
def printddl(args):
    if args.header:
        print ("--"+args.header)

    for table in tables.keys():
            
        print ("CREATE TABLE " + table+"(")
        pocet = len(tables[table])
        for val in tables[table]:
            if (pocet != 1):
                print ("\t"+str(val)+tables[table][val]+",")
            else:
                print ("\t"+str(val)+tables[table][val])             
            pocet = pocet - 1        
        print (");\n\n")
def printxml(relations):
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print("<tables>")
    for table in relations:
        print('   <table name="'+table+'">')
        for value in relations[table]:
            print('      <relation to="'+str(value.replace("prk_","").replace("_id",""))+'" relation_type="'+str(relations[table][value])+'" />')
    print("</tables>")
        
with open('tests/test03.in',encoding='utf-8') as f:
    file = f.read()
    #print (file)
    #parsed = etree.parse('tests/test03.in')
    parsed = etree.parse('xtd_tests-master/test03.in')
    parsed = etree.parse('xtd_tests-master/testC07.in')
    #parsed = etree.parse('xtd_tests-master/testG01.in')
    #parsed = etree.parse('basic.xml')
    root = parsed.getroot()
    args = makeargs()
    args.n = -10
    countFK(root)
    #print (counter)
    parsexml(root,args)
    #args.b = True
    #args.a = True
    relations = make_relations(tables)
    args.header = 'hlavicka'

    #printddl(args)
    printxml(relations)

