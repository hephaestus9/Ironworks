# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, session
from ironworks.noneditable import *
from ironworks.modules import *
from ironworks import serverTools

app = serverTools.getApp()


@app.route('/feeds')
def feeds():
    if 'username' in session:
        return render_template('feeds.html')
    return 'You are not logged in'