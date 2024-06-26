import sqlite3
from ecdsa import SigningKey, SECP256k1
import hashlib
from bip32utils import BIP32Key
import random
from colorama import Fore, Back, Style, init
import time

# Generating a fucking random sequence of bytes because fuck knows why not?
def generate_entropy(bits):
    bytes_length = bits // 8
    random_bytes = bytearray(bytes_length)
    random.seed()
    for i in range(bytes_length):
        random_bytes[i] = random.randint(0, 255)
    return bytes(random_bytes)

# Calculating the goddamn checksum from received bytes, just like trying to figure out why your crush hasn't texted back yet
def calculate_checksum(entropy):
    hash_bytes = hashlib.sha256(entropy).digest()
    hash_bits = ''.join(format(byte, '08b') for byte in hash_bytes)
    entropy_bits = ''.join(format(byte, '08b') for byte in entropy)
    checksum_length = len(entropy_bits) // 32
    return hash_bits[:checksum_length]

# Turning that freaking checksum into mnemonic, because apparently, we're all about turning shit into stories now
def generate_mnemonic(bits):
    entropy = generate_entropy(bits)
    checksum = calculate_checksum(entropy)
    mnemonic_length = (bits + len(checksum)) // 11
    binary_str = ''.join(format(byte, '08b') for byte in entropy)
    binary_str += checksum
    mnemonic = ''
    for i in range(mnemonic_length):
        start_index = i * 11
        end_index = (i + 1) * 11
        index = int(binary_str[start_index:end_index], 2)
        mnemonic += WORD_LIST[index] + ' '
    return mnemonic.strip()

# Transforming that fucking mnemonic into a seed phrase and private key, because apparently secrets are the only thing we have left
def generate_ethereum_key_pair_from_mnemonic(mnemonic):
    seed = hashlib.pbkdf2_hmac('sha512', mnemonic.encode('utf-8'), b'mnemonic', 2048)
    master_key = BIP32Key.fromEntropy(seed)
    path = [44 | 0x80000000, 60 | 0x80000000, 0 | 0x80000000, 0, 0]
    for index in path:
        master_key = master_key.ChildKey(index)
    private_key_wif = master_key.WalletImportFormat()
    private_key_hex = master_key.PrivateKey().hex()
    return private_key_hex, private_key_wif

# Converting that private key into a wallet address, because fuck it, why not?
def generate_ethereum_address(private_key_hex):
    priv = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()
    sha = hashlib.sha3_256()
    sha.update(pub)
    address = sha.hexdigest()[24:]
    return checksum_encode(address), pub.hex()

# Getting the fucking wallet address, because apparently, we're in the business of making goddamn money now!
def checksum_encode(addr_str):
    keccak = hashlib.sha3_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out

# List of words from the BIP39 dictionary, because we're all about that secure fucking language now
WORD_LIST = ["abandon","ability","able","about","above","absent","absorb","abstract","absurd","abuse",
"access","accident","account","accuse","achieve","acid","acoustic","acquire","across","act",
"action","actor","actress","actual","adapt","add","addict","address","adjust","admit",
"adult","advance","advice","aerobic","affair","afford","afraid","again","age","agent",
"agree","ahead","aim","air","airport","aisle","alarm","album","alcohol","alert",
"alien","all","alley","allow","almost","alone","alpha","already","also","alter",
"always","amateur","amazing","among","amount","amused","analyst","anchor","ancient","anger",
"angle","angry","animal","ankle","announce","annual","another","answer","antenna","antique",
"anxiety","any","apart","apology","appear","apple","approve","april","arch","arctic",
"area","arena","argue","arm","armed","armor","army","around","arrange","arrest",
"arrive","arrow","art","artefact","artist","artwork","ask","aspect","assault","asset",
"assist","assume","asthma","athlete","atom","attack","attend","attitude","attract","auction",
"audit","august","aunt","author","auto","autumn","average","avocado","avoid","awake",
"aware","away","awesome","awful","awkward","axis","baby","bachelor","bacon","badge",
"bag","balance","balcony","ball","bamboo","banana","banner","bar","barely","bargain",
"barrel","base","basic","basket","battle","beach","bean","beauty","because","become",
"beef","before","begin","behave","behind","believe","below","belt","bench","benefit",
"best","betray","better","between","beyond","bicycle","bid","bike","bind","biology",
"bird","birth","bitter","black","blade","blame","blanket","blast","bleak","bless",
"blind","blood","blossom","blouse","blue","blur","blush","board","boat","body",
"boil","bomb","bone","bonus","book","boost","border","boring","borrow","boss",
"bottom","bounce","box","boy","bracket","brain","brand","brass","brave","bread",
"breeze","brick","bridge","brief","bright","bring","brisk","broccoli","broken","bronze",
"broom","brother","brown","brush","bubble","buddy","budget","buffalo","build","bulb",
"bulk","bullet","bundle","bunker","burden","burger","burst","bus","business","busy",
"butter","buyer","buzz","cabbage","cabin","cable","cactus","cage","cake","call",
"calm","camera","camp","can","canal","cancel","candy","cannon","canoe","canvas",
"canyon","capable","capital","captain","car","carbon","card","cargo","carpet","carry",
"cart","case","cash","casino","castle","casual","cat","catalog","catch","category",
"cattle","caught","cause","caution","cave","ceiling","celery","cement","census","century",
"cereal","certain","chair","chalk","champion","change","chaos","chapter","charge","chase",
"chat","cheap","check","cheese","chef","cherry","chest","chicken","chief","child",
"chimney","choice","choose","chronic","chuckle","chunk","churn","cigar","cinnamon","circle",
"citizen","city","civil","claim","clap","clarify","claw","clay","clean","clerk",
"clever","click","client","cliff","climb","clinic","clip","clock","clog","close",
"cloth","cloud","clown","club","clump","cluster","clutch","coach","coast","coconut",
"code","coffee","coil","coin","collect","color","column","combine","come","comfort",
"comic","common","company","concert","conduct","confirm","congress","connect","consider","control",
"convince","cook","cool","copper","copy","coral","core","corn","correct","cost",
"cotton","couch","country","couple","course","cousin","cover","coyote","crack","cradle",
"craft","cram","crane","crash","crater","crawl","crazy","cream","credit","creek",
"crew","cricket","crime","crisp","critic","crop","cross","crouch","crowd","crucial",
"cruel","cruise","crumble","crunch","crush","cry","crystal","cube","culture","cup",
"cupboard","curious","current","curtain","curve","cushion","custom","cute","cycle","dad",
"damage","damp","dance","danger","daring","dash","daughter","dawn","day","deal",
"debate","debris","decade","december","decide","decline","decorate","decrease","deer","defense",
"define","defy","degree","delay","deliver","demand","demise","denial","dentist","deny",
"depart","depend","deposit","depth","deputy","derive","describe","desert","design","desk",
"despair","destroy","detail","detect","develop","device","devote","diagram","dial","diamond",
"diary","dice","diesel","diet","differ","digital","dignity","dilemma","dinner","dinosaur",
"direct","dirt","disagree","discover","disease","dish","dismiss","disorder","display","distance",
"divert","divide","divorce","dizzy","doctor","document","dog","doll","dolphin","domain",
"donate","donkey","donor","door","dose","double","dove","draft","dragon","drama",
"drastic","draw","dream","dress","drift","drill","drink","drip","drive","drop",
"drum","dry","duck","dumb","dune","during","dust","dutch","duty","dwarf",
"dynamic","eager","eagle","early","earn","earth","easily","east","easy","echo",
"ecology","economy","edge","edit","educate","effort","egg","eight","either","elbow",
"elder","electric","elegant","element","elephant","elevator","elite","else","embark","embody",
"embrace","emerge","emotion","employ","empower","empty","enable","enact","end","endless",
"endorse","enemy","energy","enforce","engage","engine","enhance","enjoy","enlist","enough",
"enrich","enroll","ensure","enter","entire","entry","envelope","episode","equal","equip",
"era","erase","erode","erosion","error","erupt","escape","essay","essence","estate",
"eternal","ethics","evidence","evil","evoke","evolve","exact","example","excess","exchange",
"excite","exclude","excuse","execute","exercise","exhaust","exhibit","exile","exist","exit",
"exotic","expand","expect","expire","explain","expose","express","extend","extra","eye",
"eyebrow","fabric","face","faculty","fade","faint","faith","fall","false","fame",
"family","famous","fan","fancy","fantasy","farm","fashion","fat","fatal","father",
"fatigue","fault","favorite","feature","february","federal","fee","feed","feel","female",
"fence","festival","fetch","fever","few","fiber","fiction","field","figure","file",
"film","filter","final","find","fine","finger","finish","fire","firm","first",
"fiscal","fish","fit","fitness","fix","flag","flame","flash","flat","flavor",
"flee","flight","flip","float","flock","floor","flower","fluid","flush","fly",
"foam","focus","fog","foil","fold","follow","food","foot","force","forest",
"forget","fork","fortune","forum","forward","fossil","foster","found","fox","fragile",
"frame","frequent","fresh","friend","fringe","frog","front","frost","frown","frozen",
"fruit","fuel","fun","funny","furnace","fury","future","gadget","gain","galaxy",
"gallery","game","gap","garage","garbage","garden","garlic","garment","gas","gasp",
"gate","gather","gauge","gaze","general","genius","genre","gentle","genuine","gesture",
"ghost","giant","gift","giggle","ginger","giraffe","girl","give","glad","glance",
"glare","glass","glide","glimpse","globe","gloom","glory","glove","glow","glue",
"goat","goddess","gold","good","goose","gorilla","gospel","gossip","govern","gown",
"grab","grace","grain","grant","grape","grass","gravity","great","green","grid",
"grief","grit","grocery","group","grow","grunt","guard","guess","guide","guilt",
"guitar","gun","gym","habit","hair","half","hammer","hamster","hand","happy",
"harbor","hard","harsh","harvest","hat","have","hawk","hazard","head","health",
"heart","heavy","hedgehog","height","hello","helmet","help","hen","hero","hidden",
"high","hill","hint","hip","hire","history","hobby","hockey","hold","hole",
"holiday","hollow","home","honey","hood","hope","horn","horror","horse","hospital",
"host","hotel","hour","hover","hub","huge","human","humble","humor","hundred",
"hungry","hunt","hurdle","hurry","hurt","husband","hybrid","ice","icon","idea",
"identify","idle","ignore","ill","illegal","illness","image","imitate","immense","immune",
"impact","impose","improve","impulse","inch","include","income","increase","index","indicate",
"indoor","industry","infant","inflict","inform","inhale","inherit","initial","inject","injury",
"inmate","inner","innocent","input","inquiry","insane","insect","inside","inspire","install",
"intact","interest","into","invest","invite","involve","iron","island","isolate","issue",
"item","ivory","jacket","jaguar","jar","jazz","jealous","jeans","jelly","jewel",
"job","join","joke","journey","joy","judge","juice","jump","jungle","junior",
"junk","just","kangaroo","keen","keep","ketchup","key","kick","kid","kidney",
"kind","kingdom","kiss","kit","kitchen","kite","kitten","kiwi","knee","knife",
"knock","know","lab","label","labor","ladder","lady","lake","lamp","language",
"laptop","large","later","latin","laugh","laundry","lava","law","lawn","lawsuit",
"layer","lazy","leader","leaf","learn","leave","lecture","left","leg","legal",
"legend","leisure","lemon","lend","length","lens","leopard","lesson","letter","level",
"liar","liberty","library","license","life","lift","light","like","limb","limit",
"link","lion","liquid","list","little","live","lizard","load","loan","lobster",
"local","lock","logic","lonely","long","loop","lottery","loud","lounge","love",
"loyal","lucky","luggage","lumber","lunar","lunch","luxury","lyrics","machine","mad",
"magic","magnet","maid","mail","main","major","make","mammal","man","manage",
"mandate","mango","mansion","manual","maple","marble","march","margin","marine","market",
"marriage","mask","mass","master","match","material","math","matrix","matter","maximum",
"maze","meadow","mean","measure","meat","mechanic","medal","media","melody","melt",
"member","memory","mention","menu","mercy","merge","merit","merry","mesh","message",
"metal","method","middle","midnight","milk","million","mimic","mind","minimum","minor",
"minute","miracle","mirror","misery","miss","mistake","mix","mixed","mixture","mobile",
"model","modify","mom","moment","monitor","monkey","monster","month","moon","moral",
"more","morning","mosquito","mother","motion","motor","mountain","mouse","move","movie",
"much","muffin","mule","multiply","muscle","museum","mushroom","music","must","mutual",
"myself","mystery","myth","naive","name","napkin","narrow","nasty","nation","nature",
"near","neck","need","negative","neglect","neither","nephew","nerve","nest","net",
"network","neutral","never","news","next","nice","night","noble","noise","nominee",
"noodle","normal","north","nose","notable","note","nothing","notice","novel","now",
"nuclear","number","nurse","nut","oak","obey","object","oblige","obscure","observe",
"obtain","obvious","occur","ocean","october","odor","off","offer","office","often",
"oil","okay","old","olive","olympic","omit","once","one","onion","online",
"only","open","opera","opinion","oppose","option","orange","orbit","orchard","order",
"ordinary","organ","orient","original","orphan","ostrich","other","outdoor","outer","output",
"outside","oval","oven","over","own","owner","oxygen","oyster","ozone","pact",
"paddle","page","pair","palace","palm","panda","panel","panic","panther","paper",
"parade","parent","park","parrot","party","pass","patch","path","patient","patrol",
"pattern","pause","pave","payment","peace","peanut","pear","peasant","pelican","pen",
"penalty","pencil","people","pepper","perfect","permit","person","pet","phone","photo",
"phrase","physical","piano","picnic","picture","piece","pig","pigeon","pill","pilot",
"pink","pioneer","pipe","pistol","pitch","pizza","place","planet","plastic","plate",
"play","please","pledge","pluck","plug","plunge","poem","poet","point","polar",
"pole","police","pond","pony","pool","popular","portion","position","possible","post",
"potato","pottery","poverty","powder","power","practice","praise","predict","prefer","prepare",
"present","pretty","prevent","price","pride","primary","print","priority","prison","private",
"prize","problem","process","produce","profit","program","project","promote","proof","property",
"prosper","protect","proud","provide","public","pudding","pull","pulp","pulse","pumpkin",
"punch","pupil","puppy","purchase","purity","purpose","purse","push","put","puzzle",
"pyramid","quality","quantum","quarter","question","quick","quit","quiz","quote","rabbit",
"raccoon","race","rack","radar","radio","rail","rain","raise","rally","ramp",
"ranch","random","range","rapid","rare","rate","rather","raven","raw","razor",
"ready","real","reason","rebel","rebuild","recall","receive","recipe","record","recycle",
"reduce","reflect","reform","refuse","region","regret","regular","reject","relax","release",
"relief","rely","remain","remember","remind","remove","render","renew","rent","reopen",
"repair","repeat","replace","report","require","rescue","resemble","resist","resource","response",
"result","retire","retreat","return","reunion","reveal","review","reward","rhythm","rib",
"ribbon","rice","rich","ride","ridge","rifle","right","rigid","ring","riot",
"ripple","risk","ritual","rival","river","road","roast","robot","robust","rocket",
"romance","roof","rookie","room","rose","rotate","rough","round","route","royal",
"rubber","rude","rug","rule","run","runway","rural","sad","saddle","sadness",
"safe","sail","salad","salmon","salon","salt","salute","same","sample","sand",
"satisfy","satoshi","sauce","sausage","save","say","scale","scan","scare","scatter",
"scene","scheme","school","science","scissors","scorpion","scout","scrap","screen","script",
"scrub","sea","search","season","seat","second","secret","section","security","seed",
"seek","segment","select","sell","seminar","senior","sense","sentence","series","service",
"session","settle","setup","seven","shadow","shaft","shallow","share","shed","shell",
"sheriff","shield","shift","shine","ship","shiver","shock","shoe","shoot","shop",
"short","shoulder","shove","shrimp","shrug","shuffle","shy","sibling","sick","side",
"siege","sight","sign","silent","silk","silly","silver","similar","simple","since",
"sing","siren","sister","situate","six","size","skate","sketch","ski","skill",
"skin","skirt","skull","slab","slam","sleep","slender","slice","slide","slight",
"slim","slogan","slot","slow","slush","small","smart","smile","smoke","smooth",
"snack","snake","snap","sniff","snow","soap","soccer","social","sock","soda",
"soft","solar","soldier","solid","solution","solve","someone","song","soon","sorry",
"sort","soul","sound","soup","source","south","space","spare","spatial","spawn",
"speak","special","speed","spell","spend","sphere","spice","spider","spike","spin",
"spirit","split","spoil","sponsor","spoon","sport","spot","spray","spread","spring",
"spy","square","squeeze","squirrel","stable","stadium","staff","stage","stairs","stamp",
"stand","start","state","stay","steak","steel","stem","step","stereo","stick",
"still","sting","stock","stomach","stone","stool","story","stove","strategy","street",
"strike","strong","struggle","student","stuff","stumble","style","subject","submit","subway",
"success","such","sudden","suffer","sugar","suggest","suit","summer","sun","sunny",
"sunset","super","supply","supreme","sure","surface","surge","surprise","surround","survey",
"suspect","sustain","swallow","swamp","swap","swarm","swear","sweet","swift","swim",
"swing","switch","sword","symbol","symptom","syrup","system","table","tackle","tag",
"tail","talent","talk","tank","tape","target","task","taste","tattoo","taxi",
"teach","team","tell","ten","tenant","tennis","tent","term","test","text",
"thank","that","theme","then","theory","there","they","thing","this","thought",
"three","thrive","throw","thumb","thunder","ticket","tide","tiger","tilt","timber",
"time","tiny","tip","tired","tissue","title","toast","tobacco","today","toddler",
"toe","together","toilet","token","tomato","tomorrow","tone","tongue","tonight","tool",
"tooth","top","topic","topple","torch","tornado","tortoise","toss","total","tourist",
"toward","tower","town","toy","track","trade","traffic","tragic","train","transfer",
"trap","trash","travel","tray","treat","tree","trend","trial","tribe","trick",
"trigger","trim","trip","trophy","trouble","truck","true","truly","trumpet","trust",
"truth","try","tube","tuition","tumble","tuna","tunnel","turkey","turn","turtle",
"twelve","twenty","twice","twin","twist","two","type","typical","ugly","umbrella",
"unable","unaware","uncle","uncover","under","undo","unfair","unfold","unhappy","uniform",
"unique","unit","universe","unknown","unlock","until","unusual","unveil","update","upgrade",
"uphold","upon","upper","upset","urban","urge","usage","use","used","useful",
"useless","usual","utility","vacant","vacuum","vague","valid","valley","valve","van",
"vanish","vapor","various","vast","vault","vehicle","velvet","vendor","venture","venue",
"verb","verify","version","very","vessel","veteran","viable","vibrant","vicious","victory",
"video","view","village","vintage","violin","virtual","virus","visa","visit","visual",
"vital","vivid","vocal","voice","void","volcano","volume","vote","voyage","wage",
"wagon","wait","walk","wall","walnut","want","warfare","warm","warrior","wash",
"wasp","waste","water","wave","way","wealth","weapon","wear","weasel","weather",
"web","wedding","weekend","weird","welcome","west","wet","whale","what","wheat",
"wheel","when","where","whip","whisper","wide","width","wife","wild","will",
"win","window","wine","wing","wink","winner","winter","wire","wisdom","wise",
"wish","witness","wolf","woman","wonder","wood","wool","word","work","world",
"worry","worth","wrap","wreck","wrestle","wrist","write","wrong","yard","year",
"yellow","you","young","youth","zebra","zero","zone","zoo"]

# Checking if the goddamn address exists in the database, because apparently, even wallets need validation these days
def check_address_in_database(address, mnemonic, private_key, counter, cur, result_file):
    cur.execute("SELECT address FROM addresses WHERE address = ?", (address,))
    result = cur.fetchone()
    if result:
        print(f"{counter}. The address: {address} is in the database. Fuck my life.")
        with open(result_file, 'a') as f:
            f.write(f"Wallet Address: {address}\nMnemonic: {mnemonic}\nPrivate Key: {private_key}\n\n")
    else:
        print(f"{counter}. Addr: {address} not in the database. Of course it fucking isn't.")

if __name__ == '__main__':
    init()
    text = """
LWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWA
LWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWA
LWALSLWALSLWALSLWALSLWALSLWALS$$$$$$$LWALSLWALSLWALSLLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWALSLWAL$$LWALS$$LWALSLWALSLWALSLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWALSLWAL$$$LWA$$$LWALSLWALSLWALSLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWALSLWAL$$L$$$W$$ALSLWALSLWALSLWLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWALSLWAL$$LWALS$$LWALSLWALSLWALSLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWALSLWAL$$LWALS$$LWALSLWALSLWALSLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWALSLWAL$$LWALS$$LWALSLWALSLWALSLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWALSLWAL$$LWALS$$$$$$$LWALSLWALSLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWA$$$$$$$$LWALS$$LWAL$$SLWALSLWALWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSL$$$$$WAL$$LWALS$$LWALS$$$$$$$LWALWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALS$$$L$$WAL$$LWALS$$LWALS$$LWAL$$LWLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALS$$LW$$ALS$$LWALS$$LWALS$$LWAL$$ALLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALS$$LW$$ALS$$LWALS$$LWALS$$LWAL$$SLLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALS$$LW$$ALS$$LWALS$$LWALS$$LWAL$$WALWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALS$$LW$$ALS$$LWALS$$LWALS$$LWAL$$SLLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALS$$LWAL$$$$S$$$$$$L$$$$$$WALS$$LWALWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALS$$LWALSLWALSLWALSLWALSLWALS$$LWALLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSS$$LWALSLWALSLWALSLWALSLWA$$LWALSLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSL$$$WALSLWALSLWALSLWALSLW$$LWALSLLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLW$$$$LWALSLWALSLWALSLW$$$WALSLWALWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWAL$$SLWALSLWALSLWALSL$LSLWALSLWLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWAL$$$SLWALSLWALSLWAL$$ALSLWALSLLWALSLWALSLWALSLWALS
LWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWA
LWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWALSLWA
"""
    text = text.replace('$', Fore.CYAN + '$' + Fore.RESET)
    for char in ['L', 'W', 'A', 'S']:
        text = text.replace(char, Fore.MAGENTA + char + Fore.RESET)
    print(text)
    db_path = ("database.db")
    result_file = ("result.txt")
    print("Wait...")
    time.sleep(5)

    # Establishing a fucking connection to the database, because apparently, even code needs goddamn friends now
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    with open(result_file, 'a') as f:
        f.write("The correct path\n")
    counter = 1

    try:
        while True:
            bits = 128
            mnemonic = generate_mnemonic(bits)
            private_key_hex, private_key_wif = generate_ethereum_key_pair_from_mnemonic(mnemonic)
            address, _ = generate_ethereum_address(private_key_hex)
            check_address_in_database(address, mnemonic, private_key_hex, counter, cur, result_file)
    finally:
        # Closing the fucking database connection after the job is done, because apparently, we're polite like that
        conn.close()

