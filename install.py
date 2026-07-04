# -*- coding: utf-8 -*-
import os
import importlib

url_prefix = os.environ.get("FISHROS_URL", "http://mirror.fishros.com/install/")
base_url = os.path.join(url_prefix, "tools/base.py")
translator_url = os.path.join(url_prefix, "tools/translation/translator.py")

INSTALL_ROS = 0
INSTALL_SOFTWARE = 1
CONFIG_TOOL = 2
INSTALL_AI = 3

tools_type_map = {
    INSTALL_ROS: "ROS相关",
    INSTALL_AI: "AI板块",
    INSTALL_SOFTWARE: "常用软件",
    CONFIG_TOOL: "配置工具",
}

tools = {
    1: {
        "tip": "一键安装:ROS",
        "type": INSTALL_ROS,
        "tool": "tools/tool_install_ros.py",
        "dep": [4, 5],
    },
    2: {
        "tip": "一键安装:GitHub桌面版",
        "type": INSTALL_SOFTWARE,
        "tool": "tools/tool_install_github_desktop.py",
        "dep": [],
    },
    3: {
        "tip": "一键安装:rosdep",
        "type": INSTALL_ROS,
        "tool": "tools/tool_config_rosdep.py",
        "dep": [],
    },
    4: {
        "tip": "一键配置:ROS环境",
        "type": INSTALL_ROS,
        "tool": "tools/tool_config_rosenv.py",
        "dep": [],
    },
    5: {
        "tip": "一键配置:系统源",
        "type": CONFIG_TOOL,
        "tool": "tools/tool_config_system_source.py",
        "dep": [1],
    },
    6: {
        "tip": "一键安装:NodeJs环境",
        "type": INSTALL_AI,
        "tool": "tools/tool_install_nodejs.py",
        "dep": [],
    },
    7: {
        "tip": "一键安装:VsCode开发工具",
        "type": INSTALL_SOFTWARE,
        "tool": "tools/tool_install_vscode.py",
        "dep": [],
    },
    8: {
        "tip": "一键安装:Docker",
        "type": INSTALL_SOFTWARE,
        "tool": "tools/tool_install_docker.py",
        "dep": [],
    },
    9: {
        "tip": "一键安装:Cartographer",
        "type": INSTALL_ROS,
        "tool": "tools/tool_install_cartographer.py",
        "dep": [3],
    },
    10: {
        "tip": "一键安装:微信",
        "type": INSTALL_SOFTWARE,
        "tool": "tools/tool_install_wechat.py",
        "dep": [8],
    },
    11: {
        "tip": "一键安装:ROS Docker版",
        "type": INSTALL_ROS,
        "tool": "tools/tool_install_ros_with_docker.py",
        "dep": [7, 8],
    },
    12: {
        "tip": "一键安装:PlateformIO MicroROS开发环境",
        "type": INSTALL_SOFTWARE,
        "tool": "tools/tool_install_micros_fishbot_env.py",
        "dep": [],
    },
    13: {
        "tip": "一键配置:Python国内源",
        "type": CONFIG_TOOL,
        "tool": "tools/tool_config_python_source.py",
        "dep": [],
    },
    14: {
        "tip": "一键安装:科学上网代理工具",
        "type": INSTALL_AI,
        "tool": "tools/tool_install_proxy_tool.py",
        "dep": [8],
    },
    15: {
        "tip": "一键安装:QQ for Linux",
        "type": INSTALL_SOFTWARE,
        "tool": "tools/tool_install_qq.py",
        "dep": [],
    },
    16: {
        "tip": "一键安装:系统自带ROS",
        "type": INSTALL_ROS,
        "tool": "tools/tool_install_ros1_systemdefault.py",
        "dep": [5],
    },
    17: {
        "tip": "一键配置:Docker代理",
        "type": CONFIG_TOOL,
        "tool": "tools/tool_config_docker_proxy.py",
        "dep": [],
    },
    18: {
        "tip": "一键安装/卸载:OpenCode",
        "type": INSTALL_AI,
        "tool": "tools/tool_install_opencode.py",
        "dep": [6],
    },
}

tool_categories = {tool_type: {} for tool_type in tools_type_map}
for tool_id, tool_info in tools.items():
    tool_type = tool_info["type"]
    tool_categories[tool_type][tool_id] = tool_info
tool_categories = {k: v for k, v in tool_categories.items() if v}

tracking = None


def main():
    os.system("mkdir -p /tmp/fishinstall/tools/translation/assets")
    url_prefix = os.environ.get("FISHROS_URL", "http://mirror.fishros.com/install/")
    if url_prefix:
        os.system(
            "wget {} -O /tmp/fishinstall/{} --no-check-certificate".format(
                base_url, base_url.replace(url_prefix, "")
            )
        )
        os.system(
            "wget {} -O /tmp/fishinstall/{} --no-check-certificate".format(
                translator_url, translator_url.replace(url_prefix, "")
            )
        )

    from tools.base import (
        CmdTask,
        FileUtils,
        PrintUtils,
        ChooseTask,
        ChooseWithCategoriesTask,
        Tracking,
    )
    from tools.base import encoding_utf8, osversion, osarch
    from tools.base import run_tool_file, download_tools
    from tools.base import config_helper, tr

    importlib.import_module("tools.translation.translator").Linguist()
    from tools.base import tr
    import copy

    global tracing
    tracing = copy.copy(Tracking)

    if tr.country != "CN":
        PrintUtils.print_success(
            tr.tr(
                "检测到当前不在CN,切换服务地址为:https://raw.githubusercontent.com/fishros/install/master/"
            )
        )
        url_prefix = "https://raw.githubusercontent.com/fishros/install/master/"

    if not encoding_utf8:
        print("Your system encoding not support ,will install some packgaes..")
        CmdTask("sudo apt-get install language-pack-zh-hans -y", 0).run()
        CmdTask("sudo apt-get install apt-transport-https -y", 0).run()
        FileUtils.append("/etc/profile", 'export LANG="zh_CN.UTF-8"')
        print("Finish! Please Try Again!")
        return False
    PrintUtils.print_success(tr.tr("基础检查通过..."))

    tip = tr.tr("""\
===============================================================================
====== ROS 快速安装工具 ======
====== 开源地址：https://github.com/fishros/install =======
===============================================================================
""")
    PrintUtils.print_delay(tip, 0.001)

    code, result = ChooseWithCategoriesTask(
        tool_categories,
        tips=tr.tr("---请选择要安装的工具---"),
        categories=tools_type_map,
    ).run()
    if code == 0:
        PrintUtils().print_success(tr.tr("已取消，感谢使用！"))
    else:
        if url_prefix:
            download_tools(code, tools, url_prefix)
        run_tool_file(tools[code]["tool"].replace("/", "."))

    if (
        os.environ.get("GITHUB_ACTIONS") != "true"
        and os.environ.get("FISH_INSTALL_CONFIG") is None
    ):
        config_helper.gen_config_file()


if __name__ == "__main__":
    run_exc = []
    try:
        main()
    except Exception as e:
        import traceback
        print(
            "\r\n检测到程序发生异常退出，请打开："
            "https://github.com/fishros/install/issues 携带如下内容进行反馈\n\n"
        )
        print("标题：使用一键安装过程中遇到程序崩溃")
        print("```")
        traceback.print_exc()
        run_exc.append(traceback.format_exc())
        print("```")
        print("本次运行详细日志文件已保存至 /tmp/fishros_install.log")

    try:
        with open("/tmp/fishros_install.log", "w", encoding="utf-8") as f:
            for exec in run_exc:
                print(exec, file=f)
            for text, end in tracing.logs:
                print(text, file=f, end=end)
            for text in tracing.err_logs:
                print(text, file=f)
    except:
        pass
