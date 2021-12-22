# 向服务器传输文件
import paramiko


Location = '315'  # '315' or 'ali'
switch = 0  # 时刻上传实验室服务器改单词后的句子

if Location == '315':  # 315实验室服务器
    tran = paramiko.Transport(('192.168.1.54', 22))
    tran.connect(username="dangkai", password='123456')
    sftp = paramiko.SFTPClient.from_transport(tran)
    Choose = 'Upload'  # 'Download' or 'Upload'
    if Choose == 'Upload':
        localpath = "../../code.tar.gz"
        remotepath = "/home/dangkai/code_slow.tar.gz"
        sftp.put(localpath, remotepath)
    if Choose == 'Download':
        localpath = "M4_M5_Data/corrected.sent"
        remotepath = "/home/dangkai/fairseq-gec-master/test/result/corrected.sent"
        sftp.get(remotepath, localpath)
    tran.close()

if Location == 'ali':  # 云服务器
    tran = paramiko.Transport(('47.94.156.250', 22))
    tran.connect(username="root", password='nkunlp2019+')
    sftp = paramiko.SFTPClient.from_transport(tran)
    Choose = 'Upload'  # 'Download' or 'Upload'
    if Choose == 'Upload':  # 上传
        localpath = "../../code.tar.gz"
        remotepath = "/home/admin/NLP6/code.tar.gz"
        sftp.put(localpath, remotepath)
    if Choose == 'Download':  # 下载
        localpath = "C:/Users/Lz/Desktop/Program-py/Web.tar.gz"
        remotepath = "/home/admin/NLP6/Web.tar.gz"
        sftp.get(remotepath, localpath)
    tran.close()

if switch == 1:  # 315实验室服务器
    tran = paramiko.Transport(('192.168.1.54', 22))
    tran.connect(username="dangkai", password='123456')
    sftp = paramiko.SFTPClient.from_transport(tran)

    localpath = "C:/Users/Lz/Desktop/Program-py/0Web+Correction(here)/Correction/M4_M5_Data/test.error.sent"
    remotepath = "/home/dangkai/fairseq-gec-master/test/raw/test.error.sent"
    sftp.put(localpath, remotepath)

    tran.close()
