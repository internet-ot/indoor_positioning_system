from flask import Flask
from flask import request

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from math import sqrt,log10

import time

app = Flask(__name__)

engine = create_engine('sqlite:///rssi.db')
base = declarative_base()
#Session = sessionmaker(bind=engine)
Session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))



class AccessPoint(base):
    __tablename__ = "accesspoint"
    id = Column(Integer, primary_key=True)
    mac_address = Column(String)

class Location(base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

class Sample(base):
    __tablename__ = "sample"
    ap_id = Column(Integer, ForeignKey("accesspoint.id"))
    source_address = Column(String, nullable=False, primary_key=True)
    timestamp = Column(Float, nullable=False, primary_key=True)
    rssi = Column(Float, nullable=False)
    ap = relationship("AccessPoint", backref="sample")

    def values(self, src, t, _rssi, _ap):
        source_address = src
        timestamp = t
        rssi = _rssi
        ap = _ap

class FingerprintValue(base):
    __tablename__ = "fingerprint_value"
    id = Column(Integer, primary_key=True)
    loc_id = Column(Integer, ForeignKey("location.id"))
    ap_id = Column(Integer, ForeignKey("accesspoint.id"))
    rssi = Column(Float, nullable=False)
    location = relationship("Location", backref="fingerprint_value")
    ap = relationship("AccessPoint", backref="fingerprint_value")

class CalibratingMobile(base):
    __tablename__ = "calibrating_mobile"
    mac_address = Column(String, primary_key=True)
    loc_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location", backref="calibrating_mobile")

@app.route("/rssi", methods=['GET', 'POST'])
def rssi():
    if request.method == 'GET':
        base_data = request.args.to_dict()
        missing = Session.query(AccessPoint).filter_by(mac_address=base_data['ap']).first()
        if missing is None:
            accessPoint = AccessPoint(mac_address = base_data['ap'])
            Session.add(accessPoint)
            Session.commit()
            print(base_data['ap'])
        
        for key in base_data:
            if key != 'ap':
                ap1 = Session.query(AccessPoint).filter_by(mac_address=base_data['ap']).first()
                Sample_data = Sample(ap_id = ap1.id, source_address = key,timestamp = time.time(),rssi = base_data[key],ap = ap1)
                Session.add(Sample_data)
                Session.commit()
                
        calibrating_data = Session.query(CalibratingMobile).filter(CalibratingMobile.mac_address == ap1.mac_address).all()
        for c_data in calibrating_data:
            loc = c_data.location
            all_samples = Session.query(Sample).filter(Sample.source_address == ap1.mac_address).filter(Sample.timestamp >= (time.time() - 1)).all()
            all_samples = Session.query(Sample).filter(Sample.source_address == ap1.mac_address).all()
            print(ap1.mac_address)
            if (all_samples is not None):
                for sample in all_samples:
                    fingerprint_value = FingerprintValue(loc_id=loc.id, ap_id=sample.ap.id, rssi=sample.rssi, location=loc, ap=sample.ap)
                    Session.add(fingerprint_value)
                    Session.commit() 
    return "Updated the DataBase"



@app.route("/start_calibration", methods=['GET', 'POST'])
def start_calibration():
    if request.method == 'GET':
        base_data = request.args.to_dict()
        missing = Session.query(Location).filter_by(x=base_data['x'],y=base_data['y'],z=base_data['z']).first()
        print(missing)
        if missing is None:
            print("Location is in missing so addding in location table")
            loc = Location(x = base_data['x'],y = base_data['y'], z = base_data['z'])
            Session.add(loc)
            Session.commit()
        
        loc2 =  Session.query(Location).filter_by(x=base_data['x'],y=base_data['y'],z=base_data['z']).first()   
        missing = Session.query(CalibratingMobile).filter_by(mac_address = base_data['mac_addr']).first()
        if missing is None:
            print("Mac address is missing so addding in Calibrating mobile table")
            calibrate_data = CalibratingMobile(mac_address = base_data['mac_addr'],loc_id = loc2.id,location = loc2)
            Session.add(calibrate_data)
            Session.commit()
        
        All_samples = Session.query(Sample).filter_by(source_address = base_data['mac_addr']).all()
        for samp in All_samples:
            diff = time.time() - samp.timestamp
            if diff < 1:
                print("Sample is less older so adding it to the FingerPrint Value Table")
                try:
                    ap2= Session.query(AccessPoint).filter_by(mac_address = base_data['mac_addr']).first()
                    finger_val = FingerprintValue(loc_id = loc2.id,ap_id = ap2.id ,rssi= samp.rssi,location= loc2,ap= ap2 )
                    Session.add(finger_val)
                    Session.commit()
                except:
                    print("Access_point is not saved in Databasse")
    return "The calibration has succesfully Done"

@app.route("/stop_calibration", methods=['GET', 'POST'])
def stop_calibration():
    if request.method == 'GET':
        base_data = request.args.to_dict()
        all_mac = Session.query(CalibratingMobile).filter_by(mac_address = base_data['mac_addr']).all()
        for mac in all_mac:
            print(mac)
            Session.delete(mac)
            Session.commit()
    return "Calibration is succefully Stopped"
        
def rssi_dist(arr1, arr2):
    avg1 = rssi_average(arr1)
    avg2 = rssi_average(arr2)
    return sqrt(pow(avg1-avg2,2))

def rssi_average(arr):
    rssi_mw_total = 0
    for x in arr:
        rssi_mw_total += 10 ** (x / 10.0)
    return 10 * log10(rssi_mw_total / len(arr))

@app.route("/locate", methods=['GET', 'POST'])
def locate():
    rssi_arr_samp = []
    loc_ids = []
    for value in Session.query(FingerprintValue.loc_id).distinct():
        loc_ids.append(value.loc_id)
    print(loc_ids)
    if request.method == 'GET':
        base_data = request.args.to_dict()
        All_samples = Session.query(Sample).filter_by(source_address = base_data['mac_addr']).all()
        for samp in All_samples:
            diff = time.time() - samp.timestamp
            if diff < 1:
                rssi_arr_samp.append(samp.rssi)
    min_rssi = 9999999
    result_loc = -1
    for id in loc_ids:
        tmp = []
        for value in Session.query(FingerprintValue).filter_by(loc_id = id).all():
            tmp.append(value.rssi)
        print(tmp)
        dist = rssi_dist(rssi_arr_samp,tmp)
        if dist<min_rssi:
            min_rssi = dist
            result_loc = id
    if result_loc == -1:
        return "unavailable"
    xyz = Session.query(Location).filter_by(id = result_loc).first()
    print(rssi_arr_samp)
    result = "Location Calculated is :  x:{} y:{} z:{}".format(xyz.x,xyz.y,xyz.z)
    return result



if __name__ == '__main__':
    app.run(debug=True)