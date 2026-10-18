"""Load the same split static dictionary as the browser; no network or runtime service."""
import json
from pathlib import Path
def load_bank(directory):
 directory=Path(directory);bank=json.loads((directory/'content.json').read_text())
 for name in bank.pop('lexiconFiles',[]):
  part=json.loads((directory/name.lstrip('/')).read_text())
  for key,value in part.items():
   if isinstance(value,list):bank['lexicon'].setdefault(key,[]).extend(value)
   else:bank['lexicon'].setdefault(key,{}).update(value)
 return bank
