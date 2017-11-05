import dramatiq
import os
import time

from contextlib import closing
from dramatiq.brokers.rabbitmq import URLRabbitmqBroker
from flask import Flask, redirect, render_template, request
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")
database = create_engine(database_url)
Model = declarative_base()
Session = sessionmaker(bind=database)

broker_url = os.getenv("CLOUDAMQP_URL", os.getenv("BROKER_URL"))
broker = URLRabbitmqBroker(broker_url)
dramatiq.set_broker(broker)


class Job(Model):
    __tablename__ = "jobs"

    TYPE_SLOW = "slow"
    TYPE_FAST = "fast"
    TYPES = (TYPE_SLOW, TYPE_FAST)

    STATUS_PENDING = "pending"
    STATUS_DONE = "done"
    STATUSES = (STATUS_PENDING, STATUS_DONE)

    id = Column(Integer, primary_key=True)
    type = Column(String(10), nullable=False)
    status = Column(String(10), default=STATUS_PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def process(self):
        if self.type == Job.TYPE_SLOW:
            time.sleep(30)
        elif self.type == Job.TYPE_FAST:
            time.sleep(1)
        else:
            raise ValueError("Unknown job type.")


@dramatiq.actor
def process_job(job_id):
    with closing(Session()) as session:
        job = session.query(Job).get(job_id)
        job.process()

        job.status = Job.STATUS_DONE
        session.add(job)
        session.commit()


@app.route("/jobs", methods=["POST"])
def add_job():
    with closing(Session()) as session:
        job = Job(type=request.form["type"])
        session.add(job)
        session.commit()
        process_job.send(job.id)
    return redirect("/")


@app.route("/")
def index():
    with closing(Session()) as session:
        jobs = session.query(Job).order_by(Job.created_at.desc()).all()
        return render_template("index.html", jobs=jobs)
