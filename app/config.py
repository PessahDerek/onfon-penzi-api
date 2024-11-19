"""
Application configuration and settings.
"""
import os


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://apps:DevDerek1738@localhost:5432/penzi"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "fasjldkfjjkljcalkfkjajf823-101==940_@()*$@)@"
    JWT_SECRET_KEY = "FJALKJF8lk;ac;092o32jk;akccj8341-787r91klackajdrl34u-"
    JWT_TOKEN_LOCATION = ["headers"]
