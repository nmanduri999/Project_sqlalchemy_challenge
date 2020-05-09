import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"/api/v1.0/date/start_date<br/>"
        f"/api/v1.0/date/start_date/end_date<br/>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipition"""
    # Query Measurement table for data and precipition
    results = session.query(Measurement.date , Measurement.prcp).all()

    session.close()

    # Create a dictionary using date as the key and prcp as the value.
    all_dates = []
    for date, prcp in results:
        precipition_dict = {}
        precipition_dict["date"] = date
        precipition_dict["prcp"] = prcp
        all_dates.append(precipition_dict)

    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(Station.station).group_by(Station.station).all()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(Measurement.tobs,Measurement.date).filter(Measurement.station == Station.station).\
                            filter(Measurement.date >="2016-08-24").\
                            filter(Measurement.date <="2017-08-23").all()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/date/<start_date>")
def start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    print(start_date)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()
    print(results)
    #results = list(np.ravel(results))
    print(results)
    given_start_date = []
    for min, avg, max in results:
        start_date_dict = {}
        start_date_dict["min"] = min
        start_date_dict["avg"] = avg
        start_date_dict["max"] = max
        given_start_date.append(start_date_dict)
    print(given_start_date)
    return jsonify(given_start_date)

@app.route("/api/v1.0/date/<start_date>/<end_date>")
def start_end_date(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    print(start_date)
    print(end_date)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    print(results)
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    given_start_end = []
    for min, avg, max in results:
        start_end_dict = {}
        start_end_dict["min"] = min
        start_end_dict["avg"] = avg
        start_end_dict["max"] = max
        given_start_end.append(start_end_dict)

    return jsonify(given_start_end)


if __name__ == '__main__':
    app.run(debug=True)
