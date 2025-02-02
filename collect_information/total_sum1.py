
if __name__=="__main__":
    have_lib,have_native=0,0
    arm64_v8a,armeabi_v7a,armeabi,x86,x86_64,mips,mips64,other=0,0,0,0,0,0,0,0
    native_activity=0
    native_function_num,native_fun_stat,native_fun_nostat=0,0,0
    so_file,so_stat_file,so_dyan_file=0,0,0
    defailed=0
    total_all_type,total_basic_type,total_icc_type,total_complex_type=0,0,0,0
    have_other_elf,have_pwd_zip=0,0
    have_other_num,have_pwd_num=0,0
    res=0
    with open("type1_3500.txt","r") as f:
        lines=f.readlines()
        for i in lines:
            lists=i.strip().replace(" ","").replace("[","").replace("]","").replace(")","").replace("(","").split(",")
            if len(lists)==23:
                have_lib+=int(lists[1])
                arm64_v8a+=int(lists[2])
                armeabi_v7a+=int(lists[3])
                armeabi+=int(lists[4])
                x86+=int(lists[5])
                x86_64+=int(lists[6])
                mips+=int(lists[7])
                mips64+=int(lists[8])
                other+=int(lists[9])

                native_activity+=int(lists[10])

                if int(lists[11])!=0:
                    have_native+=1
                native_function_num+=int(lists[11])
                native_fun_stat+=int(lists[12])
                native_fun_nostat+=int(lists[13])

                total_all_type+=int(lists[14])
                total_basic_type+=int(lists[15])
                total_icc_type+=int(lists[16])
                total_complex_type+=int(lists[17])

                so_file+=int(lists[18])
                so_stat_file+=int(lists[19])
                so_dyan_file+=int(lists[20])

                if int(lists[21])!=0:
                    have_other_num+=1
                have_other_elf+=int(lists[21])
                if int(lists[1])==0 and int(lists[21])!=0:
                    res=res+1
                if int(lists[22])!=0:
                    have_pwd_num+=1
                have_pwd_zip+=int(lists[22])
            else:
                defailed+=1
    f.close()
    if len(lines)==0:
        print("total_num 0")
        print("have_lib",have_lib)
        print("have_native",have_native)
    else:
        print("total_num",len(lines))
        print("have_lib",have_lib,"par",have_lib/len(lines))
        print("have_native",have_native,"par",have_native/len(lines))
    print("============arch=============")
    if have_lib==0:
        print("arm64_v8a",arm64_v8a)
        print("armeabi-v7a",armeabi_v7a)
        print("armeabi",armeabi)
        print("x86",x86)
        print("x86_64",x86_64)
        print("mips",mips)
        print("mips64",mips64)
        print("other",other)
    else:
        print("arm64_v8a",arm64_v8a,"par",)
        print("armeabi-v7a",armeabi_v7a,"par",armeabi_v7a/have_lib)
        print("armeabi",armeabi,"par",armeabi/have_lib)
        print("x86",x86,"par",x86/have_lib)
        print("x86_64",x86_64,"par",x86_64/have_lib)
        print("mips",mips,"par",mips/have_lib)
        print("mips64",mips64,"par",mips64/have_lib)
        print("other",other,"par",other/have_lib)
    print("============native_activity==========")
    print("native_activity",native_activity)
    print("===========native func============")
    if native_function_num==0:
        print("native_function_num 0")
        print("native_fun_stat",native_fun_stat)
        print("native_fun_nostat",native_fun_nostat)
    else:
        print("native_function_num",native_function_num)
        print("native_fun_stat",native_fun_stat,"par",native_fun_stat/native_function_num)
        print("native_fun_nostat",native_fun_nostat,"par",native_fun_nostat/native_function_num)
    print("=============native type==============")
    if total_all_type==0:
        print("total_all_type 0")
        print("total_basic_type",total_basic_type)
        print("total_icc_type",total_icc_type)
        print("total_complex_type",total_complex_type)
    else:
        print("total_all_type",total_all_type)
        print("total_basic_type",total_basic_type,"par",total_basic_type/total_all_type)
        print("total_icc_type",total_icc_type,"par",total_icc_type/total_all_type)
        print("total_complex_type",total_complex_type,"par",total_complex_type/total_all_type)

    print("===============so static or dynamic============")
    if so_file==0:
        print("so_file",so_file)
        print("so_static_file",so_stat_file)
        print("so_dynamic_file",so_dyan_file)
    else:
        print("so_file",so_file)
        print("so_static_file",so_stat_file,"par",so_stat_file/so_file)
        print("so_dynamic_file",so_dyan_file,"par",so_dyan_file/so_file)
    print("============other inf=========")
    print("have_other_num",have_other_num)
    print("have_pwd_num",have_pwd_num)

    if len(lines)==0:
        print("have_other_elf",have_other_elf,"par 0")
        print("have_pwd_zip",have_pwd_zip,"par 0")
    else:
        print("have_other_elf",have_other_elf,"par",have_other_num/len(lines))
        print("have_pwd_zip",have_pwd_zip,"par",have_pwd_num/len(lines))
    print("=============finish============")
    print("defailed_num",defailed)

    print(res)

            