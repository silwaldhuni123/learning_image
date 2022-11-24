from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Response, Request
from get_tags import get_tags
import json
import psycopg2
import logging
import config as cfg
from pydantic import BaseModel
import base64
logging.basicConfig(filename='app.log',level=logging.ERROR, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

def database_connection():
    try:
        con= psycopg2.connect(
        database=cfg.DATABASE,
        user=cfg.USER,
        password=cfg.PASSWORD,
        host=cfg.HOST,port=cfg.PORT)
        
        con.autocommit = True
        return con
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="communication with database failed "+str(e))

app = FastAPI()


@app.post('/image_tagging')
async def file_upload(
        my_file: UploadFile = File(...)
):
    con=database_connection()
    # if con==False:
    #     raise HTTPException(status_code=404, detail="communication with datbase failed")
    contets = await my_file.read()
    tags=get_tags(contets)
    cons=psycopg2.Binary(contets)
    file=','.join([tag['label']for tag in tags])
    with con.cursor() as cur:
        cur.execute('INSERT INTO imagetable (filebytes,tags) values (%s, %s);',(cons,file)) 
        cur.execute('SELECT * FROM imagetable')
        length = len(cur.fetchall())
    return length


@app.post('/upload_image')
async def file_upload(request : Request):
    data=await request.body()
    con=database_connection()

    tags=get_tags(data)
    cons=psycopg2.Binary(data)
    print(tags)
    file=','.join([tag['label']for tag in tags])
    with con.cursor() as cur:
        cur.execute('INSERT INTO imagetable (filebytes,tags) values (%s, %s);',(cons,file)) 
        cur.execute('SELECT * FROM imagetable')
        length = len(cur.fetchall())
        print(length)
        with open('image.jpg','wb') as file:
            file.write(data)
    return length


@app.get('/search_tags')
async def file_upload(search_tag):
    con=database_connection()
    print(search_tag)
    with con.cursor() as cur:
        cur.execute("SELECT * FROM imagetable WHERE tags LIKE '%{}%'".format(search_tag))
        asd={i[0]:base64.b64encode(i[1].tobytes()) for i in cur.fetchall()}
        return asd #Response(asd[0])


class image_response(BaseModel):
    image_list: list = []

@app.get('/all_images')
async def all_image():
    con=database_connection()
    with con.cursor() as cur:
        cur.execute('''SELECT * FROM "imagetable"''')
        asd={i[0]:base64.b64encode(i[1].tobytes()) for i in cur.fetchall()}
        return asd #Response(asd[0])