import os
import sys
import time
from cfg_loader import load_config
from llm import LLMPlus
from llonebot import ThreadMsgListener, ThreadMsgSender


NAME = "LLM客户端 by NIVSAYZ(柃)"
VERSION = "V2.0"
print(NAME, VERSION)


# ===本地运行===
def run_local():
    user_name = cfg_dict["user_name"]
    user_id = cfg_dict["user_id"]
    assistant_name = cfg_dict["assistant_name"]
    while True:
        receive_text = input("你：")

        # ===交互===
        if receive_text == cfg_dict["clear_user_memory_command"]:
            llm_plus.clear_memory(user_id=user_id)
            assistant_content = cfg_dict["clear_user_memory_notice"]

        else:
            assistant_content = llm_plus.chat(user_name=user_name, user_id=user_id, user_content=receive_text)

        if split_symbol in assistant_content:
            reply_text_list = assistant_content.split(split_symbol)
        else:
            reply_text_list = [assistant_content]

        for reply_text in reply_text_list:
            print(assistant_name + "：" + reply_text)
            time.sleep(0.6 + len(reply_text) * 0.2)  # 伪停顿


def run_with_llonebot():
    os.system("chcp 65001")
    print(NAME, VERSION)

    msg_sender = ThreadMsgSender(host=cfg_dict["send_host"], port=int(cfg_dict["send_port"]), max_workers=int(cfg_dict["sender_thread"])) #实例化发送器
    listen_qq_list = list(map(int, cfg_dict["listen_qq_list"].split(",")))
    msg_listener = ThreadMsgListener(listen_qq_list=listen_qq_list, max_workers=int(cfg_dict["listener_thread"])) #实例化监听器
    msg_listener.start(host=cfg_dict["listen_host"], port=int(cfg_dict["listen_port"])) #启动监听器
    msg_polling_rate = int(cfg_dict["msg_polling_rate"])

    while True:
        # ===跳过已读消息===
        if msg_listener.current_message_dict["checked"]:
            time.sleep(1 / msg_polling_rate) #轮询间隔
            continue

        # ===新消息数据获取===
        message_id = msg_listener.current_message_dict["message_id"]
        user_nickname = msg_listener.current_message_dict["user_nickname"]
        user_id = msg_listener.current_message_dict["user_id"]
        group_id = msg_listener.current_message_dict["group_id"]
        receive_text = msg_listener.current_message_dict["text"]
        print("[LLM客户端|接收|用户ID:{}|群ID:{}|内容:{}]".format(user_id, group_id, receive_text))

        # ===交互===
        if receive_text == cfg_dict["clear_user_memory_command"]:
            llm_plus.clear_memory(user_id=user_id)
            assistant_content = cfg_dict["clear_user_memory_notice"]

        else:
            assistant_content = llm_plus.chat(user_name=user_nickname, user_id=user_id, user_content=receive_text)

        # ===分割回复文本===
        if split_symbol in assistant_content:
            reply_text_list = assistant_content.split(split_symbol)
        else:
            reply_text_list = [assistant_content]

        # ===回复===
        message_list = list()
        reply_text = reply_text_list[0] #首条文本
        delay = 0.6 + len(reply_text) * 0.2 #延时时间
        if group_id:
            msg_type = "group"
            traget_id = group_id
            message_list.append([msg_type, traget_id, reply_text, message_id, delay])
        else:
            msg_type = "private"
            traget_id = user_id
            message_list.append([msg_type, traget_id, reply_text, 0, delay])

        for reply_text in reply_text_list[1:]:
            delay = 0.6 + len(reply_text) * 0.2  # 延时时间
            message_list.append([msg_type, traget_id, reply_text, 0, delay])
        msg_sender.submit_message_list(message_list) #提交消息列表

        msg_listener.current_message_dict["checked"] = True #将消息标记为已读


# ===读取配置文件===
main_dir = os.path.dirname(sys.argv[0])
cfg_path = main_dir + "\\" + "config.cfg"
cfg_dict = load_config(cfg_path)

# ===读取提示词===
system_content_path = cfg_dict["system_content_path"]
if not system_content_path:
    system_content = ""
else:
    system_content = open(system_content_path, "r", encoding="utf-8").read()

# ===检查记忆路径===
if not cfg_dict["memory_save_dir"]:
    memory_save_dir = main_dir + "\\" + "memory"
else:
    memory_save_dir = cfg_dict["memory_save_dir"] + "\\" + "memory"

llm_plus = LLMPlus(model=cfg_dict["model"], system_content=system_content, api_key=cfg_dict["api_key"], base_url=cfg_dict["base_url"], memory_save_dir=memory_save_dir)

split_symbol = cfg_dict["split_symbol"] #取得分隔符

choice = input("本地运行[Y/N]:").upper()
if choice == "Y":
    run_local()
else:
    run_with_llonebot()
