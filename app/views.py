# encoding:utf8
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, send_from_directory, url_for, redirect, flash
from app import app
from app.models import *
import re
import time

UPLOAD_FOLDER = 'd:/ex2/'

@app.route("/",methods=['GET','POST'])
def index():
    cql = ''
    if request.method=='POST':
        flist = request.files.getlist("file[]")
        temp = ''
        tlist = []
        for f in flist:
            upload_path = UPLOAD_FOLDER
            file_name = upload_path + f.filename.encode().decode('utf-8')
            f.save(file_name)
            csvunion(file_name)
            temp = file_name.split('.',1)[0].split("_",1)[1].strip()
            tlist.append(temp)
            cqlrun(file_name,temp)
        cql = cqlgen(tlist)
        flash(cql , 'success')
        return redirect(url_for('index'))
    return render_template('index.html', cql = cql, active=1)
