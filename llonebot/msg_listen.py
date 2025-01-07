import fastapi
import uvicorn
import concurrent.futures


class ThreadMsgListener:
    def __init__(self,
                 listen_qq_list: list = None,
                 #user_white_list: list = None,
                 #user_black_list: list = None,
                 #group_white_list: list = None,
                 #group_black_list: list = None,
                 group_msg_at_only: bool = True,
                 max_workers: int = 1):

        self.listen_qq_list = listen_qq_list
        #self.user_white_list = user_white_list
        #self.user_black_list = user_black_list
        #self.group_white_list = group_white_list
        #self.group_black_list = group_black_list
        self.__thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.__app = fastapi.FastAPI()
        self.current_message_dict = {"message_id":0, "user_nickname": "", "user_id": 0, "group_id": 0, "text": "", "checked": True}
        print("[信息监听器|配置|目标QQ列表:{}|工作线程:{}]".format(listen_qq_list, max_workers))

        # ===uvicorn_app配置===
        @self.__app.post("/")
        async def root(request: fastapi.Request):
            http_message = await request.json()

            # ===检查消息来源QQ===
            self_id = http_message.get("self_id")
            if not self_id in self.listen_qq_list:
                return

            # ===检查消息类型===
            post_type = http_message.get("post_type")
            if post_type != "message":
                return

            message_id = http_message.get("message_id") #消息ID

            # ===发送者信息获取===
            sender = http_message.get("sender")
            sender_user_id = sender.get("user_id")
            #if sender_user_id in self.user_black_list or not sender_user_id in self.user_white_list:
            #    return
            sender_nickname = sender.get("nickname")

            msg_type = http_message.get("message_type")
            if msg_type == "private":
                group_id = 0
            elif msg_type == "group":
                group_id = http_message.get("group_id")
            #    if group_id in self.group_black_list or not group_id in self.group_white_list:
            #        return
            else:
                raise Exception("msg_type error")

            # ===信息解读===
            message_data_at_qq = str()
            message_data_text = str()
            message = http_message.get("message")
            for message_info in message:
                message_type = message_info.get("type")
                message_data = message_info.get("data")
                if message_type == "at":
                    message_data_at_qq = int(message_data.get("qq"))
                elif message_type == "text":
                    message_data_text = message_data.get("text")

            # ===跳过群发非@信息===
            if group_msg_at_only and msg_type == "group" and not message_data_at_qq in listen_qq_list:
                return

            self.current_message_dict = {"message_id":message_id, "user_nickname": sender_nickname, "user_id": sender_user_id, "group_id": group_id, "text": message_data_text, "checked": False}


    def start(self,
              host: str="127.0.0.1",
              port: int=8080,):
        self.__thread_pool.submit(uvicorn.run, **{"app": self.__app, "host": host, "port": port, "log_config": None})
        print("[信息监听器|启动|目标主机:{}|目标端口:{}]".format(host, port))
