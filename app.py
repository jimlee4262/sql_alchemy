import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import requests
import json
import base64
import datetime as dt
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#table names
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#gets date
maxd = session.query(func.max(Measurement.date)).scalar()
#Beginning Date for 12 months of data
query_date = dt.date(2017, 8, 23) - relativedelta(months=12)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation/ <br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt; <br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt"
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    precipitation_data = {}

    for row in precipitation:
        precipitation_data[row[0]] = row[1]

    return jsonify(precipitation_data)


    session.close()

@app.route("/api/v1.0/stations")
def station_names():

    session = Session (bind = engine)

    """Return a list of all passenger names"""
    # Query all station
    station = session.query(Station.station, Station.name).group_by(Station.station).all()

    station_data = {}

    for row in station:
        station_data[row[0]] = row[1]

    return jsonify(station_data)


    session.close()    


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session (bind = engine)

    """Return a list of all passenger names"""
    # Query top station
    topstation = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).\
                filter_by(station = "USC00519281").all()

    return jsonify(topstation)


    session.close()  

@app.route('/api/v1.0/<start>')
def start_temp(start):

    session = Session (bind = engine)

    """Return min, max, avg for temp between start and end"""
    # Query top station
    start_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    return jsonify(start_temps)


    session.close()  

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start,end):

    session = Session (bind = engine)

    """Return min, max, avg for temp between start and end"""
    # Query top station
    start_end_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).all()

    return jsonify(start_end_temps)


    session.close()  


if __name__ == '__main__':
    app.run(debug=True)
