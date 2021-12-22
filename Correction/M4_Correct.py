import os
import sys
sys.path.append('/root/fairseq-gec-master/gec_scripts/')
import split_new
import revert_split_new
import time


def Correct(Spell_corrected_context):

    src_trg, idx = split_new.split(Spell_corrected_context)

    # f1=open('/root/fairseq-gec-master/test/raw/test.src-tgt.src', 'w')
    # f2=open('/root/fairseq-gec-master/test/raw/test.src-tgt.tgt', 'w')
    # for line in src_trg:
    #     f1.write(line)
    #     f1.write('\n')
    #     f2.write(line)
    #     f2.write('\n')
    # f1.close()
    # f2.close()
    M4__start_time = time.time()
    with open('/root/fairseq-gec-master/test/raw/test.src-tgt.src', 'w') as f:
        for line in src_trg:
            f.write(line)
            f.write('\n')

    with open('/root/fairseq-gec-master/test/raw/test.src-tgt.tgt', 'w') as f:
        for line in src_trg:
            f.write(line)
            f.write('\n')

    print("correction,",time.time() - M4__start_time)
    # with open('/home/wangyu/fairseq-gec-master/test/raw/test.idx', 'w') as f:
    #     for line in idx:
    #         f.write(str(line))
    #         f.write('\n')

#    os.system('bash /root/fairseq-gec-master/correct_new.sh -1 _pretrained')

    os.system('cd /root/fairseq-gec-master; bash correct_new.sh -1 _pretrained;')


    # with open('/home/wangyu/fairseq-gec-master/test/result/outputema.new.txt.split') as f:
    output_split = open('/root/fairseq-gec-master/test/result/outputema.new.txt.split').readlines()
    # idx = open('/home/wangyu/fairseq-gec-master/test/raw/test.idx').readlines()

    idx_str = []
    for id in idx:
        idx_str.append(str(id))

    print("idx_str,",time.time() - M4__start_time)
    Grammar_corrected_context = revert_split_new.main(output_split, idx_str)

    print("Grammar_corrected_context,",time.time() - M4__start_time)
    return Grammar_corrected_context


if __name__ == '__main__':
    with open('/root/code/wy/Correction/M4_M5_Data/test.error.sent', 'r') as f:
        Spell_corrected_context = f.readlines()

    answer = Correct(Spell_corrected_context)
    print(answer)
