from flask import Flask,render_template,Request,request,send_file
import pandas as pd
import csv
from pymongo import MongoClient
import pymongo
import datetime
import json
import random
from veritabani import * #.gitignore
app = Flask(__name__)



db = client.gettingStarted
mycollection = db["collectionname"]
people = db.people
veri1 = db.veri1


@app.route('/',methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route('/data',methods=['GET','POST'])
def data():

    uretilen_sayi = randomUret()
    
    if request.method == 'POST':
        f = request.form['csvfile']
        data = []
        sozluk_data = {}
        with open(f) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                data.append(row)

        with open(f,encoding='utf-8') as file2:
            csvReader = csv.DictReader(file2)
            for rows in csvReader:
  

                rows["csvno"] = uretilen_sayi
                veri1.insert_one(rows)
                
        data_frame = pd.DataFrame(data)


        return render_template("data.html", data = data_frame.to_html(header=False, index= False), uretilen = uretilen_sayi)
@app.route('/secim',methods=['GET','POST'])
def secim():
    return render_template("goruntule.html")
@app.route('/goruntule',methods=['GET','POST'])
def goruntule():
    
    
    tutulanlar= []
    key_son_list = []
    girdi = 0
    veriler = []

    if request.method == 'POST':
        csvno_girdi = request.form.get("csvno")
        bulunan_anahtarlar = []
        girdi = csvno_girdi

        alinacak_csv = veri1.find({"csvno":csvno_girdi})
        
        for i in alinacak_csv:
            tutulanlar.append(i)

        for i in tutulanlar:
            
            bulunan_anahtarlar.append(i.keys())
        for i in bulunan_anahtarlar:
            
            key_son_list.append(list(i))
        k = 1
        for i in list(key_son_list):
            for j in range(999999): 
                try:
                    
                    veriler.append(i[k])
                    k = k+1

                    
                except:
                    break
            break 
        



        
    
    return render_template("secim.html",content = veriler,content2 = girdi)


@app.route('/vericek', methods=['GET','POST'])
def vericek():
    if request.method == 'POST':
        cekilen_bilgiler = []
        verilers = request.form.getlist("checkbox_veriler")

        csvno_girdi = request.form.get("csvno")
        
        
        verilers2 = verilers.copy()
        
        
        verilers2.append("_id")
        
        deger = dict.fromkeys(verilers2,1)
        deger["_id"] = 0
        
        geldi = veri1.find({"csvno":csvno_girdi},deger) 
                

        for i in list(geldi):
            if(len(i)>0):
                        
                 cekilen_bilgiler.append(i)
        
        
            
            

       
        yazacagim = []
        for i in list(cekilen_bilgiler):
                yazacagim.append(list(i.values()))
        

        file = open('yeni.csv','w',newline='')
        with file:
            thewriter = csv.DictWriter(file,verilers)
            thewriter.writeheader()
            thewriter = csv.writer(file)
            thewriter.writerows(yazacagim)
        file.close()
                  

        

    return render_template("sonuc.html")



@app.route('/download')
def download_file():
    p = "yeni.csv"
    return send_file(p,as_attachment=True)


def randomUret():
    benzersiz = 0
    
    csvler = veri1.find({},{"csvno":1,"_id":0})
    cekilen_csvler = []
    for i in list(csvler):
        cekilen_csvler.append(i)

    yazilacak_csv = []
    for i in list(cekilen_csvler):
        yazilacak_csv.append(list(i.values()))
    for i in range(len(yazilacak_csv)):
        print(yazilacak_csv[i])
    sart = True
    if len(yazilacak_csv) == 0 :
        a = random.randint(1,999999)
        string_a = str(a)
        benzersiz = string_a
        pass
    else:
        while(sart):
            a = random.randint(1,999999)
            string_a = str(a)
            for i in range(len(yazilacak_csv)):
                if list(string_a) == yazilacak_csv[i]:
                    sart = True
                    break
                else:
                    sart = False
                    benzersiz = string_a

    return benzersiz

if __name__ == "__main__":
    app.run(debug=True)
    

