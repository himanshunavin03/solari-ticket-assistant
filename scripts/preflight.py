"""Windows-friendly readiness check: dependencies, real model, owned HTTP server, UI build."""
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]


def run(command, cwd=ROOT):
    print('CHECK:', ' '.join(map(str,command)),flush=True)
    subprocess.run(command,cwd=cwd,check=True)


def main():
    print(f'Selected backend Python: {sys.version.split()[0]} ({sys.executable})',flush=True)
    # This is a check, not a model download/bootstrap command.
    os.environ['SOLARI_OFFLINE']='1'
    if sys.version_info < (3,10): raise RuntimeError('Python >=3.10 required')
    node=shutil.which('node'); npm=shutil.which('npm.cmd' if os.name=='nt' else 'npm')
    if not node or not npm: raise RuntimeError('Node/npm missing; run scripts/bootstrap-node.ps1 and set this shell PATH')
    version=subprocess.check_output([node,'--version'],text=True).strip()
    print('Active Node:',version,flush=True)
    major,minor,*_=map(int,version.lstrip('v').split('.'))
    if not ((major==20 and minor>=19) or (major==22 and minor>=12) or major>=24):
        raise RuntimeError(f'Angular requires an additional compatible Node runtime; active {version} is unsupported. Run scripts/bootstrap-node.ps1 and set PATH.')
    run([npm,'--version']); run([sys.executable,'-m','pip','check'])
    for line in (ROOT/'requirements.txt').read_text().splitlines():
        if '==' in line:
            name,expected=line.split('=='); actual=importlib.metadata.version(name)
            if actual!=expected: raise RuntimeError(f'{name}: expected {expected}, installed {actual}')
    run([sys.executable,'-m','scripts.download_model'])
    if os.getenv('SOLARI_KEYWORD_ONLY')=='1': raise RuntimeError('Unset SOLARI_KEYWORD_ONLY to verify all capabilities')
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
    log=ROOT/'.cache/preflight-backend.log'; log.parent.mkdir(exist_ok=True)
    with log.open('w',encoding='utf-8') as stream:
        process=subprocess.Popen([sys.executable,'-m','uvicorn','backend.app:app','--host','127.0.0.1','--port',str(port),'--no-access-log'],
            cwd=ROOT,stdout=stream,stderr=stream,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            deadline=time.monotonic()+90
            while True:
                try:
                    with urlopen(f'http://127.0.0.1:{port}/api/health',timeout=2) as response:
                        health=json.load(response)
                    break
                except OSError:
                    if process.poll() is not None or time.monotonic()>deadline: raise RuntimeError(f'Backend did not become ready; inspect {log}')
                    time.sleep(.25)
            print('Readiness:',json.dumps(health),flush=True)
            if health['status']!='ready' or set(health['capabilities'])!={'keyword','semantic','hybrid'}:
                raise RuntimeError('All three retrieval capabilities required for full preflight')
        finally:
            process.terminate()
            try: process.wait(timeout=10)
            except subprocess.TimeoutExpired: process.kill(); process.wait()
    run([npm,'ls','--depth=0'],ROOT/'frontend')
    run([npm,'run','typecheck'],ROOT/'frontend'); run([npm,'run','build'],ROOT/'frontend')
    print('PREFLIGHT PASSED: real model, HTTP readiness, dependencies and frontend build. Not original Launchpad certification.',flush=True)


if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(f'PREFLIGHT FAILED: {exc}',file=sys.stderr); sys.exit(1)
