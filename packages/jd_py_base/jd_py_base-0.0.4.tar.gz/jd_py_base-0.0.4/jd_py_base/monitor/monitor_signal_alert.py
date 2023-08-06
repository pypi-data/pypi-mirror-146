# -*- coding: UTF-8 -*-
import smtplib
import traceback
import jdmssql
from email.mime.text import MIMEText
import time
import os
from example_demo.commons.common_fun import get_next_check_time

def send_mail(mail_host, email_list, sub, content, _from='msci@jindefund.com', debug=False):
    """
        发送邮件

        :param:str mail_host:
        :param:list email_list: 收件人列表
        :param:str sub: 主题
        :param:str content: 邮件内容
        :param:int _from: 发件人
        :param:bool debug:
    """
    from_addr = "zhangyf@jindefund.com"  # 这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content, _subtype='html', _charset='gb2312')  # 创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub  # 设置主题
    msg['From'] = _from
    msg['To'] = ";".join(email_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  # 连接smtp服务器
        s.sendmail(from_addr, email_list, msg.as_string())  # 发送邮件
        s.close()
        return True
    except Exception as e:
        if debug:
            traceback.print_exc()
            print("send email error : " + str(e))
        return False


def call_telephone(data_type, date_str, receiver, sub_data_type='A股市场', remind_info='download error', TemplateNO="2",
                   Status="0", CallResult="0", CallTimes="0", Memo="测试",
                   debug=False):
    """
        电话报警 表 VoiceCall

        :param:str data_type: 系统 （大类型）
        :param:str date_str:
        :param:str receiver: 接收人
        :param:str sub_data_type: 模板参数模块
        :param:str remind_info: 模板参数 提示信息
        :param:str TemplateNO: 内部模板号
        :param:str Status: 状态（0-待处理，1-已处理 ）
        :param:str CallResult: 处理结果
        :param:str CallTimes: 重试次数，最多重试5次，间隔2分钟
        :param:str Memo: 备注
        :param:bool debug:
        **表 VoiceCall
        [SerialNum]              int IDENTITY(1, 1) not null,       --自增索引值
        [TemplateNO]            int not null,                      --内部模板号
        [TemplateParas]          varchar(2048) not null,            --模板参数列表，以'|'分隔
        [Contact]               varchar(16) not null,             --联系人，填写域名
        [Status]                 int not null,                      --状态，0-待处理，1-已处理
        [CallResult]                int not null,                      --处理结果
        [CallTimes]                 int not null,                      --重试次数，最多重试5次，间隔2分钟
        [Memo]                   varchar(2048),                     --备注
        [OptName]                varchar(16) not null,                 --通知发起人
        [OptTime]                 datetime default getdate()            --入库时间
        *[SendTime]               真实发送时间，可用作定时，后续可看需新增


    """
    # %32x系统%32x模块出发告警，告警信息%32x%32x
    TemplateParas = f"{data_type}|{sub_data_type}|{date_str}|{remind_info}"
    Contact = receiver
    OptName = receiver
    sql = """insert into VoiceCall (Date, TemplateNO, TemplateParas, Contact, Status, CallResult, CallTimes, Memo, OptName, OptTime)
       values (convert(char(10), getDate(), 111),'""" + TemplateNO + """','""" + TemplateParas + """','""" + Contact + """',""" + Status + """,
       """ + CallResult + """,""" + CallTimes + """,'""" + Memo + """','""" + OptName + """',getdate())"""
    if debug:
        print(sql)
        return
    con = jdmssql.JDMSSQLHELPER(
        "CA393C4026A3EF1166558C24053F358E900E1F82CB84AA0BE8C94B92654BC5D99371FAC8CA195B77C739944344F06703EDCC4148943A72EFCBB1219DE6F49203")
    # print('类初始化时 ', con.isConnected(), con.isAlive())
    con.ExecNonQuery(sql)
    con.close()


def pipe_monitor_file(file_path, download_date, project_name, pipline_path, check_key_head, debug=False):
    """
        pipeline上报状态

        :param:str file_path:
        :param:str download_date:
        :param:str project_name:
        :param:str content:
        :param:str pipline_path:
        :param:str check_key_head:
        :param:bool debug:

    """
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cur_time_format = cur_time.replace(' ', 'T')
    next_check_time = get_next_check_time()
    if not os.path.exists(file_path):
        print('%s file_path not exists' % file_path)
        return
    check_key = check_key_head + str(file_path).split('\\')[-1].replace(download_date, '')
    print(check_key)
    cmd_str_1 = 'filereport -pt ' + project_name + ' -n ' + check_key + ' -gs True -f ' + str(
        os.path.getsize(file_path)) + ' -t ' + cur_time_format + ' -nr ' + next_check_time + ' -i "' + check_key + \
                ' check success,file:' + file_path + ',exists"'
    if debug:
        print(pipline_path + cmd_str_1)
    os.system(pipline_path + cmd_str_1)




def upload_singal_status(project_name, gen_state, update_time, singal_info, time_sleep=300, debug=False):
    """
        pipeline上传信号状态

        :param:str project_name: 项目名称
        :param:str gen_state: 生成状态（0，初始化；1，成功；-1 非交易盘；-100 失败）
        :param:str update_time: 更新时间
        :param:str singal_info: 信号信息 （init 初始化；info 成功；error 错误失败）
        :param:int time_sleep:
        :param:bool debug:
        :return: bool :

    """

    update_time_format = update_time.replace(' ', 'T')
    signal_cmd_str = f'D:\pipelinevenv\Scripts\plproxy signalset -n {project_name} -gs {gen_state} -f 0 -t {update_time_format} -i "{singal_info}" '

    if debug:
        print(signal_cmd_str)
        return False
    count = 0
    try:
        while count <= 6:
            status = os.system(signal_cmd_str)
            if status == 0:
                count = 10
            else:
                count += 1
                time.sleep(time_sleep)
    except Exception as e:
        error_signal_cmd_str = f'D:\pipelinevenv\Scripts\plproxy signalset -n {project_name} -gs -100 -f 0 -t {update_time_format} -i "error" '
        os.system(error_signal_cmd_str)
    return True if count == 10 else False


HK_signal_name = 'hk_trade_calendar'
cur_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
singal_info = 'info'
gen_state = 1

print(cur_time)
cur_time_format = cur_time.replace(' ', 'T')
print(cur_time_format)
upload_singal_status(HK_signal_name, gen_state, cur_time_format, singal_info, debug=True)