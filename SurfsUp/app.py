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
        f" * Precipitation records for last 12 months: <a href=\"/api/v1/precipitation\">/api/v1/precipitation<a><br/>"
        f" * Weather Stations: <a href=\"/api/v1/stations\">/api/v1/stations<a><br/>"
        f" * Daily Temperature Observations for Most Active Station for Last Year: <a href=\"/api/v1/tobs\">/api/v1/tobs<a><br/>"
        f" * Min, Average & Max Temperatures for Date Range: /api/v1/trip/yyyy-mm-dd/yyyy-mm-dd<br>"
    )



#################################################
# Flask Routes
#################################################

@app.route("/api/v1/precipitation")
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

@app.route("/api/v1/stations")
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

@app.route("/api/v1/tobs")
def tobs():    
    session = Session(engine)

    session.close()

# @app.route("/api/v1/trip)
# def trip1(start_date, end_date='2017-08-23'):




if __name__ == '__main__':
    app.run(debug=True)

