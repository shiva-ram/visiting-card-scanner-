from django.shortcuts import render
import requests
import sys
import sqlite3 as lite
from subprocess import run,PIPE
from django.core.files.storage import FileSystemStorage





def button(request):
    return render (request,'home.html')



def external(request):
    image=request.FILES['image']
    print("image is ",image)
    fs=FileSystemStorage()
    filename=fs.save(image.name,image)
    fileurl=fs.open(filename)
    templateurl=fs.url(filename)
    print("file raw url",filename)
    print("file full url", fileurl)
    print("template url",templateurl)
    # out= run([sys.executable,'C://Projects//final//final.py',inp],shell=False,stdout=PIPE)
    image= run([sys.executable,'C://Projects//final//final2.py',str(fileurl),str(filename)],shell=False,stdout=PIPE)

    print(image.stdout)
    # return render(request,'home.html',{'data':out.stdout})
    return render(request,'home.html',{'raw_url':templateurl,'edit_url':image.stdout})


def output(request):
    con = lite.connect('python.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM SqliteDb_developers")
        rows = cur.fetchall()

        for row in rows:
            print (row)
        
    return render(request,'home.html',{'data':row})