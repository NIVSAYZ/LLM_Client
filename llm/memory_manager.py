import os
import zlib


class MemoryManager:
    def __init__(self,
                 memory_dir: str = ""):
        self.memory_dir = memory_dir

    # ===载入记忆===
    def load_memory_save(self):
        memory_dict = dict() #记忆字典
        if not os.path.exists(self.memory_dir):
            return memory_dict
        for item in os.listdir(self.memory_dir): #遍历记忆目录
            item_path = os.path.join(self.memory_dir, item) #检查项目
            if not os.path.isfile(item_path): #跳过目录
                continue
            memory_list = list() #初始化记忆列表
            memory_save = open(item_path, "rb").read() #读取交流记录
            memory_bytes = zlib.decompress(memory_save)
            memory_lines = memory_bytes.decode(encoding="utf-8").split("\n") #分行
            for memory_line in memory_lines: #遍历行
                if not memory_line:
                    continue
                role, content = memory_line.split(":")  # 分隔读取角色与交流内容
                memory_list.append({"role": role, "content": content})  # 添加至记忆列表
            memory_dict[int(os.path.basename(item_path).replace(".dat", ""))] = memory_list  # 创建记忆字典键值对
        return memory_dict

    # ===保存记忆===
    def save_user_memory(self, user_id, user_memory_dict):
        memory_list = list() #初始化记忆列表
        for message_dict in user_memory_dict: #遍历记忆字典中的记忆列表
            role = message_dict["role"] #获取角色
            content = message_dict["content"] #获取交流内容
            memory_list.append(role + ":" + '"' + content + '"') #填入记忆列表
        memory_str = "\n".join(memory_list) #将记忆列表分行转为字符串
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
        memory_save = open(self.memory_dir + "\\" + "{}.dat".format(user_id), "wb")
        memory_bytes = zlib.compress(memory_str.encode(encoding="utf-8"), level=9)
        memory_save.write(memory_bytes) #以UTF-8编码写入二进制文件
        memory_save.close()
