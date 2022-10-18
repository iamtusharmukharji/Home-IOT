from datetime import datetime
import traceback
from .. import models
from sqlalchemy.exc import DBAPIError
from flask import render_template, url_for, redirect, request, abort
from . import cors, cross_origin, app


@app.route('/')
def index():
    return redirect(url_for('documentation'))

@app.route("/docs")
def documentation():
    print("hello")
    return render_template("docs.html")

@app.route("/switch/", methods = ["PUT"])
def switch_device(db=models.Session()):
    pin_check = {1,2,3,4,5,6,7,9,10,11,12,13,14,16,17,18,19,20,21,22}
    try:

        payload = request.json
        pin_id = payload["pin"]
        state =  payload['state']
        if pin_id not in pin_check:
            return {"detail":"invalid pin number/id"}
            
        db_pin = db.query(models.PinTable).filter(models.PinTable.pin == pin_id).all()

        if db_pin==[]:
            new_pin = models.PinTable(pin = pin_id,
                                      current_status = payload["state"],
                                      last_update = datetime.now()
                                      )
            db.add(new_pin)
            db.commit()
            db.refresh(new_pin)
            db.close()
            return {"message":f"pin {pin_id} changed to {state}"}, 201
        else:
            db_pin = db_pin[0]
            db_pin.current_status = payload["state"]
            db_pin.last_update = datetime.now()
            db.commit()
            db.close()

            return {"message":f"pin {pin_id} changed to {state}"}, 201

    except Exception as e:
        traceback.print_exc()
        err = str(e)
        return {"detail":err},403 

@app.route("/deletepin/",methods=["PUT"])
def delete_pin(db = models.Session()):
    try:
        pin_id = request.args.get("pin")
        pin_id = int(pin_id)

        db_pin = db.query(models.PinTable).filter(models.PinTable.pin == pin_id).all()

        if db_pin == []:
            return {"detail":f"{pin_id} not found"}, 404

        db.query(models.PinTable).filter(models.PinTable.pin == pin_id).delete()
        db.commit()

        return {"message":"pin deleted sucessfully"},200

    except Exception as e:
        traceback.print_exc()
        return {"detail":str(e)}, 403