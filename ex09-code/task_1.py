from abc import ABC, abstractmethod
import os


class CarWash(object):
    def __init__(self, persistence):
        self.persistence = persistence
        self.sms_sender = SmsSender()

    def register_car_for_wash(self, car, customer):
        job = self.persistence.save(CarWashJob(car, customer))
        return job.job_id

    def complete_wash(self, job_id):
        job = self.persistence.find_by_id(job_id)
        self.sms_sender.send(job.contact_details, job.notification_message)


class CarWashJob:
    job_counter = 0

    def __init__(self, car, customer, *job_id):
        self.car = car
        self.customer = customer
        if job_id:
            self.job_id = job_id
        else:
            self.job_id = self.new_job_id()

    @staticmethod
    def new_job_id():
        job_id = CarWashJob.job_counter
        CarWashJob.job_counter += 1
        return f'#{job_id}'

    @property
    def contact_details(self):
        return self.customer.mobile_phone

    @property
    def notification_message(self):
        return f'Job {self.job_id}, Car {self.car.plate}'


class Customer(object):
    def __init__(self, name, mobile_phone):
        self.name = name
        self.mobile_phone = mobile_phone


class Car(object):
    def __init__(self, plate):
        self.plate = plate


class SmsSender(object):
    def send(self, phone_number, msg):
        print(f'Sending text message to {phone_number}: {msg}')
        # ... do some weird SMS magic


class CarJobRepository(ABC):
    @abstractmethod
    def save(self, obj):
        pass

    @abstractmethod
    def find_by_id(self, obj):
        pass


class InMemoryCarJobRepository(CarJobRepository):
    persistence_dict = {}

    def save(self, obj):
        InMemoryCarJobRepository.persistence_dict[obj.job_id] = obj
        return obj

    def find_by_id(self, obj):
        job_id = InMemoryCarJobRepository.persistence_dict.get(obj)
        if not job_id:
            raise ValueError('No job with the given id is found!')
        else:
            return job_id


class FileCarJobRepository(CarJobRepository):

    def __init__(self, file_name, drop_on_startup=False):
        self.file_name = file_name
        if drop_on_startup:
            self.drop_db()

    def save(self, obj):
        pass

    def find_by_id(self, obj):
        pass

    def drop_db(self):
        if os.path.exists(self.file_name):
            print(f'dropping table {self.file_name}')
            os.remove(self.file_name)


if __name__ == '__main__':
    in_mem_db = InMemoryCarJobRepository()
    file_db = FileCarJobRepository('car-wash-db.tsv', drop_on_startup=True)

    in_memory_car_wash = CarWash(in_mem_db)
    file_db_car_wash = CarWash(file_db)

    car1 = Car('ZH 123456')
    car2 = Car('AG 654321')
    customer1 = Customer('Foo', '079 xxx xxxx')
    customer2 = Customer('Bar', '078 xxx xxxx')

    job_id1 = in_memory_car_wash.register_car_for_wash(car1, customer1)
    job_id2 = in_memory_car_wash.register_car_for_wash(car2, customer2)

    assert job_id1 != job_id2

    in_memory_car_wash.complete_wash(job_id1)
   # file_db_car_wash.complete_wash(job_id2)


