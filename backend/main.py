from fastapi import FastAPI, Request , HTTPException,Header,Response,File, UploadFile, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from fastapi import Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import date,timedelta
import shutil
import os
import uvicorn
from car_detail import Car_detail
from websitecontroller import WebsiteController
from reservation import Reservation
from fastapi.staticfiles import StaticFiles

from post_model import *

app = FastAPI()
UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)
templates = Jinja2Templates(directory="Frontend")

site = WebsiteController()

site.register("oat@a","oat","0967459032","1234","customer")
site.register("tee@a","tee","0967459032","1234","lender")

# app.mount("/static", StaticFiles(directory="static"), name="static")
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
    return {"filename": file.filename}

@app.get('/')
def index(request: Request):
    return RedirectResponse(url="/docs")

# @app.get("/get_role")
# async def get_role(request:Request,token:TokenModel):
#     token_input = token.token
#     return {site.check_token(str(token_input))}
#     try :
#         if temp == "customer":
#             return "customer"
#         elif temp == "lender":
#             return "lender"
#     except:
#         raise HTTPException(status_code=401, detail="Unauthorized")

@app.post('/home')
async def home(request : Request,token:TokenModel):
    token_input = token.token
    temp = site.check_token(str(token_input))
    try :
        if temp.role == "customer":
            return templates.TemplateResponse("customer_home.html", {"request": request, "token": token_input})
            # return RedirectResponse(url=f"/customer/home")
        elif temp.role == "lender":
            return templates.TemplateResponse("lender_home.html", {"request": request, "token": token_input})
            # return RedirectResponse(url=f"/lender/home")
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post('/login')
# async def login(email: str, password: str):
async def login(login_data: LoginModel):
    email: str = login_data.email
    password: str = login_data.password
    log = site.login(email, password)
    if log == "Incorrect Password":
        raise HTTPException(status_code=201, detail="Incorrect Password")
    elif log == "Email not found":
        raise HTTPException(status_code=202, detail="Email not found")
    return {"status": "Login Successful","name": site.find_user_with_email(email).user.name,"token": site.find_user_with_email(email).token, "role": site.find_user_with_email(email).user.role}

@app.post('/register')
async def register(register_data: RegisterModel):
    email: str = register_data.email
    name: str = register_data.name
    phone_Number: str = register_data.phone_Number
    password: str = register_data.password
    role: str = register_data.role

    log = site.register(email, name, phone_Number, password, role)
    if log == "Registration Successful":
        return {"status": "Registration Successful","token": site.find_user_with_email(email).token}
        
    elif log == "User already exists":
        raise HTTPException(status_code=401, detail="User already exists")
    
    elif log == "Invalid Role":
        raise HTTPException(status_code=402, detail="Invalid Role")
    
    return {"status": "Registration Successful"}

@app.get("/api/customer", tags=["API"])
def get_all_customer():
    return {"Customers": {index: str(obj) for index, obj in enumerate(site.customer_list)}}

@app.get("/api/lender", tags=["API"])
def get_all_lender():
    return {"Lenders": {index: str(obj) for index, obj in enumerate(site.lender_list)}}

@app.post("/reservations", tags=["Customer"])
def get_all_reservations_page(customer_id:int) -> dict:
    for customers in site.customer_list:
        if customers.id == customer_id:
            temp = customers.reservations
            return {"Reservations": {index: str(obj) for index, obj in enumerate(temp)}}
    return {"Error":"Error"}
##
@app.get("/api/car", tags = ["API"])
def get_all_car():
    return {"Cars": {index: {"Car License": obj.license, "Price": obj.price, "Status" : obj.status} for index, obj in enumerate(site.car_list)}}
@app.get("/api/carunavail", tags = ["API"])
def carunavail():
    return {"Cars": {index: {"Date": obj.unavailable_dates, "License": obj.license} for index, obj in enumerate(site.car_list)}}

@app.get("/find_car")

async def find_car_post():
    temp = site.check_available_car("ECC","3/3/2024","7/3/2024")
    return {"Available Car(s)" : {index: {"Car License": obj.license, "Price": obj.price} for index, obj in enumerate(temp)}}

@app.get("/search/car/{license}")
async def get_car_details(license: str):
    for cars in site.car_list:
        if cars.license == license:
            detail = cars.car_detail
            return {"car_detail": [
                {
                    "name":detail.name,
                    "model":detail.model,
                    "seats":detail.seats,
                    "fuel_system":detail.fuelSystem,
                    "doors":detail.doors,
                    "transmission":detail.transmission,
                    "seat_type":detail.seatType,
                    "engine_capacity":detail.engineCapacity,
                    "price":detail.price,
                    "owner": cars.owner
                }
            ]}

    raise HTTPException(status_code=404, detail="Car not found")

@app.post("/make_reservation")
async def make_reservation(data: ReservationConfirmation):
    token = data.token
    license = data.license
    location = data.location
    start_date = data.start_date
    end_date = data.end_date
    site.add_reservation(token,license,start_date,end_date,location)
    return {"message": "Reservation confirmed successfully"}
# test = Reservation("hi","hi","hi","hi","hi","hi")
# site.reservation_list.append(test)

@app.get("/get_all_reservations")
def get_all_reservations():
    return {"Reservations" : {index: {"License":obj.car,"Location" : obj.location,"Start Date":obj.start_date,"End Date":obj.end_date} for index, obj in enumerate(site.reservation_list)}}
##
@app.post("/search_car", tags=["Customer"])
async def search_car(find_car_data: FindCarModel):
    location: str = find_car_data.location
    pickupdate: str = find_car_data.pickupdate
    returndate: str = find_car_data.returndate

    temp = site.check_available_car(location,pickupdate,returndate)
    return {"car": [
            {
                "Name": car.car_detail.name,
                "Model": car.car_detail.model,
                "price": car.price,
                "license" : car.license
            }
            for car in temp
        ]}
    
@app.post("/lender/my_car", tags=["Lender"])
async def my_car_post(tokens: TokenModel):
    token: str = tokens.token
    role = site.find_user_with_token(str(token))
    if role is None:
        raise HTTPException(status_code=402, detail="Token not found")

    if role.role == "lender":
        lender_temp = site.find_lender(role.email)
        return {"car": [
            {
                "Name": car.car_detail.name,
                "Model": car.car_detail.model,
                "Status": car.status
            }
            for car in lender_temp.lent_cars
        ]}
    return {"Error": "You are not a lender"}

# @app.post("/make_reservation")
# async def make_reservation_post(request: Request, customer_id:int = Form(...), license:str = Form(...), amount:int=Form(...),start_date:date = Form(...), end_date:date = Form(...)):
#     for customers in site.customer_list:
#         if customers.id == customer_id:
#             for cars in site.car_list:
#                 if cars.license == license:
#                     start = str(start_date).split("-")
#                     end = str(end_date).split("-")
#                     new_start = f"{start[2]}/{start[1]}/{start[0]}"
#                     new_end = f"{end[2]}/{end[1]}/{end[0]}"
#                     site.add_reservation(customers,cars,amount,new_start,new_end)
#                     return {"Successful Reservation":{"From" : new_start, "To": new_end}}

@app.get("/lender/car", tags =["API"])
def get_all_car():
    return {"Cars": {index: str(obj) for index, obj in enumerate(site.car_list)}}

@app.post("/lender/add_car", tags = ["Lender"])
async def add_car(car_data: CarModel,token:TokenModel):
    name: str = car_data.name
    model: str = car_data.model
    licensePlate: str = car_data.licensePlate
    deliveryArea: str = car_data.deliveryArea
    price: int = car_data.price
    carType: str = car_data.carType
    transmission: str = car_data.transmission
    seat: int = car_data.seat
    seatType: str = car_data.seatType
    fuelSystem: str = car_data.fuelSystem
    engineCapacity: int = car_data.engineCapacity
    door: int = car_data.door

    temp = site.add_car(name, model, licensePlate, deliveryArea, price, carType, transmission, seat, seatType, fuelSystem, engineCapacity, door,token.token)
    if temp == "You are not a lender":
        raise HTTPException(status_code=401, detail="You are not a lender")
    elif temp == "Token not found":
        raise HTTPException(status_code=402, detail="Token not found")
    return {"status": "Car Added Successfully"}




@app.get("/lender/{lender_id}/car_list", tags=["Lender"])
def car_list(lender_id:int) -> dict:
    for lenders in site.lender_list:
        if lenders.id == lender_id:
            temp = lenders.lent_cars
            return {"Lent Cars": {index: {"license": obj.license, "status": obj.status, "price":obj.price, "location":obj.location} for index, obj in enumerate(temp)}}
    return {"Error"}

@app.post("/get_car_unavailable_dates", tags = ["Lender"])
async def get_car_unavailable_dates_post(request: Request,lender_id:int = Form(...), license: str = Form(...)):
    for cars in site.car_list:
        if cars.license == license:
            if cars.owner.id == lender_id:
                return {"Car Unavailable Dates" : {index: {"DAY" : obj.day, "MONTH": obj.month, "YEAR": obj.year} for index, obj in enumerate(cars.unavailable_dates)}}
    return {"Error"}

# @app.post("/add_car", tags =["API"])
# async def add_car_post(request: Request, lender_id: int = Form(...),license:str=Form(...), location: str = Form(...), price: int = Form(...)):
#     for lenders in site.lender_list:
#         if lenders.id == lender_id:
#             temp = lenders.lend_car("AVAILABLE",license,location,price)
#             site.car_list.append(temp)
#             return {"Successful"}
#     return {"Not Successful"}

@app.post("/update_car", tags =["API"])
async def update_car_post(request: Request, lender_id: int = Form(...), new_status: int = Form(...), license: str = Form(...)):
    if lender_id is None:
        return {"error": "Lender ID not provided"}
    if new_status != 1 and new_status != 0:
        return {"Not Successful"}
    for Lenders in site.lender_list:
        if(Lenders.id == lender_id):
            for Cars in Lenders.lent_cars:
                if (Cars.license == license):
                    Lenders.update_car_status(new_status,Cars)
                    return {"Car Status Changed to":Cars.status}
    return{"Not Successful"}

@app.get("/user", tags=["API"])
async def get_all_user():
    data = []
    for user in site.user_list:
        data.append({"email": user.email, "Name": user.name, "Phone_Number": user.phone_number, "Password": user.password, "Contact_info": user.contact_info, "Role": user.role , "Token": site.find_user_with_email(user.email).token})
    return data

@app.post("/get_user_token", tags=["API"])
async def get_user(request: Request, token:TokenModel):
    token_input:str = token.token
    temp = site.find_user_with_token(str(token_input))
    if temp is None:
        raise HTTPException(status_code=402,detail="token not found")
    return {"name":temp.name ,"plone_number":temp.phone_number,"role": temp.role}

@app.post("/Car_list/init", tags=["API"])
async def init_car_list(request: Request):
    site.init_car_list()
    return {"status":"Car list initialized"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host    = "127.0.0.1",
        port    = 8000, 
        reload  = True
    )