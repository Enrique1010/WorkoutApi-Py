import enum

from sqlalchemy import Integer, String, Enum, LargeBinary, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ExerciseType(str, enum.Enum):
    """
    Exercise type enum
    """
    CARDIO = "cardio"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"
    BALANCE = "balance"


class User(Base):
    """
    User model
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[bytes] = mapped_column(String(255), nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"User(name={self.name!r}, age={self.age!r}) email={self.email!r}) created_at={self.created_at!r})"


class Workout(Base):
    """
    Workout model
    """
    __tablename__ = "workout"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    workout_type: Mapped[ExerciseType] = mapped_column(Enum(ExerciseType), insert_default=ExerciseType.CARDIO)
    duration: Mapped[int] = mapped_column(Integer)
    calories: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[int] = mapped_column(Integer)
    is_schedule: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    schedule_date: Mapped[int] = mapped_column(Integer)
    exercises: Mapped[list["Exercise"]] = relationship(back_populates="workout")

    def __repr__(self):
        return f"Workout(user_id={self.user_id!r}, workout_type={self.workout_type!r}) duration={self.duration!r}) calories={self.calories!r}) created_at={self.created_at!r})"


class Exercise(Base):
    """
    Exercise model
    """
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    exercise_type: Mapped[str] = mapped_column(String)
    duration: Mapped[int] = mapped_column(Integer)
    calories: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[int] = mapped_column(Integer)

    workout_id: Mapped[int] = mapped_column(Integer, ForeignKey("workout.id"))
    workout: Mapped["Workout"] = relationship(back_populates="exercises")

    def __repr__(self):
        return f"Exercise(name={self.name!r}, exercise_type={self.exercise_type!r}) duration={self.duration!r}) calories={self.calories!r}) created_at={self.created_at!r})"
