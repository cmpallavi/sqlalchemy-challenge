# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt
from datetime import datetime


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def homepage():
    """List all the available routes."""
    return (
        f"Available Routes for Hawaii Weather Data:<br/><br>"
        f" * Precipitation records for last 12 months: <a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation<a><br/>"
        f" * Weather Stations: <a href=\"/api/v1.0/stations\">/api/v1.0/stations<a><br/>"
        f" * Daily Temperature Observations for Most Active Station for Last Year: <a href=\"/api/v1.0/tobs\">/api/v1.0/tobs<a><br/>"
        f" * Min, Average & Max Temperatures for Date Range: /api/v1.0/<start><br>"
        f" * Min, Average & Max Temperatures for Date Range: /api/v1.0/<start>/<end><br>"
        f"Note: to access values between a start and end date enter both dates using format: YYYY-mm-dd/YYYY-mm-dd"
    )



#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date_dt = datetime.strptime(most_recent_date.date, '%Y-%m-%d').date()
    # Calculate the date one year from the last date in data set.

    year_ago = most_recent_date_dt - dt.timedelta(days=365)
    year_ago

    # Perform a query to retrieve the data and precipitation scores
    values = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).\
        order_by(Measurement.date).\
        all()

    data = []
    for date, prcp in values:
        data_dict = {}
        data_dict["date"] = date
        data_dict["prcp"] = prcp
        data.append(data_dict)
    session.close()
    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    active_stations = session.query(Station.station, Station.name).\
        all()
    stations = []
    for station, name in active_stations:
        data_dict = {}
        data_dict["station"] = station
        data_dict["name"] = name
  
        stations.append(data_dict)
   
    session.close()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():    
    session = Session(engine)
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
        order_by(func.count(Measurement.station).desc()).\
        group_by(Measurement.station).all()
    most_active_station = active_stations[0]
    most_active_station_id = most_active_station[0]
    
    most_recent_date = session.query(Measurement.date).\
        filter(Measurement.station == most_active_station_id).\
        order_by(Measurement.date.desc()).first()
    most_recent_date_dt = datetime.strptime(most_recent_date.date, '%Y-%m-%d').date()
    year_ago = most_recent_date_dt - dt.timedelta(days=365)
    year_ago
    
    values = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= year_ago).\
        all()
    data = []
    for date, tobs in values:
        data_dict = {}
        data_dict["date"] = date
        data_dict["tobs"] = tobs
        data.append(data_dict)
    session.close()
    return jsonify(data)


# @app.route("/api/v1.0/trip)
# def trip1(start_date, end_date='2017-08-23'):




if __name__ == '__main__':
    app.run(debug=True)

