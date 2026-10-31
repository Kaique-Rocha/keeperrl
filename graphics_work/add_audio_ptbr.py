import math,random,re,wave,struct,subprocess,shutil,zipfile,json
from pathlib import Path
base=Path(__file__).parent;game=base/'game';rate=22050
ff=shutil.which('ffmpeg')
if not ff:
 import imageio_ffmpeg
 ff=imageio_ffmpeg.get_ffmpeg_exe()
rng=random.Random(3110)
def encode(name,duration,kind):
 wav=base/(name+'.wav');ogg=base/(name+'.ogg');buf=bytearray()
 for i in range(int(rate*duration)):
  t=i/rate
  if kind=='music':
   chord=[110,130.813,164.814,220][int(t//8)%4]
   x=sum(math.sin(2*math.pi*chord*m*t+0.25*math.sin(t/4)) / (m*7) for m in [1,1.5,2,3])*(0.5-0.5*math.cos(2*math.pi*t/duration))
  else:
   env=min(1,t/0.012)*math.exp(-t*(6 if kind in ['magic','ambient','death'] else 18))
   noise=rng.uniform(-1,1)
   freqs={'click':780,'step':95,'hit':130,'magic':440,'door':75,'craft':1050,'death':90,'ambient':220,'bow':300,'fire':55,'coin':1400}
   f=freqs[kind];phase=f*(t+(0.7*t*t if kind=='magic' else -0.15*t*t))
   x=env*(0.5*noise+0.2*math.sin(2*math.pi*phase)) if kind in ['step','hit','door','fire','bow'] else env*(0.22*math.sin(2*math.pi*phase)+0.07*math.sin(2*math.pi*phase*1.5))
  buf.extend(struct.pack('<h',int(max(-0.8,min(.8,x))*24000)))
 with wave.open(str(wav),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(buf)
 subprocess.run([ff,'-v','error','-y','-i',str(wav),'-c:a','libvorbis','-q:a','3',str(ogg)],check=True);wav.unlink();return ogg
clips={k:encode('fx_'+k,1.4 if k in ['magic','ambient','death'] else .5,k) for k in ['click','step','hit','magic','door','craft','death','ambient','bow','fire','coin']}
def category(n):
 for pattern,kind in [('button|click|select','click'),('step|walk|move','step'),('spell|magic|heal|teleport|create','magic'),('door|open|close','door'),('craft|forge|hammer|dig|mine','craft'),('dying|death|hurt|roar','death'),('ambient','ambient'),('bow|shoot|arrow','bow'),('fire|burn|explosion','fire'),('gold|coin|money','coin')]:
  if re.search(pattern,n):return kind
 return 'hit'
counts={k:0 for k in clips}
for d in (game/'data/sound').iterdir():
 k=category(d.name);counts[k]+=1
 for f in d.glob('*.ogg'):f.unlink()
 shutil.copyfile(clips[k],d/'effect.ogg')
music=encode('ambient_dungeon',32,'music')
for f in (game/'data/music').glob('*.ogg'):shutil.copyfile(music,f)
pt=base/'portugues.txt';target=game/'data_free/game_config/translations/portugues.txt';shutil.copyfile(pt,target)
def entries(s):return {p.split()[0]:p for p in re.split(r'(?m)^(?=[A-Z][A-Z0-9_]*\s)',s) if re.match(r'^[A-Z][A-Z0-9_]*\s',p)}
en=entries((game/'data_free/game_config/translations/english.txt').read_text(encoding='utf-8'));br=entries(pt.read_text(encoding='utf-8'))
assert en.keys()<=br.keys()
for k in en:assert sorted(re.findall(r'\{\d+\}',en[k]))==sorted(re.findall(r'\{\d+\}',br[k])),k
(game/'options_v1_0.txt').write_text('SOUND,40\nMUSIC,12\nLANGUAGE,2\n',encoding='utf-8')
report={'translation_keys':len(en),'placeholder_mismatches':0,'sound_families':counts,'music_seconds':32}
(game/'AUDIO-PTBR-VALIDACAO.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(game/'LEIA-ME-GRAFICOS.txt').write_text('Extraia em uma pasta NOVA e execute Iniciar.bat.\nSprites proprios com 64 desenhos-base reutilizados por familias.\nEfeitos sintetizados e trilha ambiente instrumental generica incluidos.\nIdioma inicial: Portugues. Volumes ajustaveis nas Configuracoes.\nNao substitua suas configuracoes antigas; copie seus saves separadamente se desejar.\n',encoding='utf-8')
with zipfile.ZipFile(base.parent/'KeeperRL-Windows-Sprites-Audio-PTBR.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in game.rglob('*'):
  if p.is_file() and not p.name.startswith('gui-') and p.name!='GUI-WINDOWS.png':z.write(p,p.relative_to(game))
print(report)
