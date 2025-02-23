readme.md

## main.py
Get url links to APKs for all categories of F-Droid

for example.
apk_name, have_lib, [arm64-v8a, armeabi-v7a, armeabi, x86, x86_64, mips, mips64, other], native-activity, ([jni_method_total_num, static_num, nostatic_num], [total_all_type, total_basic_type, total_icc_type, total_complex_type, total_complex_type]), [so_total_num, so_Java_num, so_onLoad_num], [have_other_elf, have_pwd_zip]
['xdsopl.robot36_64', 0, [0, 0, 0, 0, 0, 0, 0, 0], 0, ([0, 0, 0], [0, 0, 0, 0]), [0, 0, 0], [0, 0]]



## total_num.py
Compare the number of urls on the apk home page with the number of real apk download links.

In fact, 
number of urls on the apk home page: 4704
number of real apk download links: 4704


## build.py
build the apk download link 

## merge.py
merge the apk report information