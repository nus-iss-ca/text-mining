# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 13:02:48 2015

@author: akshay
"""
from lib.util import *

util = Util()
#Reading Input File
df = pd.read_csv('result/1_osha_filter_scrapper.csv')

list=df.ix[0:,2]
occ_list=[]

stop = util.stopwords
#New stop words added
additional_stop_list = ['employer','container','water','boiler','barrier','trimmer','outdoor','hammer','elevator','helicopter','power',
'reactor','motor','escavator','chamber','paper','blower','door','shoulder','fiber','bulldozer','cover','computer','giver',
'cutter','scissor','tanker','closer','member','man','upper','steer','subfloor','interior','conveyor','number','rubber','bumper',
'master','tractor','polyester','boulder','lever','floor','compressor','21inchdiameter','preheater','indoor','30indiameter','refrigerator','carrier','detonator','ladder',
'ladder','exterior','tower','bladder','tower','stater','crusher','slicer','starter','senior','mower','baler','auger','powder','odor','other','cinder','sensor','mixer',
'vapor','galvanometer','blaster','trucktractor','tractortrailer','receiver','chipper','boilermaker','dishwasher','default','order','man','operator',
'truck','either','trimmer','center','meter','threeman','diameter','hopper','finger','number','heater','manufacturer','condenser','roller','respirator','customer','generator','stepladder','examiner','december','november','october','september',
'transformer','zipper','leftover','hyster','collector','cylinder','laser','enter','proper','freezer','outer','monitor','super','manner',
'andor','river','pusher','lighter','remember','twoman','inner','smaller','color','liver','layer','calender','sorter','liver','pioneer','danger','evaporator','riser',
'recover','indicator','pier','server','radiator','upriver','transfer','factor','crawler','copper','waether','counter','separator','shower','coker','workover',
'alligator','perimeter','cooler','ranger','offcenter','poor','dockdoor','door','waterpower','manipulator','together','hoter','bdoor','feeler','autoleather',
'containertailer','dinner','voltmeter','behavior','partner','winter','summer','sucker','sandpaper','thinner','chiller','miter','remainder','regulator',
'thirdfloor','horsepower','rotor','sprinkler','corner','weather','secondfloor','plaster','trigger','tier','longer','minor','gutter','outrigger','choker','coffer','primer','adapter','screwdriver','er','median','brother','spider',
'extinguisher','capacitor','answer',
'insulator','longer','vaibrator','bunker','hanger','escalator','however','corridor','lower','underwater','fastener','booster','trailer', 'compactor', 'dumpster', 'girder', 'spreader',
'lacquer', 'werner', 'kaiser','uncover', 'solder', 'dumper', 'timber', 'oiler', 'sealer','whaler', 'wastewater', 'carburetor', 'vibrator', 'erector', 'picker','taper','sewerwater,'
'marker', 'absorber','firstfloor', 'maneuver', 'chocker',  'lather','pedestrian', 'tensioner','exchanger','badger', 'precipitator', 'improper', 'ether',
'rollercompactor','teeter','deadman', 'shaker', 'estimator','lasher', 'trencher', 'incinerator','cotter','connector', 'dozer','dormer','jackhammer','harbor','conditioner','skidsteer','stringer','rafter','liner','greater','mirror','sandblaster',
'marker','sewerwater','header','beer','blocker','fever','rollover','equalizer','snooper','consider','connector','finisher','scraper','grader','anchor','lumber','grinder']
#removing more stop words using my list
stop.extend(additional_stop_list)

#Reading each paragraph to fetch occupation
for i in list[0:]:
    occ_list1 = []
    #normalize text
    ntext=i.encode('ascii','ignore')
    #removed puntuation marks
    text_nopunc=ntext.translate(string.maketrans("",""), string.punctuation)
    #lowering all text
    text_lower=text_nopunc.lower()
    #removing all english stop words
    text_nostop=" ".join(filter(lambda word: word not in stop, text_lower.split()))
    #doing pos tagging
    pos1 = pos_tag(wt(text_nostop))
    #taking only NN words to analysis Occupation
    text1= [word for word, pos in pos1 if (pos == 'NN')]

    # Fetching only words ending with er,or,ian,man,men
    regex1=re.compile(".*(er$)|.*(or$)|.*(ian$)|.*(anic$)|.*(man$)|.*(men$)")

    empolypee=['worker','supervisor','driver','laborer','contractor','foreman','owner','carpenter','technician','manager','welder','excavator','painter',
                   'conductor','sewer','lumber','engineer','journeyman','labor','electrician','subcontractor','helper','mechanic',
                   'driller','officer','washer','instructor','lineman','brakeman','painter', 'inspector','ironworker', 'cleaner','rider','lineman',
                   'plumber','flagman','fabricator','builder','repairman','caster','warehouseman','signalman','groundsman','pipefitter','motorman','controller',
                   'presser','fireman','framer','landscaper','dealer','pressman','craftsman','derdger','technician','mechanic','fencer','operator','ironwroker',
                   'landscaper','decorator','pipefitter','fixer','steelfixer','welder','waterproofer','worker','sitemanager','Site Manager','material handler',
                   'engineer','architect','civilman','plasterer','pile driver','rigger']

   #First, we check with exhaustive list made for construction occupation
    for i in text1:
        is_break = False
        for a in empolypee:
            if(i==a):
                occ_list1=i
                occ_list.append(occ_list1)
                is_break = True
                break
        if is_break: break
    # If occupation not found in list then using regular expression which used er,or,anic words to fetch as occupation
    print occ_list1
    if occ_list1==[]:
        occ_list1=[m.group(0) for l in text1 for m in [regex1.search(l)] if m]
        if not occ_list1:
             occ_list1=["no_occupation"]
        occ_list.append(occ_list1[0])

#Output all fetched occupation in Output
dd = df.ix[0:,0:3]
dd['Occupation'] = pd.Series(occ_list, index=df.index)
dd.to_csv('result/4_question3.csv', index = False)

print "Final List"
print occ_list

#Word cloud
counts = collections.Counter(occ_list)
temp_obj = counts.most_common(100)

max_count = max(temp_obj, key=operator.itemgetter(1))[1]
temp_obj = [(name, count / float(max_count))for name, count in temp_obj]
temp_obj.pop(0) # remove "no_occupation"

word_cloud = WordCloud(font_path="fonts/Georgia.ttf",
    width=1280, height=800, max_words=100, stopwords=stop)
word_cloud.fit_words(temp_obj)
word_cloud.to_file("result/4_question3.png")
print("========DONE==========")
