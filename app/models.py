from app.database import db


class Execution(db.Model):
    __tablename__ = 'executions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    commands = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'commands': self.commands,
            'result': self.result,
            'duration': float(self.duration)
        }
