import re,json,zipfile,shutil,argparse
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('atlas');p.add_argument('package');p.add_argument('out');a=p.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(a.package) as z:z.extractall(out)
atlas=Image.open(a.atlas).convert('RGBA')
assert atlas.width==atlas.height
cell=atlas.width/8
sprites=[atlas.crop(tuple(round(v) for v in (c*cell,r*cell,(c+1)*cell,(r+1)*cell))).resize((24,24),Image.Resampling.LANCZOS) for r in range(8) for c in range(8)]
root=out/'data/images/orig24';root.mkdir(parents=True,exist_ok=True)
text=(out/'data_free/game_config/tiles.txt').read_text()
# Parse top-level records while respecting nested braces and quoted strings.
records=[];depth=0;start=0;quoted=False;escape=False
for i,ch in enumerate(text):
 if escape:escape=False;continue
 if ch=='\\' and quoted:escape=True;continue
 if ch=='"':quoted=not quoted
 if not quoted:
  if ch=='{':
   if depth==0:start=i
   depth+=1
  elif ch=='}':
   depth-=1
   if depth==0:records.append(text[start:i+1])
def family(name,symbol=''):
 n=name.lower()
 rules=[('grass|meadow',0),('sand|desert',6),('snow|ice',5),('lava|magma',4),('water|river|lake|ocean',3),('stairs.*up|up_stair',15),('stairs|staircase|ladder|entrance',14),('pine|fir_tree',9),('dead_tree|burnt_tree',10),('tree|trunk',8),('bush|flower|crop|wheat|mushroom',11),('iron_door|steel_door',13),('door|gate',12),('wall|mountain|rock|granite|brick|roof',7),('floor|road|bridge|pavement|path|stone',2),('dirt|mud|earth|soil',1),('adamantium|adoxium|crystal|infernite',55),('gold_ore',57),('ore|iron|coal',54),('wood|log|plank',56),('keeper_knight|black_knight',17),('keeper|witch|warlock',16),('imp',18),('goblin',19),('orc',20),('ogre|cyclop|giant|troll',21),('skeleton|bone',22),('zombie|mummy|corpse',23),('vampire',24),('dragon|wyvern|drake',25),('wolf|dog|fox',26),('bear|boar|pig|bison|cow',27),('spider|scorpion|ant|insect|beetle',28),('chicken|bird|raven|eagle',29),('sheep|goat',30),('horse|donkey|unicorn',31),('archer|bow|crossbow',33),('mage|wizard|sorcer|lich|shaman',34),('priest|cleric|bishop|acolyte|superior|monk',35),('dwarf|gnome',36),('elf|ranger',37),('demon|devil|succub|balrog|fiend',38),('ghost|spirit|wisp|air_',39),('chest|coffer',40),('bed|coffin',41),('book|library|scroll',42),('furnace|forge|oven|smelter',43),('anvil|workshop|craft',44),('alchemy|laboratory|cauldron',45),('table|chair|bench',46),('throne|altar|shrine|statue',47),('sword|axe|blade|spear|mace|club|hammer|dagger|knife|weapon',48),('shield|defense',49),('armor|armour|helmet|robe|boot|glove',50),('staff|wand|spell|magic',51),('gold|coin|ring|jewel|amulet',52),('potion|heal|bottle',53),('trap|spike',58),('fire|flame|torch',59),('grave|tomb',60),('fence|barricade',61),('blood|hit|attack',62),('human|knight|warrior|soldier|guard|bandit|peasant|adventurer|villager',32)]
 for pattern,idx in rules:
  if re.search(pattern,n):return idx
 if symbol in ['.','·',',']:return 1
 if symbol in ['#','⁂']:return 7
 if symbol in ['~','≈']:return 3
 if symbol and symbol.isalpha():return 32
 return 52
mapping={};needed=set()
dirs=['','e','w','s','n','ew','ns','se','sw','ne','nw','nesw','esw','nsw','nes','new']
for rec in records:
 strings=re.findall(r'"([^"\n]*)"',rec)
 if not strings:continue
 vid=re.search(r'viewId\s*=\s*"([^"]+)"',rec);vid=vid.group(1) if vid else strings[0]
 sm=re.search(r'symbol\s*=\s*"([^"]*)"',rec);symbol=sm.group(1) if sm else strings[1] if len(strings)>1 else ''
 sp=re.search(r'sprite\s*=\s*"([^"]+)"',rec);name=sp.group(1) if sp else vid
 idx=family(vid,symbol);mapping[name]=idx;needed.add(name)
 for attr in ['background','southSide','spriteName','mountainSides','waterSides']:
  for val in re.findall(attr+r'\s*=\s*"([^"]+)"',rec):mapping.setdefault(val,family(val,symbol));needed.add(val)
 if 'wallConnections = true' in rec or 'roadConnections = true' in rec:
  for d in dirs:mapping[name+d]=idx;needed.add(name+d)
 for prefix in re.findall(r'(?:mountainSides|waterSides)\s*=\s*"([^"]+)"',rec):
  for x in ['sw_w','nw_w','se_e','ne_e','nw_n','ne_n','sw_s','se_s','nw','ne','sw','se','sese_se','swsw_sw','nene_ne','nwnw_nw']+dirs:
   mapping[prefix+x]=family(prefix,symbol);needed.add(prefix+x)
# Every literal tile name used by engine, including borders and transparent fog overlays.
for n in ['empty','fogofwarall','fogofwarcornne','fogofwarcornnw','fogofwarcornse','fogofwarcornsw']:
 mapping[n]=-1;needed.add(n)
for n,idx in mapping.items():
 im=sprites[idx] if idx>=0 else Image.new('RGBA',(24,24))
 assert '/' not in n and '\\' not in n
 im.save(root/(n+'.png'))
anims=out/'data/images/animations';anims.mkdir(parents=True,exist_ok=True)
for name,idx,num in [('attack',62,3),('death',63,8)]:
 strip=Image.new('RGBA',(24*num,24))
 for j in range(num):strip.paste(sprites[idx],(j*24,0))
 strip.save(anims/(name+'.png'))
# Graphics pack does not include commercial audio; start muted.
(out/'options_v1_0.txt').write_text('SOUND,0\nMUSIC,0\n')
(out/'data/sound').mkdir(parents=True,exist_ok=True)
(out/'data/music').mkdir(parents=True,exist_ok=True)
# Validate sprite dimensions, existence and file decoding, not just filenames.
for n in needed:
 with Image.open(root/(n+'.png')) as im:assert im.size==(24,24);im.verify()
report={'sprites':len(mapping),'base_artworks':64,'animations':{'attack':3,'death':8},'mode':'24px original custom art','unique_art_per_id':False}
(out/'SPRITES-VALIDACAO.json').write_text(json.dumps(report,indent=2))
(out/'LEIA-ME-GRAFICOS.txt').write_text('Extraia em uma pasta NOVA e execute Iniciar.bat.\nPixel art propria com 64 desenhos-base, reutilizados por familias de criaturas e objetos.\nAudio inicia desativado; este pacote nao inclui audio comercial.\nNao copie options_v1_0.txt sobre suas configuracoes existentes.\n')
print(report)
