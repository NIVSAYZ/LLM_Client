import time
import httpx
import concurrent.futures


class ThreadMsgSender:
    def __init__(self,
                 host: str = "localhost",
                 port: int = 3000,
                 max_workers: int = 1):

        self.__thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.base_url = "http://{}:{}/".format(host, port)
        print("[信息发送器|配置|目标主机:{}|目标端口:{}|工作线程:{}]".format(host, port, max_workers))

    @staticmethod
    def send_post(url, json):
        result = httpx.post(url=url, json=json) #发送POST请求
        print("[POST发送器|返回|状态码:{}]".format(result.status_code))

    def send_message(self,
                     msg_type: str = "",
                     traget_id: int = 0,
                     text: str = "",
                     message_id: int = 0):

        if not traget_id:
            raise Exception("target_id not null")

        # ===私信消息===
        if msg_type == "private":
            traget_str = "user_id"
            url_parameter = "send_private_msg"

        # ===群消息===
        elif msg_type == "group":
            traget_str = "group_id"
            url_parameter = "send_group_msg"

        else:
            raise Exception("msg_type error")

        message_list = list()

        # ===回复===
        if message_id:
            message_list.append({"type": "reply", "data": {"id": message_id}})

        # ===文本===
        message_list.append({"type": "text", "data": {"text": text}})
        self.send_post(url=self.base_url + url_parameter, json={traget_str: traget_id, "message": message_list}) #发送POST

    def send_message_list(self,
                          message_list: list = None):

        if not message_list:
            raise Exception("message_list is empty")

        for msg_type, traget_id, text, message_id, delay in message_list:
            print("[信息发送器|发送|类型:{}|目标ID:{}|延时:{}|内容:{}]".format(msg_type, traget_id, delay, text))
            self.send_message(msg_type=msg_type, traget_id=traget_id, text=text, message_id=message_id)
            time.sleep(delay)

    def submit_message(self,
                       msg_type: str = "",
                       traget_id: int = 0,
                       text: str = "",
                       message_id: int = 0):

        print("[信息发送器|发送|类型:{}|目标ID:{}|内容:{}]".format(msg_type, traget_id, text))
        self.__thread_pool.submit(self.send_message, **{"msg_type":msg_type, "traget_id":traget_id, "text":text, "message_id":message_id})

    def submit_message_list(self,
                            message_list: list = None):

        self.__thread_pool.submit(self.send_message_list, **{"message_list":message_list})
