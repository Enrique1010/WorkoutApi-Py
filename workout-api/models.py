import enum

from sqlalchemy import Integer, String, Enum, ForeignKey, Boolean, Float
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
        return (f"User(id={self.id}, name={self.name!r}, age={self.age!r}, username={self.username}, \
                email={self.email!r}, created_at={self.created_at!r})")


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
    exercises: Mapped[list["Exercise"]] = relationship(back_populates="workout", lazy="selectin")

    def __repr__(self):
        return (f"Workout(id={self.id}, user_id={self.user_id!r}, workout_type={self.workout_type!r},  \
                duration={self.duration!r}, calories={self.calories!r}, created_at={self.created_at!r},  \
                is_schedule={self.is_schedule}, schedule_date={self.schedule_date!r})")


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
        return (f"Exercise(id={self.id}, name={self.name!r}, exercise_type={self.exercise_type!r},  \
                duration={self.duration!r}, calories={self.calories!r}, created_at={self.created_at!r}, \
                workout_id={self.workout_id!r})")


class TrackingData(Base):
    """
    Tracking data model
    """
    __tablename__ = "tracking_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey("exercise.id"))
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    is_new_set: Mapped[bool] = mapped_column(Boolean, insert_default=True)
    is_new_record: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    distance_covered: Mapped[int] = mapped_column(Integer)  # if applicable
    created_at: Mapped[int] = mapped_column(Integer)
    last_updated_at: Mapped[int] = mapped_column(Integer)

    route: Mapped[list["MapPoint"]] = relationship(back_populates="tracking_data")  # if applicable

    def __repr__(self):
        return (f"TrackingData(id={self.id!r}, description={self.description!r}) exercise_id={self.exercise_id!r}, \
                is_new_set={self.is_new_set}, is_new_record={self.is_new_record}, duration={self.duration!r}, \
                 distance_covered={self.distance_covered}, created_at={self.created_at!r})")


class MapPoint(Base):
    """
    MapPoint model
    """
    __tablename__ = "map_point"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    created_at: Mapped[int] = mapped_column(Integer)
    last_updated_at: Mapped[int] = mapped_column(Integer)

    tracking_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("tracking_data.id"))
    tracking_data: Mapped["TrackingData"] = relationship(back_populates="route")

    def __repr__(self):
        return f"MapPoint(id={self.id!r}, lat={self.lat!r}, lon={self.lon!r}, created_at={self.created_at!r})"
