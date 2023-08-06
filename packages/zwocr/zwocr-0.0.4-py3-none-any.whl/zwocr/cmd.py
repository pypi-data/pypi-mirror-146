import time
import subprocess
from pathlib import Path

from loguru import logger

from zwutils.fileutils import rmfile, readjson

def cmdline(cmdpth, srcpth, dstdir, outtype, timeout=None):
    spth, dpth = Path(srcpth), Path(dstdir)
    timeout = timeout or 600*3

    def run_cmd(cmd, dstfile):
        cmdtimeout = timeout
        if dstfile.exists():
            rmfile(dstfile)
        time_start = time.time()
        try:
            subprocess.run(cmd, shell=True, timeout=cmdtimeout)
        except subprocess.TimeoutExpired:
            pass
        while not dstfile.exists():
            t = time.time()
            if t > time_start+cmdtimeout:
                break
            else:
                time.sleep(1)
        if not dstfile.exists():
            logger.error('OCR fail, file not create, %s', dstfile)
            return

    if spth.is_dir():
        for f in spth.glob('**/*.pdf'):
            dstfile = dpth / ('%s.%s'%(f.stem, outtype))
            cmd = '%s "%s" /out "%s"' % (cmdpth, str(f.absolute()), str(dstfile.absolute()))
            # os.system(cmd)
            run_cmd(cmd, dstfile)
    else:
        dstfile = dpth / ('%s.%s'%(spth.stem, outtype))
        cmd = '%s "%s" /out "%s"' % (cmdpth, str(spth.absolute()), str(dstfile.absolute()))
        run_cmd(cmd, dstfile)
        # os.system(cmd)
