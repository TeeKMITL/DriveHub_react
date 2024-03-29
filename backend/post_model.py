from pydantic import BaseModel
from typing import List, Optional

class RegisterModel(BaseModel):

    name: str
    phone_Number: str
    email: str
    role: str
    password: str
    

class LoginModel(BaseModel):
    email: str
    password: str

class UserModel(BaseModel):
    username: str
    password: str
    role: str


class TokenModel(BaseModel):
    token: str


class CarModel(BaseModel):
    name: str
    model: str
    licensePlate: str
    deliveryArea: str
    price: str
    carType: str
    transmission: str
    seat: str
    seatType: str
    fuelSystem: str
    engineCapacity: str
    door: str
    owner: str
    license: str

class FindCarModel(BaseModel):
    location: str
    pickupdate: str
    returndate: str

class ReservationConfirmation(BaseModel):
    token: str
    license: str
    location: str
    start_date: str
    end_date: str