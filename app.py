# Import the dependencies
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import numpy as np  # Ensure numpy is imported for data processing

# Flask Setup
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")  
Base = automap_base()
Base.prepare(engine, reflect=True)

# References saved  to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Creates our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON list of precipitation data from the dataset."""
    results = session.query(Measurement.date, Measurement.prcp).all()
    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    results = session.query(Station.station).all()
    stations = [station[0] for station in results]
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.datetime.strptime(latest_date[0], "%Y-%m-%d")
    query_date = latest_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= query_date).\
        filter(Measurement.station == 'USC00519281').all()  #Most active station ID, (determined in climate_starter)

    temps = {date: tobs for date, tobs in results}
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    """Return JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range."""
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
    if end:
        query = query.filter(Measurement.date >= start, Measurement.date <= end)
    else:
        query = query.filter(Measurement.date >= start)
    results = query.all()
    temps = list


