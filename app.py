import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    precp= session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary
    all_precipitations = []
    for date,prcp in precp:
        prec_dict = {}
        prec_dict["date"] = date
        prec_dict["prcp"] = prcp
        all_precipitations.append(prec_dict)

    
    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all stations
    station_names= session.query(Station.station, Station.name).all()

    session.close()

    #List of stations
    all_stations = list(np.ravel(station_names))
 
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperatures():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all stations
    first_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the date and precipitation scores

    temperature = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= first_date).all()

    session.close()

    #List of stations
    all_temperatures = list(np.ravel(temperature))
 
    return jsonify(all_temperatures)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for summary information from a date
    start_summary = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(func.strtime("%y-%m-%d",Measurement.date) >= start).all()

    session.close()

    #List of stations
    st_summary = list(np.ravel(start_summary))
 
    return jsonify(st_summary)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for summary information from a date


    start_end_summary = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    #List of stations
    st_summary = list(np.ravel(start_end_summary))
 
    return jsonify(st_summary)    

    