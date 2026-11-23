# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import fetch
import shared

case, archive, held, address = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve(), sys.argv[4], sys.argv[5]
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
folder = case / 'archives' / digest
folder.mkdir(parents=True)
if held == 'archive':
    (folder / archive.name).write_bytes(archive.read_bytes())
if held == 'part':
    (folder / (archive.name + '.part')).write_bytes(b'xyz')
url = (archive if address == 'archive' else case / 'gone' / archive.name).as_uri()
print(fetch.kept(url, digest, folder, shared.config(case)['fetch']['timeout']).name)
