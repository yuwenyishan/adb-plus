# coding:utf-8
from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need fine tuning.
# build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"
# executables = [cx_Freeze.Executable(u"D:\Python_project\adb-plus\adb_plus.py",
# base=base,icon=#"这里替换成图标位置",shortcutName="#这里替换成你软件名称",
# shortcutDir="#你想要创建的位置（以下有介绍）")]
executables = [Executable("adb_plus.py",
                          base=base,
                          icon="icon.ico",
                          targetName='adb-p.exe')]
# bdist_msi_options = {
#     "upgrade_code": "{#去网上生成一个固定的GUID，就不要变了}"
# }
bdist_msi_options = {
    "add_to_path": True,
    "upgrade_code": "{9d0b4568-0f37-4aa1-9cfa-484973803529}"
}
setup(
    name='adb-p',
    version='1.0.0',
    options={
        "bdist_msi": bdist_msi_options,
        "build_exe": {
            "packages": ['os', 'sys', 'signal', 'dircache', 'cmd', 'subprocess'],
            "include_files": ["icon.ico"],
            "optimize": 2
        }},
    author='Jack_long',
    executables=executables,
    description='improve android adb tool .'
)
