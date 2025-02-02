def parse_line(line):
    return line.strip().replace(" ", "").replace("[", "").replace("]", "").replace(")", "").replace("(", "").split(",")


def update_counters(lists, counters):
    counters['have_lib'] += int(lists[1])
    counters['archs']['arm64_v8a'] += int(lists[2])
    counters['archs']['armeabi_v7a'] += int(lists[3])
    counters['archs']['armeabi'] += int(lists[4])
    counters['archs']['x86'] += int(lists[5])
    counters['archs']['x86_64'] += int(lists[6])
    counters['archs']['mips'] += int(lists[7])
    counters['archs']['mips64'] += int(lists[8])
    counters['archs']['other'] += int(lists[9])

    counters['native_activity'] += int(lists[10])

    if int(lists[11]) != 0:
        counters['have_native'] += 1
    counters['native_function_num'] += int(lists[11])
    counters['native_fun_stat'] += int(lists[12])
    counters['native_fun_nostat'] += int(lists[13])

    counters['total_all_type'] += int(lists[14])
    counters['total_basic_type'] += int(lists[15])
    counters['total_icc_type'] += int(lists[16])
    counters['total_complex_type'] += int(lists[17])

    counters['so_file'] += int(lists[18])
    counters['so_stat_file'] += int(lists[19])
    counters['so_dyan_file'] += int(lists[20])

    if int(lists[21]) != 0:
        counters['have_other_num'] += 1
    counters['have_other_elf'] += int(lists[21])
    if int(lists[1]) == 0 and int(lists[21]) != 0:
        counters['res'] += 1
    if int(lists[22]) != 0:
        counters['have_pwd_num'] += 1
    counters['have_pwd_zip'] += int(lists[22])


def print_summary(counters, total_lines):
    # Print total statistics
    print("total_num", total_lines)
    print("have_lib", counters['have_lib'], "par", counters['have_lib'] / total_lines if total_lines > 0 else 0)
    print("have_native", counters['have_native'], "par",
          counters['have_native'] / total_lines if total_lines > 0 else 0)

    print("============arch=============")
    if counters['have_lib'] == 0:
        for arch, count in counters['archs'].items():
            print(f"{arch}: {count}")
    else:
        for arch, count in counters['archs'].items():
            print(f"{arch}: {count}, par: {count / counters['have_lib']}")

    print("============native_activity==========")
    print("native_activity", counters['native_activity'])

    print("===========native func============")
    if counters['native_function_num'] == 0:
        print("native_function_num 0")
        print("native_fun_stat", counters['native_fun_stat'])
        print("native_fun_nostat", counters['native_fun_nostat'])
    else:
        print("native_function_num", counters['native_function_num'])
        print("native_fun_stat", counters['native_fun_stat'], "par",
              counters['native_fun_stat'] / counters['native_function_num'])
        print("native_fun_nostat", counters['native_fun_nostat'], "par",
              counters['native_fun_nostat'] / counters['native_function_num'])

    print("=============native type==============")
    if counters['total_all_type'] == 0:
        print("total_all_type 0")
        print("total_basic_type", counters['total_basic_type'])
        print("total_icc_type", counters['total_icc_type'])
        print("total_complex_type", counters['total_complex_type'])
    else:
        print("total_all_type", counters['total_all_type'])
        print("total_basic_type", counters['total_basic_type'], "par",
              counters['total_basic_type'] / counters['total_all_type'])
        print("total_icc_type", counters['total_icc_type'], "par",
              counters['total_icc_type'] / counters['total_all_type'])
        print("total_complex_type", counters['total_complex_type'], "par",
              counters['total_complex_type'] / counters['total_all_type'])

    print("===============so static or dynamic============")
    if counters['so_file'] == 0:
        print("so_file", counters['so_file'])
        print("so_static_file", counters['so_stat_file'])
        print("so_dynamic_file", counters['so_dyan_file'])
    else:
        print("so_file", counters['so_file'])
        print("so_static_file", counters['so_stat_file'], "par", counters['so_stat_file'] / counters['so_file'])
        print("so_dynamic_file", counters['so_dyan_file'], "par", counters['so_dyan_file'] / counters['so_file'])

    print("============other inf=========")
    print("have_other_num", counters['have_other_num'])
    print("have_pwd_num", counters['have_pwd_num'])

    if total_lines == 0:
        print("have_other_elf", counters['have_other_elf'], "par 0")
        print("have_pwd_zip", counters['have_pwd_zip'], "par 0")
    else:
        print("have_other_elf", counters['have_other_elf'], "par", counters['have_other_num'] / total_lines)
        print("have_pwd_zip", counters['have_pwd_zip'], "par", counters['have_pwd_num'] / total_lines)

    print("=============finish============")
    print("defailed_num", counters.get('defailed', 0))
    print("res", counters['res'])


def main():
    counters = {
        'have_lib': 0,
        'have_native': 0,
        'native_activity': 0,
        'native_function_num': 0,
        'native_fun_stat': 0,
        'native_fun_nostat': 0,
        'total_all_type': 0,
        'total_basic_type': 0,
        'total_icc_type': 0,
        'total_complex_type': 0,
        'so_file': 0,
        'so_stat_file': 0,
        'so_dyan_file': 0,
        'have_other_elf': 0,
        'have_pwd_zip': 0,
        'have_other_num': 0,
        'have_pwd_num': 0,
        'res': 0,
        'archs': {
            'arm64_v8a': 0,
            'armeabi_v7a': 0,
            'armeabi': 0,
            'x86': 0,
            'x86_64': 0,
            'mips': 0,
            'mips64': 0,
            'other': 0,
        },
        'defailed': 0,
    }

    try:
        with open("type1_3500.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                lists = parse_line(line)
                if len(lists) == 23:
                    update_counters(lists, counters)
                else:
                    counters['defailed'] += 1

        print_summary(counters, len(lines))

    except FileNotFoundError:
        print("Error: report.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
