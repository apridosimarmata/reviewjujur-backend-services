from cassandra.cluster import Cluster
from cassandra.query import dict_factory

from functions import *

cluster = Cluster(['172.17.0.3'])
session = cluster.connect('fingerprint')
session.row_factory = dict_factory

phone_ids = session.execute('SELECT phone_id FROM fingerprints')
phone_ids_unique = set()

for value in phone_ids:
    phone_ids_unique.add(value.get('phone_id'))

phone_fingerprints = {}

fingerprints = session.execute('SELECT * FROM fingerprints')

for fingerprint in fingerprints:
    try:
        phone_fingerprints[fingerprint.get('phone_id')].append(fingerprint)
    except:
        phone_fingerprints[fingerprint.get('phone_id')] = [fingerprint]


unknown_fingerprint = {'available_ringtones': 'AcousticGuitar,Andromeda,Aquila,ArgoNavis,Atria,Backroad,BeatPlucker,BellPhone,BentleyDubs,BigEasy,BirdLoop,Blues,Bollywood,Boötes,Breeze,BusaMove,Cairo,CalypsoSteel,Candy,CanisMajor,CaribbeanIce,Carina,Carousel,Cassiopeia,Celesta,Centaurus,ChampagneEdition,Childhood,ChimeyPhone,ClubCubano,Country,Cowboy,CrayonRock,CrazyDream,CurveBallBlend,Cygnus,DancinFool,DigitalPhone,Ding,DonMessWivIt,Draco,DreamTheme,EasternSky,Echo,EntertheNexus,Eridani,EtherShake,Fairyland,Fantasy,FieldTrip,FluteyPhone,FreeFlight,FriendlyGhost,FunkYall,GameOverGuitar,GimmeMoTown,Girtab,GlacialGroove,Glee,Glockenspiel,Growl,HalfwayHome,Hydra,IceLatte,InsertCoin,Kuma,Kungfu,Lollipop,LoopyLounge,LoveFlute,Lyra,Machina,MedievalJaunt,Mi,MiHouse,MiJazz,MildlyAlarming,MiMix2,MiRemix,MountainSpring,Nairobi,Nassau,NewPlayer,NoLimits,NoiseyOne,Orange,OrganDub,Orion,ParadiseIsland,Pegasus,Perseus,Playa,Pyxis,Raindrops,Rasalas,Revelation,Rigel,RoadTrip,RomancingTheTone,Safari,Savannah,Scarabaeus,Sceptrum,Seville,ShesAllThat,SilkyWay,SitarVersusSitar,Solarium,SpaceAge,SpringyJalopy,SteppinOut,Sunrise,Terminated,TerribleTwos,Testudo,Themos,ThirdEye,ThrillerThree,Thunderfoot,ToyRobot,TwirlAway,UrsaMinor,VeryAlarmed,Vespa,Vigor,World,Zeta', 'external_storage_capacity': '299892736', 'input_methods': 'com.baidu.simeji.SimejiIME,com.android.inputmethod.latin.LatinIME,com.google.android.voicesearch.ime.VoiceInputMethodService', 'is_password_shown': '1', 'kernel_name': '[Linux localhost 4.14.190-perf-gd847327c934e-dirty #2 SMP PREEMPT Mon Dec 20 20:59:57 WIB 2021 aarch64]', 'location_providers': 'false,false', 'phone_id': 'f7c34872d87a3afd', 'ringtone': 'Tidak Ada', 'screen_timeout': '2147483647', 'wallpaper': 'd41d8cd98f00b204e9800998ecf8427e', 'wifi_policy': '2'}

max_ringtone_similarity = 0

max_similarity = 0

for phone in phone_fingerprints.keys():
    # List type

    # Available ringtones
    ringtone_similarity = jaccard_index(set(unknown_fingerprint.get('available_ringtones').split(',')), set(phone_fingerprints[phone][-1].get('available_ringtones').split(',')))
    if ringtone_similarity > max_ringtone_similarity:
        max_ringtone_similarity = ringtone_similarity
        #print(f'[AVAILABLE RINGTONES] It seems that this phone is {phone} with probability {max_ringtone_similarity}')
    

    # String type

    # Wallpaper
    if unknown_fingerprint.get('wallpaper') == phone_fingerprints[phone][-1].get('wallpaper'):
        #print(f'[WALLPAPER] It seems that this phone is {phone}')
        pass
    
    # Kernel
    if unknown_fingerprint.get('kernel_name') == phone_fingerprints[phone][-1].get('kernel_name'):
        #print(f'[KERNEL NAME] It seems that this phone is {phone}')
        pass
    
    # External storage
    ext
    if unknown_fingerprint.get('external_storage_capacity') != phone_fingerprints[phone][-1].get('external_storage_capacity'):
        #print(f'[EXTERNAL STORAGE CAPACITY] It seems that this phone is {phone}')
        number_string_extract_probabilities(phone, 'external_storage_capacity', phone_fingerprints).get('phone_probability')
    else:
        number_string_extract_probabilities(phone, 'external_storage_capacity', phone_fingerprints).get('phone_probability')
    
    # Input methods
    if unknown_fingerprint.get('input_methods') == phone_fingerprints[phone][-1].get('input_methods'):
        #print(f'[INPUT METHODS] It seems that this phone is {phone}')
        pass
    
    # Ringtone
    if unknown_fingerprint.get('ringtone') == phone_fingerprints[phone][-1].get('ringtone'):
        pass
        #print(f'[RINGTONE] It seems that this phone is {phone}')
    
    # Number / Int

    # Screen time out
    if unknown_fingerprint.get('screen_timeout') == phone_fingerprints[phone][-1].get('screen_timeout'):
        #print(f'[SCREEN TIMEOUT] It seems that this phone is {phone}')
        pass
    

print(max_external_storage)

    
