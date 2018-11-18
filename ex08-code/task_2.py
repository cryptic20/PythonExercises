class UniPerson:
    def __init__(self, name):
        self._name = name
        self.__inbox = []

    def receive_email(self, text):
        self.__inbox.append(text)

    def read_emails(self):
        emails = self.__inbox.copy()
        self.__inbox.clear()
        return emails

    def __str__(self):
        return f'Name: {self._name}'


class Student(UniPerson):
    student_dict = {}
    student_number = -1

    def __init__(self, name, start_year, has_graduated, ects):
        UniPerson.__init__(self, name)
        if start_year in Student.student_dict:
            Student.student_dict[start_year] += 1
        else:
            Student.student_dict[start_year] = Student.student_number+1
        self.start_year = start_year
        self.has_graduated = has_graduated
        self.__ects = ects
        self.__legi_nr = f'{start_year}-{str(Student.student_dict[start_year]).zfill(5)}'

    def __str__(self):
        summary = f'{UniPerson.__str__(self)}\nStart Year: {self.__legi_nr}\nGraduated: {self.has_graduated}' \
                  f'\nNo. of ECTS: {self.__ects}'
        return summary


class Lecturer(UniPerson):
    def __init__(self, name, lecture_name):
        UniPerson.__init__(self, name)
        self.__lecture_name = lecture_name

    def __str__(self):
        summary = f'{UniPerson.__str__(self)}\nLecture: {self.__lecture_name}'
        return summary


class UniManagement:
    def __init__(self):
        self.__persons = []

    def add_person(self, person):
        self.__persons.append(person)

    def list_persons(self,):
        return [person.__str__(self) for person in self.__persons]

    def send_email(self, text):
        for person in self.__persons:
            person.receive_email(text)

    def count_alumni(self):
        count = 0
        for person in self.__persons:
            if hasattr(person, 'has_graduated'):
                if getattr(person, 'has_graduated'):
                    count += 1
        return count


if __name__ == '__main__':
    p1 = UniPerson("Hans Muster")
    assert p1.__str__() == "Name: Hans Muster"

    p1.receive_email("Email 1")
    p1.receive_email("Email 2")
    assert p1.read_emails() == ["Email 1", "Email 2"]
    assert p1.read_emails() == []  # Because inbox was emptied after reading the first time

    s1 = Student("Student 1", 2017, False, 40)
    assert "Student 1" in s1.__str__()
    assert "2017-00000" in s1.__str__()
    assert "False" in s1.__str__()
    assert "40" in s1.__str__()

    s2 = Student("Student 2", 2017, True, 120)
    assert "Student 2" in s2.__str__()
    assert "2017-00001" in s2.__str__()
    assert "True" in s2.__str__()
    assert "120" in s2.__str__()

    s3 = Student("Student 3", 2016, True, 180)
    assert "Student 3" in s3.__str__()
    assert "2016-00000" in s3.__str__()
    assert "True" in s3.__str__()
    assert "180" in s3.__str__()

    mgmt = UniManagement()

    lecturer = Lecturer("Prof. Dr. Harald Gall", "Informatik 1")

    mgmt.add_person(s1)
    mgmt.add_person(s2)
    mgmt.add_person(s3)
    mgmt.add_person(lecturer)

    assert mgmt.count_alumni() == 2

    mgmt.send_email("This test email is sent to all university persons.")
    assert s1.read_emails() == ["This test email is sent to all university persons."]
    assert s2.read_emails() == ["This test email is sent to all university persons."]
    assert s3.read_emails() == ["This test email is sent to all university persons."]
    assert lecturer.read_emails() == ["This test email is sent to all university persons."]
