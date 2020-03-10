from crnn import t01
from Dictionary_FYP import dict_using_ginger
from Keyphrase_FYP import test

d_s = t01.segment_process("crnn/Images/i.png")

c_s = dict_using_ginger.spell_checker(d_s)

f_s = test.new(c_s)


