#python3.x
#v0.1.0

import requests,urllib.parse,json,sys,time,os
a=os.path.exists('音乐')
b=os.getcwd()
if a==False:
    os.mkdir(b+'//音乐')
else:
    pass




def zhuti():
    url='http://music.lizhanqi.xyz'

    song=input('请输入您想听的歌曲，我来帮您下载：\n')
    if song!='':
        fs=input('请选择下载渠道\n1，酷狗音乐\t2，网易云音乐\t3，QQ音乐\n4，酷我音乐\t5，虾米音乐\t6，百度音乐\n7，一听音乐\t8，咪咕音乐\t9,荔枝音乐\n10,蜻蜓音乐\t11,喜马拉雅\t12，全民k歌\n13,5sing原创\t14,5sing翻唱 \n输入下载渠道的序号就可以，想在酷狗端口下载就输入“1”就可以，依次类推\n请输入下载序号:')
        try:
            
            api={1:'kugou',2:'netease',3:'qq',
            4:'kuwo',5:'xiami',6:'baidu',
            7:'1ting',8:'migu',9:'lizhi',
            10:'qingting',11:'ximalaya',12:'kg'
                 ,13:'5singyc',14:'5singfc'}



            referer=url+"?name="+urllib.parse.quote(song)+"&type="+api[int(fs)]



            print('正在接收数据中……\n过程可能会有点慢，请耐心等待勿关闭程序')


            headers={
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Cookie":"UM_distinctid=17c817bb40a1ce-09e4d77e59fc2c-513c1e45-149c48-17c817bb40b530; CNZZDATA1273782431=678524499-1634253232-https%253A%252F%252Fwww.baidu.com%252F%7C1634253232",
                "Referer":"http://music.lizhanqi.xyz/?name=%E5%BE%AE%E5%BE%AE&type=kugou",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47"
                ,"X-Requested-With":"XMLHttpRequest"
                }
            data={
                "input":"微微",
                "filter":"name",
                "type":"kugou",
                "page":"1"
                }

            headers['Referer']=referer
            data['input']=song
            data['type']=api[eval(fs)]
        
            

            req=requests.post(url,headers=headers,data=data)

            print('正在为您解析数据中……\n请勿关闭程序')

            text=json.loads(req.text)

            yyxq={}

            for i in range(0,len(text['data'])-1):
                xq=[]
                xq.append(text['data'][i]['title'])
                xq.append(text['data'][i]['author'])
                xq.append(text['data'][i]['url'])
                yyxq[i]=xq
                if len(text['data'][i]['title'])>len(song): 
                        print('序号为'+str(i)+'\t'*2+text['data'][i]['title']+" "*(30-len(text['data'][i]['title']))+text['data'][i]['author'])
                else:
                        print('序号为'+str(i)+'\t'*2+text['data'][i]['title']+" "*30+text['data'][i]['author'])

            if yyxq=={}:
                print('\n\n\n很抱歉，我们在接口为'+fs+'的渠道中没有找到'+song+'这首歌。\n\n\n')
                print('\n\n\n程序将在2秒后自动退出！！！\n\n如需继续下载，请重启本程序，谢谢使用！')
                time.sleep(2)
                sys.exit()


            xzxh=input('请选择您要下载哪一首歌，直接输入序号就行\n如需下载多个请用逗号分割即可，例如1,2(切记要用英文逗号分开，否则后果自负！！)\n如果不需要下载多个，请直接输入序号就行：')

            xh=xzxh.split(',')

            if xzxh=='':
                print('\n\n\n您未做出选择！程序将在2秒后自动退出！！！')
                time.sleep(2)
                sys.exit()
            def xzsong(mp3url,i):
                print('正在下载'+yyxq[i][-2]+'唱的'+yyxq[i][0]+'请稍后……')

                #下载MP3文件
                req=requests.get(mp3url)
                fo=open('音乐//'+yyxq[i][0]+'-'+yyxq[i][-2]+'.mp3','wb')
                fo.write(req.content)
                fo.close()

                print(yyxq[i][-2]+'唱的'+yyxq[i][0]+'下载完成啦！')
                print("\n\n已保存至当前目录的音乐文件夹下")

            for i in xh:
                i=eval(i)
                xzsong(yyxq[i][-1],i)
            
        except:
            print("您没有正确的填写序号")
        
    else:
        print("您没有输入需要下载的歌曲的名字")


zhuti()


print('谢谢您对本程序的使用，祝您生活愉快！')

