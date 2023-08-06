import subprocess
import logging
import pathlib

logging.basicConfig(level=logging.DEBUG)

class BobBuilder:
    def __init__(self, project_dir: str) -> None:
        abs_path = str(pathlib.Path(project_dir).resolve())
        self.common_args = [
            '--verbose', 
            '--root', abs_path, 
            '--input', abs_path
        ]
        self.exec = ['java', '-jar', 'bob.jar']
        self.project_dir = abs_path
    
    def resolve_deps(self):
        cmd = 'resolve'
        exec_cmd = self.exec + self.common_args + [cmd]
        result = self._exec_cmd(exec_cmd)
            
    def build(self, platform: str, arch: str, variant: str):
        cmd = 'build'
        args = [
            '--archive',
            '--platform', platform,
            '--architectures', arch,
        ]
        if variant == 'debug':
            args.append("-d")
        exec_cmd = self.exec + self.common_args + args + [cmd]
        logging.debug(exec_cmd)
        result = self._exec_cmd(exec_cmd)

    def bundle(self, output_dir: str, platform: str, arch: str, variant):
        out_dir = str(pathlib.Path(output_dir).resolve())
        varian_hack = None
        if variant == 'debug':
            varian_hack = ["-d"]
        else:
            varian_hack = ["--variant", "release"]
        cmd = 'bundle'
        args = [
            '--bundle-output', out_dir,
            '--platform', platform,
            '--architectures', arch
        ]
        args += varian_hack
        exec_cmd = self.exec + self.common_args + args + [cmd]
        logging.debug(exec_cmd)
        result = self._exec_cmd(exec_cmd)

    def _exec_cmd(self, cmd) -> subprocess.CompletedProcess:
        result = subprocess.run(cmd, check=True)
        return result
