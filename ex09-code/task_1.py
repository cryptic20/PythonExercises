from abc import ABC, abstractmethod
import os
import csv


class CarWash(object):
    def __init__(self, persistence, notifier):
        self.persistence = persistence
        self.notifier = notifier

    def register_car_for_wash(self, car, customer):
        job = self.persistence.save(CarWashJob(car, customer))
        return job.job_id

    def complete_wash(self, job_id):
        job = self.persistence.find_by_id(job_id)
        self.notifier.send(job)


class CarWashJob:
    job_counter = 0

    def __init__(self, car, customer, job_id=None):
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
        return f'Job {self.job_id}, Car {self.car.plate} washed.'


class Customer(object):
    def __init__(self, name, mobile_phone):
        self.name = name
        self.mobile_phone = mobile_phone


class Car(object):
    def __init__(self, plate):
        self.plate = plate


class CarJobRepository(ABC):
    @abstractmethod
    def save(self, obj):
        pass

    @abstractmethod
    def find_by_id(self, obj):
        pass


class Notifier(ABC):
    @abstractmethod
    def send(self, msg):
        return f'Sending message...'


class SmsSender(Notifier):
    def send(self,  job):
        print(f'Sending sms to {job.customer.mobile_phone}, Message : Job {job.job_id}, Car {job.car.plate} washed.')


class CallSender(Notifier):
    def send(self, job):
        print(f'Calling {job.customer.mobile_phone}, Message: Job {job.job_id}, Car {job.car.plate} washed.')


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
        with open(self.file_name, 'a', ) as tsv_file:
            tsv_out = csv.writer(tsv_file, delimiter='\t')
            tsv_out.writerow([obj.job_id, obj.car.plate, obj.customer.name, obj.customer.mobile_phone])
        return obj

    def find_by_id(self, obj):
        with open('car-wash-db.tsv') as tsv_file:
            data = csv.reader(tsv_file, delimiter='\t')
            for row in data:
                if row:
                    if row[0] == obj:
                        return CarWashJob(Car(row[1]), Customer(row[2], row[3]), row[0])
                    else:
                        raise ValueError

    def drop_db(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)


if __name__ == '__main__':
    in_mem_db = InMemoryCarJobRepository()
    file_db = FileCarJobRepository('car-wash-db.tsv', drop_on_startup=True)

    sms_sender = SmsSender()
    call_sender = CallSender()

    in_memory_car_wash = CarWash(in_mem_db, sms_sender)
    file_db_car_wash = CarWash(file_db, call_sender)

    car1 = Car('ZH 123456')
    car2 = Car('AG 654321')
    customer1 = Customer('Foo', '079 xxx xxxx')
    customer2 = Customer('Bar', '078 xxx xxxx')

    job_id1 = in_memory_car_wash.register_car_for_wash(car1, customer1)
    job_id2 = in_memory_car_wash.register_car_for_wash(car2, customer2)
    job_id3 = file_db_car_wash.register_car_for_wash(car1, customer1)

    assert job_id1 != job_id2

    in_memory_car_wash.complete_wash(job_id1)
    file_db_car_wash.complete_wash(job_id3)



