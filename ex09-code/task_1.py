class CarWash(object):
    def __init__(self):
        self.persistence = {}
        self.sms_sender = SmsSender()

    def register_car_for_wash(self, car, customer):
        job = CarWashJob(car, customer)
        self.persistence[job.job_id] = job
        return job.job_id

    def complete_wash(self, job_id):
        job = self.persistence[job_id]
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


if __name__ == '__main__':
    car_wash = CarWash()
    car1 = Car('ZH 123456')
    car2 = Car('AG 654321')
    customer1 = Customer('Foo', '079 xxx xxxx')
    customer2 = Customer('Bar', '078 xxx xxxx')

    job_id1 = car_wash.register_car_for_wash(car1, customer1)
    job_id2 = car_wash.register_car_for_wash(car2, customer2)
    assert job_id1 != job_id2

    car_wash.complete_wash(job_id1)

