from tkinter import Frame,Tk
import ctypes
import multiprocessing
import bind as webview

enumWindows = ctypes.windll.user32.EnumWindows
enumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
getWindowText = ctypes.windll.user32.GetWindowTextW
getWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
isWindowVisible = ctypes.windll.user32.IsWindowVisible
SetParent=ctypes.windll.user32.SetParent
MoveWindow=ctypes.windll.user32.MoveWindow
GetWindowLong=ctypes.windll.user32.GetWindowLongA
SetWindowLong=ctypes.windll.user32.SetWindowLongA
def _getAllTitles():
    titles=[]
    def foreach_window(hWnd, lParam):
        if isWindowVisible(hWnd):
            length = getWindowTextLength(hWnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            getWindowText(hWnd, buff, length + 1)
            titles.append((hWnd, buff.value))
        return True
    enumWindows(enumWindowsProc(foreach_window),0)
    return titles
def getWindowsWithTitle(title):
    hWndsAndTitles = _getAllTitles()
    windowObjs = []
    for hWnd, winTitle in hWndsAndTitles:
        if title.upper() in winTitle.upper():
            windowObjs.append(hWnd)
    return windowObjs



class WebView2(Frame):
    #说明，若要使用这个组件，请将pywebview的__init__.py改为同目录内新的文件
    
    def __init__(self,parent,width:int,height:int,url:str='',**kw):
        Frame.__init__(self,parent,width=width,height=height,**kw)
        self.fid=self.winfo_id()
        self.width=width
        self.height=height
        self.title=str(self.fid)
        self.parent=parent
        if url=='':
            self.web=webview.create_window(self.title,width=width,height=height,frameless=True,text_select=True)
        else:
            self.web=webview.create_window(self.title,url,width=width,height=height,frameless=True,text_select=True)
        webview.start(func=self.in_frame)

    def in_frame(self):
        wid=getWindowsWithTitle(self.title)
        while wid==[]:
            wid=getWindowsWithTitle(self.title)
        wid=wid[0]
        SetParent(wid,self.fid)
        MoveWindow(wid,0,0,self.width,self.height,True)
        self.wid=wid
        self.__go_bind()

    def __go_bind(self):
        self.bind('<Destroy>',lambda event:self.web.destroy())
        self.bind('<Configure>',self.__resize_webview)
    def __resize_webview(self,event):
        MoveWindow(self.wid,0,0,self.winfo_width(),self.winfo_height(),True)

    def get_url(self):
        #返回当前url，若果没有则为空
        return self.web.get_current_url()

    def evaluate_js(self,script):
        #执行javascript代码，并返回最终结果
        return self.web.evaluate_js(script)

    def load_css(self,css):
        #加载css
        self.web.load_css(css)

    def load_html(self,content,base_uri=None):
        #加载HTML代码
        #content=HTML内容
        #base_uri=基本URL，默认为启动程序的目录
        if base_uri==None:
            self.web.load_html(content)
        else:
            self.web.load_html(content,base_uri)

    def load_url(self,url):
        #加载全新的URL
        self.web.load_url(url)

    def none(self):
        pass



def have_runtime():#检测是否含义webview2 runtime
    from webview.platforms.winforms import _is_chromium
    return _is_chromium()

def install_runtime():#安装webview2 runtime
    #https://go.microsoft.com/fwlink/p/?LinkId=2124703
    from urllib import request
    import subprocess
    import os
    url=r'https://go.microsoft.com/fwlink/p/?LinkId=2124703'
    unit=request.urlopen(url).read()
    with open('D:/webview2runtimesetup.exe',mode='wb') as uf:
        uf.write(unit)
    del uf
    cmd='D:/webview2runtimesetup.exe'
    p=subprocess.Popen(cmd,shell=True)
    return_code=p.wait()#等待子进程结束
    os.remove('D:/webview2runtimesetup.exe')
    return return_code

#print(install_runtime())
#范例
if __name__=='__main__':
    if not have_runtime():#没有webview2 runtime
        install_runtime()
    root=Tk()
    root.title('pywebview for tkinter test')
    root.geometry('1200x600+5+5')

    frame=WebView2(root,500,500)
    frame.pack(side='left')
    frame.load_html('<h1>hi hi</h1>')

    frame2=WebView2(root,500,500)
    frame2.pack(side='left',padx=20,fill='both',expand=True)
    frame2.load_url('https://smart-space.com.cn/')
    
    root.mainloop()

