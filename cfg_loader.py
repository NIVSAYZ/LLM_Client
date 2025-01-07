def load_config(cfg_path):
    cfg_dict = dict()
    cfg_lines = open(cfg_path, "r", encoding="utf-8").readlines()

    for cfg_line in cfg_lines[1:]:
        cfg_line = cfg_line.strip()
        if not cfg_line or cfg_line[0] == "#":
            continue
        line_start, line_value = cfg_line.split("=")
        cfg_dict[line_start] = line_value
    return cfg_dict
