# -*- coding: utf-8 -*-
import getpass
import os
import shutil
from jd_program_temp.commons import common_fun as tools

def deal_file_info(file):
    file = file.replace("{DATE}", tools.get_current_date())
    file = file.replace("{USER}", getpass.getuser())

    return file

class GenerateProject:
    def copy_callback(self, src, dst, *, follow_symlinks=True):
        if src.endswith(".py"):
            with open(src, "r", encoding="utf-8") as src_file, open(
                dst, "w", encoding="utf8"
            ) as dst_file:
                content = src_file.read()
                content = deal_file_info(content)
                dst_file.write(content)

        else:
            shutil.copy2(src, dst, follow_symlinks=follow_symlinks)

    def generate(self, project_name, need_date=False):
        if need_date:
            now_time_str = tools.get_now_timedate()
            project_name = project_name + '_' + now_time_str
        if os.path.exists(project_name):
            print("%s 项目已经存在" % project_name)
        else:
            template_path = os.path.abspath(
                os.path.join(__file__, "../../../templates/project_template")
            )
            shutil.copytree(
                template_path, project_name, copy_function=self.copy_callback
            )

            print("\n%s 项目生成成功" % project_name)