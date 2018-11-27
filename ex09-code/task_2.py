from abc import ABC, abstractmethod


class Toy:
    def __init__(self, name):
        self.name = name
        self.is_assembled = False
        self.is_painted = False
        self.is_wrapped = False

    def is_complete(self):
        if self.is_assembled and self.is_painted and self.is_wrapped:
            return True
        else:
            return False


class AssemblyLine:
    def __init__(self, toys):
        self.__toys = toys

    def get_toys(self):
        return self.__toys

    def get_number_of_toys(self):
        return len(self.__toys)

    def take_toy(self):
        if self.__toys:
            first_toy = self.__toys[0]
            self.__toys.remove(self.__toys[0])  # remove toy
            return first_toy
        else:
            return None

    def put_toy_back(self, toy):
        self.__toys.append(toy)


class Elf(ABC):
    def __init__(self):
        self._toy_working_on = None

    @abstractmethod
    def do_job(self):
        pass

    def take_from(self, assembly_line):
        if self._toy_working_on is None:
            self._toy_working_on = assembly_line.take_toy()

    def put_back(self, assembly_line):
        assembly_line.put_toy_back(self._toy_working_on)
        self._toy_working_on = None


class AssemblerElf(Elf):
    def __init__(self):
        Elf.__init__(self)

    def do_job(self):
        self._toy_working_on.is_assembled = True


class PainterElf(Elf):
    def __init__(self):
        Elf.__init__(self)

    def do_job(self):
        self._toy_working_on.is_painted = True


class WrapperElf(Elf):
    def __init__(self):
        Elf.__init__(self)

    def do_job(self):
        if self._toy_working_on.is_painted and self._toy_working_on.is_painted:
            self._toy_working_on.is_wrapped = True


class Santa:

    def verify(self, assembly_line):
        for toy in assembly_line.get_toys():
            if not toy.is_complete():
                return False
        return True


if __name__ == '__main__':
    # Create three toys
    toy1 = Toy("Toy1")
    toy2 = Toy("Toy2")
    toy3 = Toy("Toy3")

    # Create an assembly line with three toys
    line = AssemblyLine([toy1, toy2, toy3])

    # Create three elves, one of each subclass
    assembler = AssemblerElf()
    painter = PainterElf()
    wrapper = WrapperElf()

    # Create a Santa :-)
    santa = Santa()

    # Let the elves work through the assembly line
    for elf in [assembler, wrapper, painter]:  # Wrong order: wrapping can't happen before painting!
        for i in range(line.get_number_of_toys()):
            elf.take_from(line)
            elf.do_job()
            elf.put_back(line)

    # The line cannot be verified because the toys are not wrapped
    assert not santa.verify(line)

    # Create three new toys...
    toy4 = Toy("Toy4")
    toy5 = Toy("Toy5")
    toy6 = Toy("Toy6")

    # ... and a new assembly line
    line2 = AssemblyLine([toy4, toy5, toy6])

    # This time, let the elves work through the assembly line in the right order
    for elf in [painter, assembler, wrapper]:  # Right order: wrap at the end!
        for i in range(line2.get_number_of_toys()):
            elf.take_from(line2)
            elf.do_job()
            elf.put_back(line2)

    # Now the line can be verified
    assert santa.verify(line2)
