import requests,urllib.parse,json,sys,time,os

##检测当前目录下是否存在“音乐”文件夹
a=os.path.exists('音乐')
b=os.getcwd()
if a==False:
    os.mkdir(b+'//音乐')
else:
    pass



def zhuti():
    song=input('请输入您想听的歌曲，我来帮您下载：\n')
    if song!='':
##        try:
        fs=eval(input('请选择下载渠道\n1，酷狗音乐\t2，网易云音乐\t3，QQ音乐\t4，酷我音乐\t\n输入下载渠道的序号就可以，想在酷狗端口下载就输入“1”就可以，依次类推\n请输入下载序号:'))
        api={1:'kugou',2:'netease',3:'qq',4:'kuwo'}

        if fs in api.keys():
            if fs==1:
                song_name,singer_name,song_url=kugou(song)
                if song_name=='':
                    print('\n\n\n——很抱歉，我们在接口为'+fs+'的渠道中没有找到'+song+'这首歌。\n\n\n')
                    sys.exit()
            if fs==2:
                song_name,singer_name,song_url=netease(song)
                if song_name=='':
                    print('\n\n\n——很抱歉，我们在接口为'+fs+'的渠道中没有找到'+song+'这首歌。\n\n\n')
                    sys.exit()
            if fs==3:
                song_name,singer_name,song_url=qq(song)
                if song_name=='':
                    print('\n\n\n——很抱歉，我们在接口为'+fs+'的渠道中没有找到'+song+'这首歌。\n\n\n')
                    sys.exit()
            if fs==4:
                song_name,singer_name,song_url=kuwo(song)
                if song_name=='':
                    print('\n\n\n——很抱歉，我们在接口为'+fs+'的渠道中没有找到'+song+'这首歌。\n\n\n')
                    sys.exit()
        else:
            print("您输入的接口有误！")
        xiazai(song_name,singer_name,song_url)
        sys.exit()


def kugou(song):
    from get_music import kugou
    print('正在接收数据中……\n过程可能会有点慢，请耐心等待勿关闭程序')
    return kugou.kugou(song)
def netease(song):
    from get_music import netease
    print('正在接收数据中……\n过程可能会有点慢，请耐心等待勿关闭程序')
    return netease.netease(song)
def qq(song):
    from get_music import qq
    print('正在接收数据中……\n过程可能会有点慢，请耐心等待勿关闭程序')
    return qq.qq(song)
def kuwo(song):
    from get_music import kuwo
    print('正在接收数据中……\n过程可能会有点慢，请耐心等待勿关闭程序')
    return kuwo.kuwo(song)

def xiazai(name,singer,song_url):
    for i in range(0,len(name)-1):
        print("序号{}\t\t{}————{}".format(i+1,name[i],singer[i]))
    songs=input('请选择您要下载哪一首歌，直接输入序号就行\n如需下载多个请用逗号分割即可，例如1,2\n如果不需要下载多个，请直接输入序号就行：')
    if songs=='':
        print('\n\n\n——您未做出选择！程序将在2秒后自动退出！！！')
        time.sleep(2)
        sys.exit()
    song_list=songs.split(",")
    for i in song_list:
        i=int(i)
        rep=requests.get(song_url[i])
        with open("./音乐/"+name[i-1]+"-"+singer[i-1]+'.mp3','wb') as f:
            f.write(rep.content)
            print("\n\n"+singer[i-1]+'唱的'+name[i-1]+'下载完成啦！')
            print("\n\n已保存至当前目录的音乐文件夹下")
    print('\n≧∀≦\n感谢您对本程序的使用，祝您生活愉快！')


