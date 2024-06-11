from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, FLOAT, BOOLEAN

Base = declarative_base()


class MeasurementSource(Base):
    __tablename__ = "measurementsource"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Add additional fields if there are any


class SensorItem(Base):
    __tablename__ = "sensoritem"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Add additional fields if there are any
    active = Column(Boolean, nullable=False)


class Attachment(Base):
    __tablename__ = "attachment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    description = Column(VARCHAR(500))
    type = Column(VARCHAR(50), nullable=False)
    content = Column(String, nullable=False)
    model_mapping_id = Column(Integer, ForeignKey("modelmapping.id"))


class ModelMapping(Base):
    __tablename__ = "modelmapping"
    id = Column(Integer, primary_key=True, autoincrement=True)
    measurement_source_id = Column(
        Integer, ForeignKey("measurementsource.id"), nullable=False
    )
    sensor_item_id = Column(Integer, ForeignKey("sensoritem.id"), nullable=False)
    model_id = Column(Integer, nullable=False)
    block_id = Column(Integer, ForeignKey("block.id"), nullable=False)

    measurement_source = relationship("MeasurementSource")
    sensor_item = relationship("SensorItem")
    block = relationship("Block")


class Property(Base):
    __tablename__ = "property"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    unit = Column(VARCHAR(100), nullable=False)


class Prediction(Base):
    __tablename__ = "prediction"
    insert_ts = Column(Integer, nullable=False)
    m_data = Column(Float, nullable=False)
    property_id = Column(Integer, ForeignKey("property.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("block.id"), nullable=False)

    property = relationship("Property")
    block = relationship("Block")


class Block(Base):
    __tablename__ = "block"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False)
    model_mappings = relationship("ModelMapping")
    predictions = relationship("Prediction")
