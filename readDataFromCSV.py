#!/usr/bin/env python
# encoding: utf-8
from os import listdir
from os.path import isfile, join
import sys
import xlrd
# 第一个参数：要进行比较的所有 excel 文件，把所有要进行比较的 excel 文件放入一个目录中，目录中要包含 【./AE/4cpu16g】
# 第二个参数：确定固定参数，DB or QD
# 第三个参数：确定固定参数的值（DB：4k、16k、1m、4m、8m；QD：1、4、16、64）
# 第四个参数：想要显示的指标
# value 是二维数组，长度等于给定目录下文件的个数
# 数据块大小
numofdb = 5
# 队列宽度个数
numofqd = 4
# 将要进行比较的 csv / excel 文件放到一个目录中，即 csvFilePath
csvFilePath = sys.argv[1]
csvFileArray = [ f for f in listdir(csvFilePath) if isfile(join(csvFilePath, f)) ]
# 规格
flavor = csvFilePath.split('/')[-1]
# 固定参数为数据块时，输入 DB（data block）；固定参数为队列深度时，输入 QD（queue depth）
parameterFixed = sys.argv[2]
# 单位
unit = ''
# 固定参数的具体值（DB：4k、16k、1m、4m、8m；QD：1、4、16、64）
parameterValue = sys.argv[3]
if parameterFixed == 'DB':
    parameterValueDict = {'4K': 0, '16K': 1, '1M': 2, '4M': 3, '8M': 4}
elif parameterFixed == 'QD':
    parameterValueDict = {'1': 0, '4': 1, '16': 2, '64': 3}
else:
    print 'parameterValueDict is wrong'
# 指标id，即在 csv 中处于第几列，从 0 开始
index = int(sys.argv[4])
if index == 2:
    index_chinese = '顺序读'
    unit = 'KB/s'
elif index == 3:
    index_chinese = 'IOPS 读'
    unit = '次数'
elif index == 4:
    index_chinese = '顺序写'
    unit = 'KB/s'
elif index == 5:
    index_chinese = 'IOPS 写'
    unit = '次数'
elif index == 6:
    index_chinese = '随机读'
    unit = 'KB/s'
elif index == 7:
    index_chinese = '随机读 IOPS'
    unit = '次数'
elif index == 8:
    index_chinese = '随机写'
    unit = 'KB/s'
elif index == 9:
    index_chinese = '随机写 IOPS'
    unit = '次数'

# 纵坐标描述信息
if parameterFixed == 'DB':
    if index in (2, 4, 6, 8):
        DescriptionOfAbscissa = "\"" + flavor + '20G-' + '数据块' + parameterValue + "-" + index_chinese + "带宽-单位:(" + unit + ")\""
    else:
        DescriptionOfAbscissa = "\"" + flavor + '20G-' + '数据块' + parameterValue + "-" + index_chinese + "-单位:(" + unit + ")\""
else:
    if index in (2, 4, 6, 8):
        DescriptionOfAbscissa = "\"" + flavor + '20G-' + '队列深度' + parameterValue + "-" + index_chinese + "带宽-单位:(" + unit + ")\""
    else:
        DescriptionOfAbscissa = "\"" + flavor + '20G-' + '队列深度' + parameterValue + "-" + index_chinese + "-单位:(" + unit + ")\""

def getValue(csvFileName): # 第二个参数是固定参数，固定参数是 DB 或者是 QD
    value = []
    data = xlrd.open_workbook(csvFilePath + "/" + csvFileName)
    sheet = data.sheets()[0] # excel 表里的第一个也是唯一一个 sheet
    if parameterFixed == 'DB':
        for j in range(1 + parameterValueDict[parameterValue] * numofqd, 1 + parameterValueDict[parameterValue] * numofqd + numofqd - 1 + 1):
            value.append(sheet.cell(j, index).value)
        return value

    elif parameterFixed == 'QD':
        for j in range(numofdb):
            value.append(sheet.cell(1 + parameterValueDict[parameterValue]  + j * numofqd, index).value)
        return value

    else:
        print "---parameterFixed was not found!---"


if parameterFixed == 'DB':
    DescriptionOfOrdinate = ['队列深度：1', '队列深度：4', '队列深度：16', '队列深度：64']
elif parameterFixed == 'QD':
    DescriptionOfOrdinate = ['数据块：4K', '数据块：16K', '数据块：1M', '数据块：4M', '数据块：8M']
else:
    print 'DescriptionOfOrdinate was wrong'
# 将数组 DescriptionOfOrdinate 转成字符串
DescriptionOfOrdinateString = "["
for doo in DescriptionOfOrdinate:
    DescriptionOfOrdinateString += "\'" + doo + "\',"
DescriptionOfOrdinateString += "]"

# factoryClass 即 AE QE AEQ
factoryClass = csvFilePath.split('/')[-2]
if factoryClass == 'AE':
    with open('./Disk_Template_AE_small.html', 'r') as htmlFile:
        dataOfHtmlFile = htmlFile.read()
elif factoryClass == 'QE':
    with open('./Disk_Template_QE_small.html', 'r') as htmlFile:
        dataOfHtmlFile = htmlFile.read()
else:
    with open('./Disk_Template_AEQ_small.html', 'r') as htmlFile:
        dataOfHtmlFile = htmlFile.read()

dataOfHtmlFile = dataOfHtmlFile.replace('{DescriptionOfAbscissa}', DescriptionOfAbscissa)
dataOfHtmlFile = dataOfHtmlFile.replace('{DescriptionOfOrdinate}', DescriptionOfOrdinateString)
if parameterFixed == 'DB':
    num = numofdb
else:
    num = numofqd
#for i in range(len(csvFileArray)):
 #   print csvFileArray[i]
def printOut(value):
    for i in value:
        print int(i)
    print '--------'
for i in range(len(csvFileArray)):
    value = getValue(csvFileArray[i])
    if factoryClass == 'AE':
        if csvFileArray[i].split('_')[0] == 'ali1':
            dataOfHtmlFile = dataOfHtmlFile.replace('{AliyunNormal}', str(value))
        elif csvFileArray[i].split('_')[0] == 'ali2':
            dataOfHtmlFile = dataOfHtmlFile.replace('{AliyunHigh}', str(value))
        elif csvFileArray[i].split('_')[0] == 'ali3':
            dataOfHtmlFile = dataOfHtmlFile.replace('{AliyunSsd}', str(value))
        elif csvFileArray[i].split('_')[0] == 'eayun':
            dataOfHtmlFile = dataOfHtmlFile.replace('{Eayun}', str(value))
        else:
            print 'something about AE will be wrong ----------------'
    elif factoryClass == 'QE':
        if csvFileArray[i].split('_')[0] == 'qyun1':
            dataOfHtmlFile = dataOfHtmlFile.replace('{QingcloudNormalBig}', str(value))
        elif csvFileArray[i].split('_')[0] == 'qyun2':
            dataOfHtmlFile = dataOfHtmlFile.replace('{QingcloudNormal}', str(value))
        elif csvFileArray[i].split('_')[0] == 'qyun3':
            dataOfHtmlFile = dataOfHtmlFile.replace('{QingcloudHigh}', str(value))
        elif csvFileArray[i].split('_')[0] == 'eayun':
            dataOfHtmlFile = dataOfHtmlFile.replace('{Eayun}', str(value))
        else:
            print 'something about QE will be wrong ----------------'
    elif factoryClass == 'AEQ':
        if csvFileArray[i].split('_')[0] == 'ali1':
            dataOfHtmlFile = dataOfHtmlFile.replace('{AliyunNormal}', str(value))
            printOut(value)
        elif csvFileArray[i].split('_')[0] == 'ali2':
            printOut(value)
            dataOfHtmlFile = dataOfHtmlFile.replace('{AliyunHigh}', str(value))
        elif csvFileArray[i].split('_')[0] == 'ali3':
            printOut(value)
            dataOfHtmlFile = dataOfHtmlFile.replace('{AliyunSsd}', str(value))
        elif csvFileArray[i].split('_')[0] == 'eayun':
            printOut(value)
            dataOfHtmlFile = dataOfHtmlFile.replace('{Eayun}', str(value))
        elif csvFileArray[i].split('_')[0] == 'qyun1':
            printOut(value)
            dataOfHtmlFile = dataOfHtmlFile.replace('{QingcloudNormalBig}', str(value))
        elif csvFileArray[i].split('_')[0] == 'qyun2':
            printOut(value)
            dataOfHtmlFile = dataOfHtmlFile.replace('{QingcloudNormal}', str(value))
        elif csvFileArray[i].split('_')[0] == 'qyun3':
            printOut(value)
            dataOfHtmlFile = dataOfHtmlFile.replace('{QingcloudHigh}', str(value))
        else:
            print 'something about QE will be wrong ----------------'
    else:
        print 'factoryClass is wrong!'


if parameterFixed == 'DB':
    fixChineseName = '数据块'
else:
    fixChineseName = '队列深度'

ResultHTMLFileName = csvFilePath.split('/')[-1] + '20G-' + index_chinese + '-' + fixChineseName + '为' + parameterValue + '.html'
with open(ResultHTMLFileName, "w") as resultFile:
    resultFile.write(dataOfHtmlFile)
print "输出文件：" + ResultHTMLFileName
