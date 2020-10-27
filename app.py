from flask import Flask,render_template,Request,request,send_file
import pandas as pd
import csv
from pymongo import MongoClient
import pymongo
import datetime
import json
from veritabani import * #.gitignore
app = Flask(__name__)



db = client.gettingStarted
mycollection = db["collectionname"]
people = db.people
veri1 = db.veri1

# personDocument = {
#   "name": { "first": "Alan", "last": "Turing" },
#   "birth": datetime.datetime(1912, 6, 23),
#   "death": datetime.datetime(1954, 6, 7),
#   "contribs": [ "Turing machine", "Turing test", "Turingery" ],
#   "views": 1250000
# }
# people.insert_one(personDocument)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route('/data',methods=['GET','POST'])
def data():
    if request.method == 'POST':
        f = request.form['csvfile']
        # csvler.insert_one(f)
        data = []
        sozluk_data = {}
        with open(f) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                data.append(row)
        with open(f,encoding='utf-8') as file2:
            csvReader = csv.DictReader(file2)
            for rows in csvReader:
  
                key = rows['csvno']
                sozluk_data[key] = rows
                veri1.insert_one(rows)
                
        data_frame = pd.DataFrame(data)
        print(type(sozluk_data))


        # data_json = json.dumps(data)
        # #data_json = data.json()
        # #veri1.insert_one(data)
        # veri1.insert(sozluk_data)
        return render_template("data.html", data = data_frame.to_html(header=False, index= False))
@app.route('/secim',methods=['GET','POST'])
def secim():
    return render_template("goruntule.html")
@app.route('/goruntule',methods=['GET','POST'])
def goruntule():
    
    # #print(people.find_one({ "name.last": "Turing" }))
    # #asddas = veri1({ "2.spor": "basketbol"})
    # print(veri1.find_one({ "2.spor": "basketbol"}))

    # scotts_posts = veri1.find_one({'1.spor': 'futbol'})
    # asdasd = people.find_one({ "name.last": "Turing" })
    # print(asdasd)
    # print("******************")
    # print(scotts_posts)
    # # for i in scotts_posts:
    # #     print(i)
    # a  = veri1.find_one({'1.spor' : 'futbol'})
    # b  = veri1.find_one({'1.telefon' : '54564'})
    # print(a)

    # print("*******b")
    
    
    # print(b)
    

    # csvno1_olanlar = veri1.find({"csvno":"1"})
    
    # print(csvno1_olanlar)

    # for i in csvno1_olanlar:
    #     print(i)
    

    #kullanici soyisim isterse


    # eposta = veri1.find({}, { "eposta":1 })
    # for i in eposta:
    #     if len(i) > 1:
    #         print(i)
        
    # csvno0_olanlar = veri1.find({"csvno":"2"})
    # print(csvno0_olanlar)
    # for i in csvno0_olanlar:
    #     print(i)    

    # sporlar = veri1.find({},{"spor":1})
    # for i in sporlar:
    #     if len(i)>1:
    #         print(i)
    tutulanlar= []
    key_son_list = []
    girdi = 0
    veriler = []

    if request.method == 'POST':
        csvno_girdi = request.form.get("csvno")
        bulunan_anahtarlar = []
        girdi = csvno_girdi
        print(csvno_girdi)

        alinacak_csv = veri1.find({"csvno":csvno_girdi})
        
        for i in alinacak_csv:
            tutulanlar.append(i)

        for i in tutulanlar:
            # print(" \n" ,i.keys())
            bulunan_anahtarlar.append(i.keys())
        for i in bulunan_anahtarlar:
            # print(list(i))
            key_son_list.append(list(i))
        k = 1
        for i in list(key_son_list):
            for j in range(999999): #simdilik
                try:
                    
                    veriler.append(i[k])
                    k = k+1

                    
                except:
                    print("An exception occurred")
                    break
            break            
        



        
    # print(tutulacak.items())
    # print(len(tutulacak))
    # for i in tutulanlar:
    #     print(i)
        
    return render_template("secim.html",content = veriler,content2 = girdi)


@app.route('/vericek', methods=['GET','POST'])
def vericek():
    if request.method == 'POST':
        cekilen_bilgiler = []
        verilers = request.form.getlist("checkbox_veriler")
        for i in verilers:
            if i !="csvno":
                geldi = veri1.find({},{i:1,"_id":0}) #veriler cekildi.

                for i in list(geldi):
                    if(len(i)>0):
                        # print(i)
                        cekilen_bilgiler.append(i)
        
        # for i in cekilen_bilgiler:
        #     print(i)
            
            

        # geldiler = []

        # for i in geldi:
        #     geldiler.append(i)
        # print(geldiler)
        yazacagim = []
        for i in list(cekilen_bilgiler):
                yazacagim.append(list(i.values()))
        # for i in range(len(yazacagim)):
        #     print(yazacagim[i])
        # with open('yeni.csv','w',newline='') as f:
        #     thewriter = csv.DictWriter(f,verilers)
        #     thewriter.writeheader()

        #  with open('yeni.csv', 'a') as csvfile:
        #      spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        #      spamwriter.writerow(yazacagim[i])
              

            #eger verilers[0] ile verilers[1] eşitse aynı türdür pass geç yazdırma. eşit değilse \n koy aşağı yazdırmaya başla.
        # for i in range(len(yazacagim)):
        #      for j in range(len(verilers)):
        #          with open('yeni.csv', 'a') as csvfile:
        #             if verilers[j-1] != verilers[j]:
        #                 print("verils1:",verilers[j-1])
        #                 print("verils2:",verilers[j])
        #                 spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        #                 spamwriter.writerow(yazacagim[i])
        #                 break
        #                 print("slas")

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




if __name__ == "__main__":
    app.run(debug=True)
    

