'''
用于统计要用于和成的文件夹的目标个数
并用柱状图显示
'''
#-*-UTF-8-*-
import matplotlib.pyplot as plt
import os
from pylab import mpl
import xml.etree.ElementTree as ET





def input_file_name():     
    file_name=input('需要查看的文件夹名称：')     
    print(type(file_name))     
    print(file_name)     
    return file_name






'''
提供自定义的绘图函数给obj_count.py
和obj_display.py使用
'''
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题



def draw_bar(source_data,x_label,y_label,flie_title):
    # ha 文字指定在柱体中间， va指定文字位置 fontsize指定文字体大小
    for a, b in source_data.items():
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)

    # 设置X轴Y轴数据，两者都可以是list或者tuple
    x_axis = tuple(source_data.keys())
    y_axis = tuple(source_data.values())

    
    plt.xlabel(x_label)  # 指定x轴描述信息
    plt.ylabel(y_label)  # 指定y轴描述信息
    plt.title(flie_title)  # 指定图表描述信息
    #plt.ylim(0, 600)  # 指定Y轴的高度
    #plt.savefig('{}.png'.format(time.strftime('%Y%m%d%H%M%S')))  # 保存为图片
    plt.bar(x_axis, y_axis,width=0.6,alpha=0.5, color='rgb')  # 如果不指定color，所有的柱体都会是一个颜色
    #plt.show()
    





def get_multi_label_path_list(multi_path):         #获取xml文件列表

    filenames_multi = []
    dic_file_m={}
    img_path=os.path.split(multi_path)[0]+'/img'  #将xml文件路径替换为为img文件路径
    img_list=os.listdir(img_path)                 #或取图片文件列表
    file_img=len(img_list)                        #获取图片文件个数
    #对xml文件进行分析
    for i in os.walk(multi_path):
        
        filenames_multi = filenames_multi + list(i)[2]                #获取完整的xml文件列表
    #print(multi_path)
    filenames_multi=[multi_path +'/'+ c for c in filenames_multi]     #所有文件完整路径的列表

    file_xml = len(filenames_multi)                                  #xml文件个数
    dic_file_m['xml']=file_xml                                       #字典形式的多标签文件个数统计
    dic_file_m['img']=file_img
    return filenames_multi,dic_file_m
    




#标签目标统计
def obj_count(list1,file_name):

    dic = {}
    num_1=0
    num_z=0
    label_name=[]
    #for m in range(len(label_name)):
        #dic[label_name[m]] = 0
    for i in list1:
        #print(i)
        xml_path=i
        in_file_test = open(xml_path, encoding='gb18030', errors='ignore')
        tree_test=ET.parse(in_file_test)
        root_test=tree_test.getroot()
        for obj_test in root_test.iter('object'):
            num_1=num_1+1                     #用来统计所有的目标总数
            #acc = obj_test.find('confidence').text
            cls = obj_test.find('name').text
            if cls in dic:
                dic[cls]=dic[cls]+1
            else:
                dic[cls] =1
                label_name.append(cls)  #所有标签名称列表
    for key_word in dic:
        num_z=num_z+dic[key_word]        #计算所有目标总数
    if(num_z==num_1):                    #判断统计结果是否正确
        #print('\n')
        
        #print('数据正确！')
        #print(dic)
        return dic,label_name           #返回统计结果字典和标签名称列表
    else:
        print(file_name + ':')
        print('数据与标签不符，请检查后再来生成数据！')




def display_m(dic_m,dic_file_m,label_name):
    print('\n')
    print('多标签数据统计:')
    for num in range(len(label_name)):
        print(label_name[num] + ':' + '\n' + 'obj个数：' + str(dic_m[label_name[num]]))
    print('文件个数：' + str(dic_file_m['img']))





if __name__=='__main__':
    #file_name=input_file_name()
    #para_path = './点击运行/配置文件.ini'
    #para=obj_count.get_para(para_path)
    #label_name=para[0]
    #file_name=para[1]
    file_path=r'E:\work\Experiment\data\image\fire_smoke_1\select_common\xml'
    file_name='123'
    mul_1 = get_multi_label_path_list(file_path)  # 返回元组，元素为所有xml文件路径列表，img和xml文件个数统计结果字典
    filenames_multi = mul_1[0]    #所有文件路径列表
    dic_file_m = mul_1[1]         #img和xml文件个数统计结果字典
    print(filenames_multi)
    print(dic_file_m)
    dic_m = obj_count(filenames_multi, file_name)    #返回统计结果字典和标签名称列表
    #print(dic_m[1])
    #print(type(dic_m[1]))
    display_m(dic_m[0], dic_file_m,dic_m[1])         #文本显示统计结果
    #绘图显示统计结果
    plt.figure()
    draw_bar(dic_m[0], 'obj统计', '标签数目', '')
    plt.savefig('1.png')
    plt.show()
    plt.figure()
    draw_bar(dic_file_m, '文件个数统计', '文件个数', '')
    plt.savefig('2.png')
    plt.show()

