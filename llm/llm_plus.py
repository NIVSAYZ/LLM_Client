import openai
from llm.memory_manager import MemoryManager
from llm.system_content_manager import SystemContentManager


class LLMPlus:
    def __init__(self,
                 model: str = "",
                 system_content: str = "",
                 api_key: str = "",
                 base_url: str = "",
                 memory_save_dir: str = ""):

        self.__memory_manager = MemoryManager(memory_save_dir) #记忆管理器
        self.__system_content_manager = SystemContentManager(system_content) #系统提示词管理器

        self.model = model
        self.__client = openai.OpenAI(api_key=api_key, base_url=base_url) #OpenAI客户端
        self.__memory_dict = self.__memory_manager.load_memory_save() #记忆字典

    # ===聊天===
    def chat(self,
             user_name: str = "",
             user_id: int = 0,
             user_content: str = ""):

        if not user_id in self.__memory_dict.keys(): #未在记忆字典中找到用户ID
            self.__memory_dict[user_id] = [] #创建新记忆列表

        system_content = self.__system_content_manager.update_prompt(user_name) #获取动态提示词
        system_message = {"role": "system", "content": system_content} #系统提示词
        user_message = {"role": "user", "content": user_content} #用户发言
        messages = self.__memory_dict[user_id] + [system_message] #使用记忆内容并添加系统提示词
        self.__memory_dict[user_id].append(user_message) #记忆用户发言
        chat_completion = self.__client.chat.completions.create(model=self.model, messages=messages + [user_message]) #创建对话
        assistant_content = chat_completion.choices[0].message.content.strip() #模型回答文本
        self.__memory_dict[user_id].append({"role": "assistant", "content": assistant_content}) #记忆模型回复
        self.__memory_manager.save_user_memory(user_id=user_id, user_memory_dict=self.__memory_dict[user_id])
        return assistant_content

    def clear_memory(self,
                     user_id: int = 0):
        if user_id in self.__memory_dict.keys(): #用户ID存在于记忆字典
            self.__memory_dict[user_id] = []
