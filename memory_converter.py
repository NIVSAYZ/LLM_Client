import os
import sys
import zlib


def dat_to_txt(item_path):
    memory_save = open(item_path, "rb").read()  # 读取交流记录
    memory_bytes = zlib.decompress(memory_save)
    output_path = os.path.dirname(item_path) + "\\" + os.path.basename(item_path).replace(".dat", ".txt")
    output = open(output_path, "w", encoding="utf-8")
    output.write(memory_bytes.decode(encoding="utf-8"))
    output.close()


def txt_to_dat(item_path):
    memory_text = open(item_path, "r", encoding="utf-8").read()
    memory_bytes = zlib.compress(memory_text.encode(encoding="utf-8"), level=9)
    output_path = os.path.dirname(item_path) + "\\" + os.path.basename(item_path).replace(".txt", ".dat")
    output = open(output_path, "wb")
    output.write(memory_bytes)
    output.close()


item_path_list = sys.argv[1:]
for item_path in item_path_list:
    if ".dat" in item_path:
        dat_to_txt(item_path)

    elif ".txt" in item_path:
        txt_to_dat(item_path)
