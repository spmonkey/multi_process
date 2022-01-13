# -*- coding: utf-8 -*-
import multiprocessing
import requests, re, time, shutil
from bs4 import BeautifulSoup
import json, sys, msvcrt, os
from multiprocessing import Process
from tqdm import *
task_list = [
 'https://so.gushiwen.cn/gushi/tangshi.aspx',
 'https://so.gushiwen.cn/gushi/songsan.aspx',
 'https://so.gushiwen.cn/gushi/sanbai.aspx']
gushiwen_list = [
 '唐诗',
 '宋词',
 '古诗']

# time_tangshi = []
# time_songci = []
# time_gushi = []
class multi_process(object):
    # for i in range(len(task_list)):
    #     regular = '/shiwenv_.+\\.aspx'
    #     request_url = requests.get(task_list[i])
    #     html = request_url.text
    #     url_gushiwen = 'https://so.gushiwen.cn'
    #     html_txt = re.findall(regular, html)

    def tangshi(self,json_path):
        regular = '/shiwenv_.+\\.aspx'
        request_url = requests.get(task_list[0])
        html = request_url.text
        url_gushiwen = 'https://so.gushiwen.cn'
        html_txt = re.findall(regular, html)
        # print(html_txt)
        title_txt1 = []
        title_txt2 = []
        p_txt1 = []
        p_txt2 = []
        result = []
        try:
            for i in tqdm(range(len(html_txt))):
                result.clear()
                soup_reque = requests.get(url_gushiwen + html_txt[i]).content
                soup = BeautifulSoup(soup_reque, 'lxml')
                title_h1 = soup.find_all('h1')
                for txt in title_h1:
                    title_txt1.append(txt.string)
                    # print("唐诗标题：",txt.string)
                    soup_reque = requests.get(url_gushiwen + html_txt[i]).content
                    text = BeautifulSoup(soup_reque, 'lxml')
                    text_txts = str(text.find(attrs={'class': 'contson'})).split('<br/>')
                    title_h2 = soup.find('h2')
                    for text_txt in text_txts:
                        a = re.sub('<div class="contson" id="contson.+\\">', '', str(text_txt))
                        b = re.sub('<p>', '', a)
                        c = re.sub('</p>', '', b)
                        d = re.sub('</div>', '', c)
                        e = re.sub('\\n', '', d)
                        p_txt1.append(e.encode('gbk', 'ignore').decode('gbk'))
                    if title_h2 == '<h2><span style="float:left;">译文及注释</span></h2>':
                        title_txt2.append(title_h2.string)
                        translation = str(soup.find(name='div', attrs={'class': 'contyishang'})).split('<br/>')
                        data = '展开阅读全文'
                        data_txts = re.findall(data, str(translation))
                        if data_txts == []:
                            for translation_txt in translation:
                                translation_txts1 = re.sub('<div class="contyishang">', '', str(translation_txt))
                                translation_txts2 = re.sub('<div style="height:30px; font-weight:bold; font-size:16px; margin-bottom:10px; clear:both;">', '', translation_txts1)
                                translation_txts3 = re.sub('<h2><span style="float:left;">译文及注释</span></h2>', '', translation_txts2)
                                translation_txts4 = re.sub('<span id="fanyiPlay.+\\" style=" display:none;width:1px; height:1px; float:left;"></span>', '', translation_txts3)
                                translation_txts5 = re.sub('<img alt="" height="16" id="speakerimgFanyi.+" src="https://song.gushiwen.cn/siteimg/speak-er.png" width="16"/></a>', '', translation_txts4)
                                translation_txts6 = re.sub('<div class="contyishang" style="padding-bottom:10px;">', '', translation_txts5)
                                translation_txts7 = re.sub('<a href="javascript:PlayFanyi(.+,.+)" style="float:left; margin-top:7px; margin-left:5px;">', '', translation_txts6)
                                translation_txts8 = re.sub('<div style="text-align:center; margin-top:-5px;">', '', translation_txts7)
                                translation_txts9 = re.sub('<p>', '', translation_txts8)
                                translation_txts10 = re.sub('<strong>', '', translation_txts9)
                                translation_txts11 = re.sub('</strong>', '', translation_txts10)
                                translation_txts12 = re.sub('</p>', '', translation_txts11)
                                translation_txts13 = re.sub('</div>', '', translation_txts12)
                                translation_txts14 = re.sub('\\n', '', translation_txts13)
                                translation_txts15 = re.sub('<a href="https://so.gushiwen.cn/authorv_.+.aspx" target="_blank">', '', translation_txts14)
                                translation_txts16 = re.sub('</a>', '', translation_txts15)
                                p_txt2.append(translation_txts16.encode('gbk', 'ignore').decode('gbk'))

                        else:
                            a = re.findall('<a href="javascript:fanyiShow(.+,.+)" style="text-decoration:none;">', str(translation))
                            b = re.compile('(\\w+)')
                            c = b.findall(str(a))
                            reg = 'https://so.gushiwen.cn/nocdn/ajaxfanyi.aspx?id=%s' % c[1]
                            soup_reg = requests.get(reg).content
                            text_1 = BeautifulSoup(soup_reg, 'lxml')
                            translation_txts17 = str(text_1.find('p')).split('<br/>')
                            for translation_txt in translation_txts17:
                                translation_txts18 = re.sub('<p><strong>', '', translation_txt)
                                translation_txts19 = re.sub('</strong>', '', translation_txts18)
                                translation_txts20 = re.sub('</p>', '', translation_txts19)
                                translation_txts21 = re.sub('<a href="https://so.gushiwen.cn/authorv_.+.aspx" target="_blank">', '', translation_txts20)
                                translation_txts22 = re.sub('</a>', '', translation_txts21)
                                if translation_txts22 == '<p>未登录':
                                    continue
                                p_txt2.append(translation_txts22.encode('gbk', 'ignore').decode('gbk'))

                    lst_title1 = ''.join(title_txt1)
                    lst_text = ''.join(p_txt1)
                    lst_title2 = ''.join(title_txt2)
                    lst_translation = ''.join(p_txt2)
                    item = {'title':lst_title1,
                     'text':lst_text,
                     'translation and notes':lst_title2,
                     'translation':lst_translation}
                    result.append(item)
                    with open(json_path + '\\%s' % gushiwen_list[0] + '\\%s.json' % txt.string, 'a') as (dump_file):
                        title_txt1.clear()
                        p_txt1.clear()
                        title_txt2.clear()
                        p_txt2.clear()
                        dump_file.write(json.dumps(result, ensure_ascii=False))
            pass
        except Exception as e:
            print('唐诗爬取出现问题了，请复制这条报错给开发人员：', e)
            print('请输入任意键退出程序！！！')
            if ord(msvcrt.getche()) == [0, 100]:
                sys.exit()

    def songci(self,json_path):
        regular = '/shiwenv_.+\\.aspx'
        request_url = requests.get(task_list[1])
        html = request_url.text
        url_gushiwen = 'https://so.gushiwen.cn'
        html_txt = re.findall(regular, html)
        title_txt1 = []
        title_txt2 = []
        p_txt1 = []
        p_txt2 = []
        result = []
        try:
            for i in tqdm(range(len(html_txt))):
                result.clear()
                soup_reque = requests.get(url_gushiwen + html_txt[i]).content
                soup = BeautifulSoup(soup_reque, 'lxml')
                title_h1 = soup.find_all('h1')
                for txt in title_h1:
                    title_txt1.append(txt.string)
                    # print("宋词标题：", txt.string)
                    soup_reque = requests.get(url_gushiwen + html_txt[i]).content
                    text = BeautifulSoup(soup_reque, 'lxml')
                    text_txts = str(text.find(attrs={'class': 'contson'})).split('<br/>')
                    title_h2 = soup.find('h2')
                    for text_txt in text_txts:
                        a = re.sub('<div class="contson" id="contson.+\\">', '', str(text_txt))
                        b = re.sub('<p>', '', a)
                        c = re.sub('</p>', '', b)
                        d = re.sub('</div>', '', c)
                        e = re.sub('\\n', '', d)
                        p_txt1.append(e.encode('gbk', 'ignore').decode('gbk'))

                    if title_h2 == '<h2><span style="float:left;">译文及注释</span></h2>':
                        title_txt2.append(title_h2.string)
                        translation = str(soup.find(name='div', attrs={'class': 'contyishang'})).split('<br/>')
                        data = '展开阅读全文'
                        data_txts = re.findall(data, str(translation))
                        if data_txts == []:
                            for translation_txt in translation:
                                translation_txts1 = re.sub('<div class="contyishang">', '', str(translation_txt))
                                translation_txts2 = re.sub('<div style="height:30px; font-weight:bold; font-size:16px; margin-bottom:10px; clear:both;">', '', translation_txts1)
                                translation_txts3 = re.sub('<h2><span style="float:left;">译文及注释</span></h2>', '', translation_txts2)
                                translation_txts4 = re.sub('<span id="fanyiPlay.+\\" style=" display:none;width:1px; height:1px; float:left;"></span>', '', translation_txts3)
                                translation_txts5 = re.sub('<img alt="" height="16" id="speakerimgFanyi.+" src="https://song.gushiwen.cn/siteimg/speak-er.png" width="16"/></a>', '', translation_txts4)
                                translation_txts6 = re.sub('<div class="contyishang" style="padding-bottom:10px;">', '', translation_txts5)
                                translation_txts7 = re.sub('<a href="javascript:PlayFanyi(.+,.+)" style="float:left; margin-top:7px; margin-left:5px;">', '', translation_txts6)
                                translation_txts8 = re.sub('<div style="text-align:center; margin-top:-5px;">', '', translation_txts7)
                                translation_txts9 = re.sub('<p>', '', translation_txts8)
                                translation_txts10 = re.sub('<strong>', '', translation_txts9)
                                translation_txts11 = re.sub('</strong>', '', translation_txts10)
                                translation_txts12 = re.sub('</p>', '', translation_txts11)
                                translation_txts13 = re.sub('</div>', '', translation_txts12)
                                translation_txts14 = re.sub('\\n', '', translation_txts13)
                                translation_txts15 = re.sub('<a href="https://so.gushiwen.cn/authorv_.+.aspx" target="_blank">', '', translation_txts14)
                                translation_txts16 = re.sub('</a>', '', translation_txts15)
                                p_txt2.append(translation_txts16.encode('gbk', 'ignore').decode('gbk'))

                        else:
                            a = re.findall('<a href="javascript:fanyiShow(.+,.+)" style="text-decoration:none;">', str(translation))
                            b = re.compile('(\\w+)')
                            c = b.findall(str(a))
                            reg = 'https://so.gushiwen.cn/nocdn/ajaxfanyi.aspx?id=%s' % c[1]
                            soup_reg = requests.get(reg).content
                            text_1 = BeautifulSoup(soup_reg, 'lxml')
                            translation_txts17 = str(text_1.find('p')).split('<br/>')
                            for translation_txt in translation_txts17:
                                translation_txts18 = re.sub('<p><strong>', '', translation_txt)
                                translation_txts19 = re.sub('</strong>', '', translation_txts18)
                                translation_txts20 = re.sub('</p>', '', translation_txts19)
                                translation_txts21 = re.sub('<a href="https://so.gushiwen.cn/authorv_.+.aspx" target="_blank">', '', translation_txts20)
                                translation_txts22 = re.sub('</a>', '', translation_txts21)
                                if translation_txts22 == '<p>未登录':
                                    continue
                                p_txt2.append(translation_txts22.encode('gbk', 'ignore').decode('gbk'))

                    lst_title1 = ''.join(title_txt1)
                    lst_text = ''.join(p_txt1)
                    lst_title2 = ''.join(title_txt2)
                    lst_translation = ''.join(p_txt2)
                    item = {'title':lst_title1,
                     'text':lst_text,
                     'translation and notes':lst_title2,
                     'translation':lst_translation}
                    result.append(item)
                    with open(json_path + '\\%s' % gushiwen_list[1] + '\\%s.json' % txt.string, 'a') as (dump_file):
                        title_txt1.clear()
                        p_txt1.clear()
                        title_txt2.clear()
                        p_txt2.clear()
                        dump_file.write(json.dumps(result, ensure_ascii=False))
            pass
        except Exception as e:
            print('宋词爬取出现问题了，请复制这条报错给开发人员：', e)
            print('请输入任意键退出程序！！！')
            if ord(msvcrt.getche()) == [0, 100]:
                sys.exit()

    def gushi(self,json_path):
        regular = '/shiwenv_.+\\.aspx'
        request_url = requests.get(task_list[2])
        html = request_url.text
        url_gushiwen = 'https://so.gushiwen.cn'
        html_txt = re.findall(regular, html)
        title_txt1 = []
        title_txt2 = []
        p_txt1 = []
        p_txt2 = []
        result = []
        try:
            for i in tqdm(range(len(html_txt))):
                result.clear()
                soup_reque = requests.get(url_gushiwen + html_txt[i]).content
                soup = BeautifulSoup(soup_reque, 'lxml')
                title_h1 = soup.find_all('h1')
                for txt in title_h1:
                    title_txt1.append(txt.string)
                    # print("古诗标题：", txt.string)
                    soup_reque = requests.get(url_gushiwen + html_txt[i]).content
                    text = BeautifulSoup(soup_reque, 'lxml')
                    text_txts = str(text.find(attrs={'class': 'contson'})).split('<br/>')
                    title_h2 = soup.find('h2')
                    for text_txt in text_txts:
                        a = re.sub('<div class="contson" id="contson.+\\">', '', str(text_txt))
                        b = re.sub('<p>', '', a)
                        c = re.sub('</p>', '', b)
                        d = re.sub('</div>', '', c)
                        e = re.sub('\\n', '', d)
                        p_txt1.append(e.encode('gbk', 'ignore').decode('gbk'))

                    if title_h2 == '<h2><span style="float:left;">译文及注释</span></h2>':
                        title_txt2.append(title_h2.string)
                        translation = str(soup.find(name='div', attrs={'class': 'contyishang'})).split('<br/>')
                        data = '展开阅读全文'
                        data_txts = re.findall(data, str(translation))
                        if data_txts == []:
                            for translation_txt in translation:
                                translation_txts1 = re.sub('<div class="contyishang">', '', str(translation_txt))
                                translation_txts2 = re.sub('<div style="height:30px; font-weight:bold; font-size:16px; margin-bottom:10px; clear:both;">', '', translation_txts1)
                                translation_txts3 = re.sub('<h2><span style="float:left;">译文及注释</span></h2>', '', translation_txts2)
                                translation_txts4 = re.sub('<span id="fanyiPlay.+\\" style=" display:none;width:1px; height:1px; float:left;"></span>', '', translation_txts3)
                                translation_txts5 = re.sub('<img alt="" height="16" id="speakerimgFanyi.+" src="https://song.gushiwen.cn/siteimg/speak-er.png" width="16"/></a>', '', translation_txts4)
                                translation_txts6 = re.sub('<div class="contyishang" style="padding-bottom:10px;">', '', translation_txts5)
                                translation_txts7 = re.sub('<a href="javascript:PlayFanyi(.+,.+)" style="float:left; margin-top:7px; margin-left:5px;">', '', translation_txts6)
                                translation_txts8 = re.sub('<div style="text-align:center; margin-top:-5px;">', '', translation_txts7)
                                translation_txts9 = re.sub('<p>', '', translation_txts8)
                                translation_txts10 = re.sub('<strong>', '', translation_txts9)
                                translation_txts11 = re.sub('</strong>', '', translation_txts10)
                                translation_txts12 = re.sub('</p>', '', translation_txts11)
                                translation_txts13 = re.sub('</div>', '', translation_txts12)
                                translation_txts14 = re.sub('\\n', '', translation_txts13)
                                translation_txts15 = re.sub('<a href="https://so.gushiwen.cn/authorv_.+.aspx" target="_blank">', '', translation_txts14)
                                translation_txts16 = re.sub('</a>', '', translation_txts15)
                                p_txt2.append(translation_txts16.encode('gbk', 'ignore').decode('gbk'))

                        else:
                            a = re.findall('<a href="javascript:fanyiShow(.+,.+)" style="text-decoration:none;">', str(translation))
                            b = re.compile('(\\w+)')
                            c = b.findall(str(a))
                            reg = 'https://so.gushiwen.cn/nocdn/ajaxfanyi.aspx?id=%s' % c[1]
                            soup_reg = requests.get(reg).content
                            text_1 = BeautifulSoup(soup_reg, 'lxml')
                            translation_txts17 = str(text_1.find('p')).split('<br/>')
                            for translation_txt in translation_txts17:
                                translation_txts18 = re.sub('<p><strong>', '', translation_txt)
                                translation_txts19 = re.sub('</strong>', '', translation_txts18)
                                translation_txts20 = re.sub('</p>', '', translation_txts19)
                                translation_txts21 = re.sub('<a href="https://so.gushiwen.cn/authorv_.+.aspx" target="_blank">', '', translation_txts20)
                                translation_txts22 = re.sub('</a>', '', translation_txts21)
                                if translation_txts22 == '<p>未登录':
                                    continue
                                p_txt2.append(translation_txts22.encode('gbk', 'ignore').decode('gbk'))

                    lst_title1 = ''.join(title_txt1)
                    lst_text = ''.join(p_txt1)
                    lst_title2 = ''.join(title_txt2)
                    lst_translation = ''.join(p_txt2)
                    item = {'title':lst_title1,
                     'text':lst_text,
                     'translation and notes':lst_title2,
                     'translation':lst_translation}
                    result.append(item)
                    with open(json_path + '\\%s' % gushiwen_list[2] + '\\%s.json' % txt.string, 'a') as (dump_file):
                        title_txt1.clear()
                        p_txt1.clear()
                        title_txt2.clear()
                        p_txt2.clear()
                        dump_file.write(json.dumps(result, ensure_ascii=False))
            pass
        except Exception as e:
            print('古诗爬取出现问题了，请复制这条报错给开发人员：', e)
            print('请输入任意键退出程序！！！')
            if ord(msvcrt.getche()) == [0, 100]:
                sys.exit()


    def main(self):
        try:
            P1 = Process(target=self.tangshi, args=(path,))
            P2 = Process(target=self.songci, args=(path,))
            P3 = Process(target=self.gushi, args=(path,))
            P1.start()
            P2.start()
            P3.start()
            P1.join()
            P2.join()
            P3.join()
            print(time.time())
            print('程序执行结束！！！\n')
            print('当前程序为指定网站爬虫，并且json可能有点问题，如需要爬取其他网站或优化输出的json文件，请联系开发人员进行优化代码。但不一定理你哦！\n')
            print('请输入任意键退出程序！！！')
            if ord(msvcrt.getche()) == [0, 100]:
                sys.exit()
        except Exception as e:
            print("整个程序都出BUG了，把这段报错复制给开发哦!!",e)
            print('请输入任意键退出程序！！！')
            if ord(msvcrt.getche()) == [0, 100]:
                sys.exit()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    path = input('请输入需要存放json文件的文件夹路径（C:\\User\\Desktop）：')
    print('程序开始执行！！！\n')
    print('过程有点漫长，请耐心等候！！\n')
    for gushiwen in gushiwen_list:
        isExists = os.path.exists(path + '\\%s' % gushiwen)
        if isExists == True:
            shutil.rmtree(path + '\\%s' % gushiwen)
            os.mkdir(path + '\\%s' % gushiwen)
        else:
            os.mkdir(path + '\\%s' % gushiwen)
    multi = multi_process()
    multi.main()


