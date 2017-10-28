# myTools
myTools
## addr_trans.py
python addr_trans.py -w 64 -e b 0x7FFFF78FE390 ==> \x00\x00\x7F\xFF\xF7\x8F\xE3\x90
## binary_dump.py
python binary-dump.py -s 192.168.2.14 -f /Users/gjy/Desktop/test_yqb/expression.ipa -o binary/

python binary-dump.py -s 192.168.2.14 -i com.tencent.xin -o binary/

目前脱壳只采用了clutch。
## br_class.py
command script import br_class.py
添加bc命令，使用方法：bc class_name，为该类的所有instance method下断点，并在断点触发时输出该method的名字。
