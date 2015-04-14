import os.path
import subprocess
import sys
import time

import pywinauto
from pywinauto.controls import GetDialogPropsFromHandle
# from pywinauto import timings


def print_edit_and_button_ctl(hwnd):
    if hwnd.__class__.__name__ == 'EditWrapper':
        print("[%s][EditWrapper]=>%s(IsVisible=%s)" % (hwnd, hwnd.Texts(), hwnd.IsVisible()))
    elif hwnd.__class__.__name__ == 'ButtonWrapper':
        print("[%s][ButtonWrapper]=>%s(IsVisible=%s)" % (hwnd, hwnd.Texts(), hwnd.IsVisible()))
    elif hwnd.__class__.__name__ == 'HwndWrapper':
        if hwnd.ControlCount() != 0:
            for hwnd_child in hwnd.Children():
                print_edit_and_button_ctl(hwnd_child)


def main():
    print "start RunRun:%s" % os.path.realpath(os.path.curdir)
    print "start RunRun:%s" % os.getcwd()

    # params = [r"C:\Program Files (x86)\FileZilla FTP Client\filezilla.exe"]
    # print subprocess.list2cmdline(params)

    # p = subprocess.Popen("runBin.bat", cwd=r"C:\Users\xchen\Desktop")
    # stdout, stderr = p.communicate()
    # print sys.getsizeof('\e')
    # print sys.getsizeof(r'\e')
    # print sys.getsizeof(u'\e')

    pwa_app = pywinauto.application.Application()
    application_path = r"C:\Program Files (x86)\GCTI\Workspace Desktop Edition\InteractionWorkspace.exe"
    window_title_text = u'.*Workspace.*'
    # w_handles = pywinauto.findwindows.find_windows(title=window_title_text)
    # print w_handles
    # for w_handle in w_handles:
    #     try:
    #         dlg_window = pwa_app.window_(handle=w_handle)
    #         dlg_window.Close()
    #         dlg_window.WaitNot("exists")
    #     except pywinauto.timings.TimeoutError:
    #         pass
    #
    # w_handles = pywinauto.findwindows.find_windows(title=window_title_text)
    # print w_handles
    # for w_handle in w_handles:
    #     try:
    #         dlg_window = pwa_app.window_(handle=w_handle)
    #         dlg_window['&Yes'].Click()
    #         dlg_window.WaitNot("exists")
    #     except pywinauto.controls.HwndWrapper.InvalidWindowHandle:
    #         pass

    pwa_app.start_(application_path)
    while len(pywinauto.findwindows.find_windows(title_re=window_title_text)) == 0:
        print("...WDE Application Starting...")
        time.sleep(3)
    # pwa_app.connect_(path=application_path)
    # w_handles = pwa_app.windows_()
    # for w_handle in w_handles:
    #     dlg_window = pwa_app.window_(handle=w_handle)
    #     dlg_window.PrintControlIdentifiers()
    # pwa_app.Workspace.Wait("exists enabled visible ready")
    # dlg_window = pwa_app.top_window_()
    # dlg_window.PrintControlIdentifiers()
    # pwa_app[u'Workspace - Log In'].PrintControlIdentifiers()

    for w_handle in pywinauto.findwindows.find_windows(title_re=window_title_text):
        dlg_window = pwa_app.window_(handle=w_handle)
        dlg_window.PrintControlIdentifiers()
    # w_handle = pywinauto.findwindows.find_windows(title=window_title_text)[0]
    # dlg_window = pwa_app.window_(handle=w_handle)
    # for i in ['2','3','4','5','6','7','8','9','13','14','15','16','17','DirectUIHWND2','WorkerW2','ReBar2','Toolbar4']:
    #     print_edit_and_button_ctl(dlg_window[i])
        # print("%s=>%s" % (i, dlg_window[i].ControlCount()))
        # print("%s=>%s" % (i, dlg_window[i].Children()))
        # if dlg_window[i].ControlCount() != 0:
        #     for ctl in dlg_window[i].Children():
                # if ctl.__class__.__name__ == 'EditWrapper' and ctl.IsVisible():
                #     ctl.SetText("lalalla")
                #     print("[SET]%s=>%s" % (i, ctl.WindowText()))
                # if ctl.__class__.__name__ == 'StaticWrapper':
                #     print("[%s][StaticWrapper]=>%s" % (i, ctl.Texts()))
                # if ctl.__class__.__name__ == 'EditWrapper':
                #     print("[%s][EditWrapper]=>%s(IsVisible=%s)" % (i, ctl.Texts(), ctl.IsVisible()))

                # if ctl.__class__.__name__ == 'TreeViewWrapper':
                #     print("[%s][TreeViewWrapper]=>%s" % (i, ctl.ItemCount()))
                # dlg_window['&Next'].Click()
                # pwa_app.InteractionWorkspace.PrintControlIdentifiers()
                #
                # print dlg_window['Edit'].WindowText()
                # dlg_window['Edit'].SetText("E:\sdkjlasdkfa")
                # pwa_app.InteractionWorkspaceDeploymentManager.PrintControlIdentifiers()
                # w_handle = pywinauto.findwindows.find_windows(title=window_title_text)[0]
                # dlg_window = pwa_app.window_(handle=w_handle)
                # pwa_app.InteractionWorkspaceDeploymentManager.PrintControlIdentifiers()
                # dlg_window['&YesButton'].Click()


if __name__ == "__main__":
    # main()
    ccid = None
    if ccid is None or "".strip():
        print "True"
    else:
        print "False"

    # pwa_app = pywinauto.application.Application()
    # pwa_app.start(r"C:\Windows\system32\calc.exe")
    # window = pywinauto.timings.WaitUntilPasses(10, 0.5, lambda: pwa_app.window_(title=u'Calculator'))
    # pwa_app.Calculator.PrintControlIdentifiers()
    # w_handle = pywinauto.findwindows.find_windows(title=u'Calculator', class_name='CalcFrame')[0]
    # window = pwa_app.window_(handle=w_handle)
    # ctrl = window['Button15']
    # ctrl.Click()
    # ctrl = window['Button20']
    # ctrl.Click()
    # ctrl = window['Button16']
    # ctrl.Click()
    # ctrl = window['Button28']
    # ctrl.Click()
    # print window['Static4'].WindowText()