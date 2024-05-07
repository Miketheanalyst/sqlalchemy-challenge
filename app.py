



# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

app = Flask(__name__)

# Create an engine to the SQLite database
engine = create_engine('sqlite:///hawaii.sqlite')

# Define routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    last_date = datetime.strptime(most_recent_date, '%Y-%m-%d')
    start_date = last_date - timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).all()
    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    return jsonify(stations)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

app = Flask(__name__)
engine = create_engine('sqlite:///hawaii.sqlite')

@app.route("/api/v1.0/tobs")
def temperature_observations():
    session = Session(engine)
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    last_date = datetime.strptime(most_recent_date, '%Y-%m-%d')
    start_date = last_date - timedelta(days=365)

    # Most active station from previous queries
    most_active_station_id = 'USC00519281'  # Example station ID

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= start_date).\
        order_by(Measurement.date).all()
    session.close()

    temperatures = {date: tobs for date, tobs in results}
    return jsonify(temperatures)

@app.route("/api/v1.0/<start>", defaults={'end': None})
@app.route("/api/v1.0/<start>/<end>")
def stats(start, end):
    session = Session(engine)
    if end:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    session.close()

    temps = list(np.ravel(results))
    return jsonify({
        "TMIN": temps[0],
        "TAVG": temps[1],
        "TMAX": temps[2]
    })

if __name__ == '__main__':
    app.run(debug=True)




#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
