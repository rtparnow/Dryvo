import datetime as dt

from sqlalchemy.orm import backref

from server.api.database import db
from server.api.database.mixins import (
    Column,
    Model,
    SurrogatePK,
    reference_col,
    relationship,
)


class Payment(SurrogatePK, Model):
    """Payment from student to teacher"""

    __tablename__ = "payments"
    teacher_id = reference_col("teachers", nullable=False)
    teacher = relationship("Teacher", backref=backref("payments", lazy="dynamic"))
    student_id = reference_col("students", nullable=True)
    student = relationship("Student", backref=backref("payments", lazy="dynamic"))
    amount = Column(db.Integer, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "teacher": self.teacher.to_dict(),
            "student": self.student.to_dict(),
            "amount": self.amount,
        }