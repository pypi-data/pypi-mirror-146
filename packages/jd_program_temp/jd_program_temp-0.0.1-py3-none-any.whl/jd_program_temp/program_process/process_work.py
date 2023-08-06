# -*- coding: utf-8 -*-
import os

from jd_program_temp.commons.common_fun import check_path, try_get
from jd_program_temp.commons.common_cfg import get_cfg_data
from jd_program_temp.program_process.process_sftp import SftpProcess
import jd_program_temp.setting as setting
CONFIG_FILE = "project.cfg"


class ProgramProcess:
    def __init__(self, debug=False, **kwargs):
        self.debug = debug

    def sftp_program(self, url_source):
        for sour in url_source:
            request_info = sour.get("request_info")
            if not request_info:
                request_info = {}
                request_info["sftp_host"] = sour.get("sftp_host")
                request_info["sftp_user"] = sour.get("sftp_user")
                request_info["sftp_password"] = sour.get("sftp_password")
            load_path = sour.get("sftp_load_path")
            out_path = sour.get("sftp_out_path")
            sftp_program = SftpProcess(request_info, load_path, out_path)
            sftp_program.run()

    def run(self):
        cfg_path = (os.path.join(os.getcwd(), CONFIG_FILE))
        if not check_path(cfg_path):
            print('no cfg!!')
            return
        program_config = get_cfg_data(cfg_path, need_dict=True)
        debug = try_get(program_config, ["debug", "enable"])
        debug = True if debug=='1' else False
        url_customize = try_get(program_config, ["url_source", "customize"])
        if url_customize != '1':
            requests_type = try_get(program_config, ["url_source", "request_type"])
            if requests_type == 'sftp':
                url_source = program_config.get("url_source")
                self.sftp_program(url_source)
        else:
            requests_type = try_get(program_config, ["url_source", "request_type"])
            url_source = setting.UrlSource(debug=debug).load_all_source()
            if requests_type == 'sftp':
                self.sftp_program(url_source)
            print('load_customiza:%s'%len(url_source))



        # url_source_customize = int(program_config.get("url_source", "customize"))
        # print("workflow_customize:%s" % type(url_source_customize))
