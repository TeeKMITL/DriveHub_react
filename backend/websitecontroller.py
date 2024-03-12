from user import User,Customer,Lender
from car import Car
from car_detail import Car_detail
from DMY import DMY
from datetime import date,timedelta
from uuid import uuid4
from reservation import Reservation
rand_token = uuid4()

class Token:
    def __init__(self,user,token):
        self.__User: User = user
        self.__token: str = token

    @property
    def token(self):
        return self.__token
    
    @property
    def user(self):
        return self.__User
    
class WebsiteController:
    def __init__(self):
        # self.User_list = []
        # self.Brand_list = []
        # self.Car_list = []
        # self.Reservation_list = []
        # self.Car_reserved_date_list = []
        # self.Review_list = []
        # self.Payment_list = []
        # self.Waiting_for_approval_car_lost = []

        self.__user_list = []
        self.__customer_list = []
        self.__lender_list = []
        self.__reservation_list = []
        self.__car_list = []
        self.__token_list = []

    @property
    def user_list(self):
        return self.__user_list
    @property
    def customer_list(self):
        return self.__customer_list
    @property
    def lender_list(self):
        return self.__lender_list
    @property
    def reservation_list(self):
        return self.__reservation_list
    @property
    def car_list(self):
        return self.__car_list
    
    @property
    def token_list(self):   
        return self.__token_list
    
    # def check_token(self,token):
    #     for tokens in self.token_list:
    #         if tokens.token == token:
    #             return tokens.user.role

    def register(self, email, Name, Phone_Number, Password, Role):

        for user in self.user_list:
            if user.email == email:
                return "User already exists"
            
        token = uuid4()
        # user = User(email, Name, Phone_Number, Password, Role,token)
        if (Role == "customer"):

            customer = Customer(email, Name, Phone_Number, Password)
            user = User(email, Name, Phone_Number, Password)
            user.role = "customer"
            token_data = Token(user,token)
            self.customer_list.append(customer)
            self.token_list.append(token_data)
            self.user_list.append(user)

        elif (Role == "lender"):

            lender = Lender(email, Name, Phone_Number, Password)
            user = User(email, Name, Phone_Number, Password)
            user.role = "lender"

            token_data = Token(user,token)
            self.token_list.append(token_data)
            self.lender_list.append(lender)
            self.user_list.append(user)

        else:
            return "Invalid Role"
        
        return "Registration Successful"
        
        pass
    def login(self, email, password):
        for user in self.user_list:
            if user.email == email and user.password == password:
                return user
            elif user.email == email and user.password != password:
                return "Incorrect Password"
        return "Email not found"

    def find_user_with_token(self,token) -> User:
        for tokens in self.token_list:
            if str(tokens.token) == str(token):
                return tokens.user
        
    
    def find_user_with_email(self,email):

        for token in self.__token_list:
            if token.user.email == email:
                return token
        return None
    
    def find_lender(self,email):
        for lender in self.lender_list:
            if lender.email == email:
                return lender
        return None
    
    def add_car(self,name, model, licensePlate, deliveryArea, price, carType, transmission, seats, seatType, fuelSystem, engineCapacity, doors, token):

        user = self.find_user_with_token(str(token))

        if user is None:
            return "Token not found"
        elif user.role != "lender":
            return "User is not a lender"
        
        temp = self.find_lender(user.email)
        data_car = Car_detail( name, model, price,carType,seats, fuelSystem, doors, transmission, seatType, engineCapacity)
        car = Car("AVAILABLE",data_car,licensePlate,user.name,deliveryArea,price)

        temp.lend_car(car)
        self.car_list.append(car)
        return "Car Added Successfully"
        


        pass

    def remove_car(self):
        pass

    def approve_car(self):
        pass

    def add_history(self):
        pass

    def update_car_status(self):
        pass

    def pay_lender(self):
        pass

    def add_brand(self):
        pass

    def pay_back_deposit(self):
        pass

    def check_available_car(self, location, start_date, end_date):
        unavailable = False
        available_car = []
        temp = start_date.split("/")
        start = DMY(int(temp[0]),int(temp[1]),int(temp[2]))
        temp = end_date.split("/")
        end = DMY(int(temp[0]),int(temp[1]),int(temp[2]))
        for car in self.car_list:
            if car.location == location:
                if car.status == "AVAILABLE":
                    for date in car.unavailable_dates:
                        if date.year == start.year and date.month == start.month:
                            if date.day >= start.day and date.day <= end.day:
                                unavailable = True
                                break
                    if not unavailable:
                        available_car.append(car)
        return available_car
            

    def get_payment(self):
        pass

    def view_reservation(self):
        pass

    def init_car_list(self):
        owner = self.find_user_with_email("tee@a")
        lender = self.find_lender("tee@a")


        car = Car_detail("Toyota","Camry", 100,"Sedan",4,"Petrol",4,"Automatic","Leather",2000)
        car_detail2 = Car_detail("Honda", "Accord", 120, "Sedan", 4, "Petrol", 4, "Automatic", "Cloth", 1800)
        car_detail3 = Car_detail("Nissan", "Altima", 110, "Sedan", 4, "Petrol", 4, "Automatic", "Cloth", 2000)
        car1 = Car("AVAILABLE",car,"ABC123",owner.user.name,"ECC",100)
        car2 = Car("AVAILABLE", car_detail2, "DEF456", owner.user.name, "ECC", 150)
        car3 = Car("AVAILABLE", car_detail3, "GHI789", owner.user.name, "ECC", 120)
        car3.reserve_date(5,3,2024)

        self.car_list.append(car1)
        lender.lend_car(car1)
        self.car_list.append(car2)
        lender.lend_car(car2)
        self.car_list.append(car3)
        lender.lend_car(car3)

    def find_car_with_license(self,license):
        for cars in self.car_list:
            if license == cars.license:
                return cars
    
    def add_reservation(self,token,license,start_date,end_date,location):

        user = self.find_user_with_token(token)
        for customers in self.customer_list:
            if user.name == customers.name:
                customer = customers
                break

        car = self.find_car_with_license(license)
        temp = start_date.split("/")
        date1 = date(int(float(temp[2])),int(temp[1]),int(temp[0]))
        temp = end_date.split("/")
        date2 = date(int(float(temp[2])),int(temp[1]),int(temp[0]))
        delta = date2-date1
        for i in range(delta.days + 1):
            a = date1 + timedelta(days=i)
            b = str(a)
            splitted = b.split("-")
            r_date = DMY(int(splitted[2]),int(splitted[1]),int(splitted[0]))
            car.unavailable_dates.append(r_date)
        reserve = Reservation(customer,car.license,car.price,start_date,end_date,location)
        self.reservation_list.append(reserve)
        customer.add_reservation(reserve)
        return reserve
        
