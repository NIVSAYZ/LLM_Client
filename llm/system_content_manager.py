import time
import cnlunar
import datetime


class SystemContentManager:
    def __init__(self,
                 system_content: str = ""):
        self.system_content = system_content

    # ===动态提示词===
    def update_prompt(self, user_name=""):
        if not self.system_content:
            return ""
        dynamic_system_content = self.system_content  # 提示词模板

        # ===cnlunar===
        local_time = time.localtime()  # 读取本地时间
        date_time = datetime.datetime(local_time[0], local_time[1], local_time[2], local_time[3], local_time[4])
        cn_lunar = cnlunar.Lunar(date_time, godType='8char')

        # ===用户名写入===
        if "{user_name}" in self.system_content:
            dynamic_system_content = dynamic_system_content.replace("{user_name}", user_name)  # 写入用户名

        # ===用户时间写入===
        if "{user_time}" in self.system_content:
            std_time = time.strftime("%Y年%m月%d日%H时%M分%S秒", local_time)  # 转化为标准时间
            dynamic_system_content = dynamic_system_content.replace("{user_time}", std_time)  # 写入当前时间

        # ===ALIYA时间写入===
        if "{aliya_time}" in self.system_content:
            aliya_time = "{}年{}月{}日{}时{}分{}秒".format(local_time[0] + 1000, local_time[1], local_time[2],
                                                           local_time[3], local_time[4], local_time[5])
            dynamic_system_content = dynamic_system_content.replace("{aliya_time}", aliya_time)  # 写入当前时间

        # ===当天节气写入===
        if "{solar_terms}" in self.system_content:
            solar_terms = cn_lunar.todaySolarTerms
            dynamic_system_content = dynamic_system_content.replace("{solar_terms}", solar_terms)  # 写入当天节气

        if "{holiday}" in self.system_content:
            holiday = cn_lunar.get_otherHolidays()
            if not holiday:
                holiday = "无"
            dynamic_system_content = dynamic_system_content.replace("{holiday}", holiday)  # 写入当天节日
        return dynamic_system_content
