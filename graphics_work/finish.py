from pathlib import Path
import re,shutil,zipfile,json
from PIL import Image
base=Path(__file__).parent;game=base/'game';source=base.parent
# Supply every audio identifier with a quiet compatibility clip. Original commercial audio is not distributed.
ids=set()
for p in list(source.glob('*.cpp'))+list(source.glob('*.h'))+list((game/'data_free/game_config').rglob('*.txt')):
 ids.update(re.findall(r'"([A-Z][A-Z0-9_]+)"',p.read_text(errors='ignore')))
for n in ids:
 d=game/'data/sound'/n.lower();d.mkdir(parents=True,exist_ok=True);shutil.copyfile(base/'silence.ogg',d/'compat.ogg')
for n in re.findall(r'path.file\("([^"\n]+\.ogg)"\)',(source/'main.cpp').read_text()):shutil.copyfile(base/'silence.ogg',game/'data/music'/n)
# Check all direct filename references and sprites are decodable.
for p in (game/'data/images').rglob('*.png'):
 with Image.open(p) as im:im.verify()
for n,frames in [('attack',3),('death',8)]:
 with Image.open(game/f'data/images/animations/{n}.png') as im:assert im.width==24*frames and im.height==24
with zipfile.ZipFile(base.parent/'KeeperRL-Windows-x64-Sprites.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in game.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(game))
with zipfile.ZipFile(base/'graphics-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
 for folder in ['data']:
  for p in (game/folder).rglob('*'):
   if p.is_file():z.write(p,p.relative_to(game))
 for n in ['options_v1_0.txt','SPRITES-VALIDACAO.json','LEIA-ME-GRAFICOS.txt']:z.write(game/n,n)
print('audio_compatibility_ids',len(ids));print('pack_bytes',(base/'graphics-pack.zip').stat().st_size)
