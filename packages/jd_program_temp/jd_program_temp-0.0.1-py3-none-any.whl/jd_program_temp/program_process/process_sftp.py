# -*- coding: utf-8 -*-
import traceback
import time
from jd_program_temp.request_downloader.downloaders import sftp_farbic_connect
from jd_program_temp.commons.common_fun import check_path, un_zip
from jd_program_temp.monitor.monitor_signal_alert import send_mail, pipe_monitor_file
import datetime

class SftpProcess:
    def __init__(self, request_info, load_path, out_path, load_need_email=False, need_unzip=False, unzip_path='',
                 need_monitor_file=False, download_date='', **kwargs):
        self.request_info = request_info
        self.load_path = load_path
        self.out_path = out_path
        self.need_unzip = need_unzip
        self.unzip_path = unzip_path
        self.load_need_email = load_need_email
        self.need_monitor_file = need_monitor_file
        self.download_date = download_date if download_date else (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')

    def get_connect(self):
        return sftp_farbic_connect(**self.request_info)

    def sftp_download(self, sftp_con):
        load_res = False
        for i in range(3):
            try:
                print('start_load')
                print(self.load_path)
                print(self.out_path)
                print('---------------------------------')
                sftp_con.get(self.load_path, self.out_path)
                if check_path(self.out_path, check_file_size=True):
                    load_res = True
                    break
            except Exception as e:
                traceback.print_exc()
                time.sleep(2)
                continue
        return load_res

    def run(self):

        sftp_con = sftp_farbic_connect(**self.request_info)
        load_res = self.sftp_download(sftp_con)
        if not load_res:
            print('load_error')
            return False
        if self.load_need_email:
            print('send_email')
            # to_list "[172.30.16.31]msci barra ase2 message"   download_date + " done."
            # send_mail(to_list, "[172.30.16.31]msci barra ase2 message", download_date + " done.")

        if self.need_unzip and self.unzip_path:
            t_zip_path = r'C:\\Users\\zhangyf\\Downloads\\demo_load\\zip_dir\\'
            try:
                un_zip(self.out_path, self.unzip_path)
            except Exception as e:
                print('un_zip_error')
                traceback.print_exc()
        if self.need_monitor_file:
            print('pipe_monitor_file')
            # pipe_monitor_file(self.out_path, self.download_date)
