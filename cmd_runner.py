""" Runner for local os commands """
import shlex
import subprocess

class CmdRunner():
    """ Cnd Runner: Runs OS Commands locally """

    def __init__(self) -> None:
        """ constructor """
        self.output=None
        self.return_code=0


    def run_cmd(self,os_cmd:str):
        """ runs command line command """
        oscmd_shlex=shlex.split(os_cmd)
        # special case: output contains keywords (in this case its displaying a logfile)
        self.output=[]
        self.return_code=0
        try:
            # encoding for german umlauts
            with subprocess.Popen(oscmd_shlex, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    errors='ignore',universal_newlines=True,encoding="utf8") as popen:
                for line in popen.stdout:
                    self.output.append(line)
                    line=line.replace("\n","")
                    # TODO switch to log
                    # print(line)

            # popen.stdout.close()
            # TODO switch to log
            if popen.stderr:
                print(f"ERROR OCCURED: {popen.stderr}")

            self.return_code = popen.returncode
            if self.return_code:
                raise subprocess.CalledProcessError(self.return_code, os_cmd)
        except subprocess.CalledProcessError as e:
            self.return_code=1
            print("xxx",e.args)
            print(f"EXCEPTION OCCURED {e}, command {os_cmd}")
        return self.return_code

    def get_output(self,as_string=True):
        """ Returns output from last command
        Args:
            as_string (bool, optional): if True, output string list will be concatenated. Defaults to True.
        Returns:
            string/list: single output strings as list or concatenated string
        """
        out= self.output
        if as_string and isinstance(out,list):
            out = "".join([l.strip() for l in out])
        return out
