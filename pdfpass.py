import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import os
import pikepdf
import threading

def openFromFolder():
  global entFrom
  fld = fd.askdirectory()
  entFrom.delete(0, tk.END)
  entFrom.insert(tk.END, fld)

def openToFolder():
  global entTo
  fld = fd.askdirectory()
  entTo.delete(0, tk.END)
  entTo.insert(tk.END, fld)

def setPassword():
  th = threading.Thread(target=setPasswordThread)
  th.start()

def setPasswordThread():
  global entFrom, entTo, entPass, pb
  fromDir = entFrom.get()
  toDir = entTo.get()
  password = entPass.get()
  if fromDir == '':
    mb.showerror('エラー', '元フォルダを指定してしません')
    return
  if not os.path.isdir(fromDir):
    mb.showerror('エラー', '元フォルダが存在しません')
    return
  if toDir == '':
    mb.showerror('エラー', '保存先フォルダを指定してしません')
    return
  if password == '':
    mb.showerror('エラー', 'パスワードを指定してしません')
    return
  if not os.path.isdir(toDir):
    try:
      os.mkdir(toDir)
    except FileNotFoundError:
      mb.showerror('エラー', '保存先フォルダの作成に失敗しました')
      return
  files = os.listdir(fromDir)
  l = len(files)
  i = 0
  for file in files:
    base, ext = os.path.splitext(file)
    ext = ext.lower()
    if ext == '.pdf':
      fromFile = os.path.join(fromDir, file)
      toFile = os.path.join(toDir, file)
      print(fromFile, toFile)
      pdf = pikepdf.open(fromFile)
      pdf.save(toFile, encryption = pikepdf.Encryption(user=password))
    i += 1
    pb.configure(value = i / l)
    pb.update
  mb.showinfo('終了', 'パスワード一括設定が終了しました')
  pb.configure(value = 0)
  pb.update

root = tk.Tk()
root.title("PDFパスワード一括設定")
root.geometry("520x240")
lblFrom = tk.Label(text = '元フォルダ')
lblFrom.place(x = 20, y = 20)
lblTo = tk.Label(text = '保存先フォルダ')
lblTo.place(x = 20, y = 60)
entFrom = tk.Entry(width = 50)
entFrom.place(x = 110, y = 20)
entTo = tk.Entry(width = 50)
entTo.place(x = 110, y = 60)
refFrom = tk.Button(width = 10, text = "参照", command = openFromFolder)
refFrom.place(x = 420, y = 20)
refTo = tk.Button(width = 10, text = "参照", command = openToFolder)
refTo.place(x = 420, y = 60)
lblPass = tk.Label(text = 'パスワード')
lblPass.place(x = 20, y = 100)
entPass = tk.Entry(width = 25)
entPass.place(x = 110, y = 100)
pb = ttk.Progressbar(root, length = 480, mode = 'determinate', maximum = 1)
pb.place(x = 20, y = 140)
btnStart = tk.Button(text = "開始", width = 30, height = 2, command = setPassword)
btnStart.place(x = 150, y = 180)
root.mainloop()