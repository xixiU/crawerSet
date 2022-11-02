#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-27 18:44:31
# @Author  : yuan
# @Version : 1.0.0
# @describe: 

# 伪装浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}
# Cookie有点重要，不然访问要失败，不过也可以用selenium，省去了自己拼装的麻烦
bd_headers = {
    'Cookie': 'BIDUPSID=8640A1C37FE0690CCFD0ADC95CDD0614; PSTM=1573012288; BAIDUID=8640A1C37FE0690C2FF67C0B307E1236:FG=1; BD_UPN=12314753; BDSFRCVID=cHFOJeC62xSAeNnwFmf5T97SHxCLPfRTH6aVosjQ3KdSxvaQuPVtEG0Pjx8g0KA-Nb29ogKKXgOTHw0F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR-tVCtatCI3HnRv5t8_5-LH-UoX-I62aKDs-Dt2BhcqEIL4hhLV3-4X5pjrWlcPMDnU5R5ctfJ8DUbSj4Qo5Pky-H3pQROhfnAJKRQH0q5nhMJN3j7JDMP0-xPfa5Oy523ihn3vQpnbhhQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0Djb-jN0qJ6FsKKJ03bk8KRREJt5kq4bohjnDjgc9BtQmJJrt2-T_5CQbflRmypo0bh-FBn8HJq4tQg-q3R7JJDTxEDO4jJQiWlTLQf5v0x-jLgbPVn0MW-5DSlI4qtnJyUPRbPnnBn-j3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CFhJKIbhKLlejRjh-FSMgTK2Pc8bC_X3b7EfMjpsh7_bf--D6cLbpAe5JbqBTnK-4ceQhj1oMFGLpOxy5K_hP6x2U70WNOfLMcHbRclHDbHQT3mMRvbbN3i34jpWRuLWb3cWMnJ8UbS5T3PBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGKJJ6LqJJ4HV-35b5raeR5g5DTjhPrM2RQAWMT-0bFH_---ahQofPcFLtTxej-9yMcU55cUJGn7_JjOWCOds-J2hU5hLnLW2b37BxQxtNRd2CnjtpvhHRnRbP5obUPUWMJ9LUvftgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtCthMI04ejt35n-Wqx5KhtvtK65tsJOOaCvjOhQOy4oTj6Db0PQ-Wt6f3Djh_x-XJMO1JhOs0-jC3MvB-Jjyb-TIt23bb-nKKxjhVMQmQft20-IbeMtjBM_LBDuHVR7jWhviep72ybt2QlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjH62btt_tJk8_CoP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1427_21089_18560_29568_29220_28702; delPer=0; BD_CK_SAM=1; PSINO=7; COOKIE_SESSION=11616_0_9_9_7_46_0_3_9_6_8_20_261159_0_34_0_1574317407_0_1574317373%7C9%23334846_17_1574055214%7C4; BD_HOME=0; H_PS_645EC=a2613mtU9Z3zzlE3Z%2BGp%2Bj49ILi6lAP%2Fqx95Q%2FkEvc3CO5Lp9KZCsfjQvzU',
    # 'Host': 'www.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',

}


debug_mode = True #　debug模式会显示Ui,正常运行可以不启动ｕi，在非windowsX环境配置定时脚本　，可以自动填
singleton_timeout = 5# time out for single page
id_password_set=[("yourid","password")] #支持多线程调用，填上多人的信息即可

