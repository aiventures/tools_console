""" Persistence / access to local files / csv / xls / txt / json files
    Used Libraries
    * https://docs.python.org/3/library/csv.html

"""

from pathlib import Path
import json
#import csv
import os
#import re
# import shlex
# import shutil
# import subprocess
import traceback
import logging
# import time
# import datetime
#from datetime import datetime as DateTime
# from datetime import date
#from pathlib import Path
# from bs4 import BeautifulSoup as bs
# import pandas as pd
# # import lxml.etree as etree
# import pytz
# import pprint
# # from pytz import timezone
from tools import img_file_info_xls as fi

log = logging.getLogger(__name__)

class Persistence():
    """ anything concerned with reading / writing """

    # Regex for Date Prefix YYYYMMDD_
    REGEX_DATE_PREFIX = r"^(\d{8})_"

    @staticmethod
    def read_csv(f:str,delim=";",header=True,encoding="utf-8")->list:
        """ Reading CSV
            Args:
                f (str): Filename Path
                delim (str, optional): CSV delimiter. Defaults to ";".
                header (bool, optional): flag: csv contains header. Defaults to True.
                encoding (str, optional): File Encoding. Defaults to "utf-8".
            Returns:
                list: List
        """
        # TODO IMPLEMENT
        out = []


        return out

    @staticmethod
    def read_file(f:str)->list:
        """ reading UTF8 txt File """
        lines = []
        try:
            with open(f,encoding="utf-8") as fp:
                for line in fp:
                    line = line.strip()
                    if len(line) == 0:
                        continue
                    lines.append(line)
        except:
            # TODO switch to logging
            print(f"Exception reading file {f}")
            print(traceback.format_exc())
        return lines

    @staticmethod
    def read_json(filepath:str,encoding="utf-8"):
        """ Reads JSON file"""
        data = None

        if not os.path.isfile(filepath):
            print(f"File path {filepath} does not exist. Exiting...")
            return None

        try:
            with open(filepath,encoding=encoding) as json_file:
                data = json.load(json_file)
        except:
            # TODO switch to logging
            print(f"**** Error opening {filepath} ****")
            print(traceback.format_exc())
            print("***************")

        return data

    @staticmethod
    def save_json(filepath,data:dict):
        """ Saves dictionary data as UTF8 """

        with open(filepath, 'w', encoding='utf-8') as json_file:
            try:
                json.dump(data, json_file, indent=4,ensure_ascii=False)
            except:
                # TODO switch to logging
                print(f"Exception writing file {filepath}")
                print(traceback.format_exc())

            return None

    @staticmethod
    def delete_folder(fp:str, prompt:bool=True):
        """deletes a folder including files (non recursively, only file in filepath will be deleted)

        Args:
            fp (str): folder path for deletion
            prompt (bool, optional): Prompt before deletion. Defaults to True.
        """
        log.debug("start")

        if prompt and input(f"Delete folder {fp} [y]?")=="y":
            return
        # change to deletion path
        last_dir=os.getcwd()
        files=[]
        if os.path.isdir(fp):
            os.chdir(fp)
            # get files
            file_dict=fi.get_file_dict(fp)
            files=[p_info["files"] for p,p_info in file_dict.items() if Path(p)==Path(fp)]
        else:
            print(f"Path {fp} doesn't exist")
            return

        if files:
            files=files[0]
            log_info={"len":str(len(files)),"path":str(fp)}
            log.info("Removing %(len)s files in path %(path)s",log_info)
            for f in files:
                os.remove(f)

        # delete directory, switch to last used directory
        os.chdir(last_dir)
        try:
            os.rmdir(fp)
        except (PermissionError,OSError) as e:
            log.error("Error: %s",e)
