from datetime import datetime
import traceback
from .. import models
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import load_only
from flask import render_template, url_for, redirect, request, abort
from . import cors, cross_origin, app

@app.route("/fetchstatus/")
def fetch_pin_status(db=models.Session()):
    try:
        db_pin = db.query(models.PinTable.pin,models.PinTable.current_status).all()
        if db_pin==[]:
            return [],404
        
        db_pin = [list(i) for i in db_pin]
        db.close()
        return {"data":db_pin},200

    except Exception as e:
        traceback.print_exc()
        err = str(e)
        return {"detail":err}, 403