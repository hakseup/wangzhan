"""Locally transcribe the two uploaded recordings which have no matching PDF."""
import glob,json,os,subprocess,tarfile,wave
from pathlib import Path
from vosk import Model,KaldiRecognizer,SetLogLevel
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'transcribed';OUT.mkdir(parents=True,exist_ok=True)
modelroot=Path('/workspace/tooling/models/vosk-fr')
if not modelroot.exists():
 modelroot.mkdir()
 with tarfile.open('/workspace/tooling/models/vosk-fr.tar.gz') as archive:archive.extractall(modelroot,filter='data')
config=next(modelroot.rglob('final.mdl'));directory=config.parents[1] if config.parent.name=='am' else config.parent
SetLogLevel(-1);model=Model(str(directory))
for p in glob.glob('/workspace/attachments/*/*.m4a'):
 if '2024年3月中国DALF C1短听力' not in p:continue
 segment=1 if '（一）' in p else 2;wav=f'/tmp/noix-orphan-{segment}.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-i',p,'-ac','1','-ar','16000','-sample_fmt','s16',wav],check=True)
 result=[]
 with wave.open(wav,'rb') as audio:
  rec=KaldiRecognizer(model,audio.getframerate());rec.SetWords(True)
  while chunk:=audio.readframes(4000):
   if rec.AcceptWaveform(chunk):result.append(json.loads(rec.Result()))
  result.append(json.loads(rec.FinalResult()))
 payload={'file':Path(p).name,'model':'vosk-model-small-fr-pguyot-0.3','segments':result,'text':'\n'.join(r.get('text','') for r in result)}
 (OUT/f'2024-3-cn-{segment}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
 print(segment,payload['text'],flush=True)
