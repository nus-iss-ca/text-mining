from lib.util import *
from collections import Counter

util = Util()

# --load msia data
msia_data = pd.read_excel("data/MsiaAccidentCases.xlsx", "MsiaAccidentCases-cleaned")
msia_data.columns = ['cause', 'title', 'summary'] # rename columns
msia_columns = ['title','summary']
# --load osha data
osha_data = pd.read_excel("data/osha.xlsx", "out_title")
osha_data.columns = ['id', 'title', 'summary'] # rename columns

dictionary = ["access","accompanied","admitted","afterwards","agent","airconditioner","aluminium","aluminum","anticlockwise","area","assigned","assistance","assisted","attempt",
"attempted","bag","balance","balanced","balcony","barge","barrel","barrier","batching","bay","belt","bin","binding","block","blow","board","boarding","bottom","box","brake",
"breaking","brick","bringing","brought","bucket","building","bulldozer","bundle","buried","burying","cabin","cable","cage","calibrator","carried","carry","carrying","caught",
"cement","chain","chainsaw","change","checking","circuit","citizen","cladding","climb","climbed","climber","climbing","close","closed","closing","coal","collapsed","collect",
"collecting","collision","column","coming","complained","completing","completion","concreting","condition","conditioner","conditioning","conduct","cone","confined","confirmed",
"connection","construction","container","containing","contractor","control","controlling","conveyor","copper","counterweight","cover","coworkers","crane","craned","crash",
"crashed","crawler","cross","crossing","crushed","crusher","crushing","curtain","cut","cutter","cutting","designated","designed","diesel","digged","disintegrated","dismantling",
"district","ditch","divider","diving","division","done","door","downhill","downwards","drain","drainage","drawbar","drilling","drowned","drum","dug","earth","electrocuted",
"electrocution","eletricity","elevator","emergency","entered","entering","entrance","escalator","estate","excavation","excavator","excessive","exploded","explosion","facilitate",
"factory","failed","fainting","fall","fallen","falling","falsework","fan","fell","fiber","finished","finishing","fire","fixing","flagman","floor","following","foot","form",
"front","furnace","gantry","gate","ground","grounding","guard","gush","gust","hall","hanging","height","helmet","highway","hill","holding","hook","hot","house","inhabited",
"inside","instability","install","installation","installed","installing","instructed","intention","involved","involving","iron","kg","ladder","land","landing","landslide",
"lawnmower","level","leveling","levelling","lift","lifted","lifting","light","lightning","line","load","loaded","loading","located","lorry","lowered","lug","machine",
"machinery","magnet","maintain","maintenance","malfunctioned","material","measured","metal","mining","move","movement","moving","noted","noticed","office","oil","opened",
"opening","operation","operator","outside","overtake","overturned","pane","part","passenger","patching","path","pavement","perform","performing","piece","pile","piling","pinned",
"pipe","pipeline","pit","place","placed","placing","plant","plantation","plastic","platform","plug","plunged","plywood","position","pothole","preparation","prepared",
"problem","process","processing","product","progress","project","pronounced","protection","pulled","pulling","pump","pumped","pumping","pushing","raised","reaching","receiving",
"reconstruction","release","removal","removing","renovating","renovation","repair","repairing","replacement","replacing","reported","reserve","resident","return","revealed",
"reversed","reversing","riding","road","rock","rod","roll","rolled","roller","roof","rooftop","room","rope","rubber","safety","sand","sanding","scaffold","scaffolding","schedule",
"school","scraping","screw","seal","section","security","segment","selling","separation","series","shaft","shovel","shoveler","shoveling","side","sign","site","situated","size",
"skidded","skylift","slab","sliding","slip","slipped","slipping","slope","sludge","spanner","spinning","splash","spot","spraying","spread","stair","standing","steel","steep",
"steering","stone","stop","stopped","storage","store","street","striking","struck","structure","stuck","subcontractor","supervisor","support","surrounding","suspended","sway",
"tag","tagging","tank","telephone","tied","tile","tilt","timber","tire","tonne","topple","toppled","towards","towed","tower","toxic","tractor","train","transfering","transferring",
"transformer","trapped","traversed","treatment","tree","trench","truck","truss","tube","tubing","tyre","unchained","undergoing","undertaking","unloading","upgrading","uphill",
"utility","valve","vehicle","wagon","walking","wall","warehouse","water","way","wear","weighing","weight","welder","welding","went","wheel","wide","winch","wind","window","wire","wiring",
"wood","wooden","work","worked","worker","working","workplace","worn"]

# --create classifier based on dictionary to identify class Construction or not
class_construction = Construction(dictionary)

# --preprocessing osha data
osha_data_processed = util.preprocessing(osha_data, msia_columns)
# osha_combine = osha_data_processed['title'] + " " + osha_data_processed['summary']

# --count words' class (Construction/Other) in each row, if row has at least 20 words belong to Construction class, save it
for index, row in osha_data_processed.iterrows():
	tmp = wt(util.lemmatize(wt(row["summary"]))) # tokenize string before assign class to each word
	temp_array = class_construction.get_construction_category(tmp)
	counter = Counter(temp_array)
	if counter['Construction'] < 20:
		osha_data = osha_data.drop(index)

osha_data.to_csv('result/1_osha_filter_dictionary.csv', index=False)
print "========DONE=========="
