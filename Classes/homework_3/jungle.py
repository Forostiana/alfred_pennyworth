from __future__ import annotations

from typing import Dict

import abc
import uuid
import random


class Animal(abc.ABC):

    def __init__(self, power: int, speed: int):
        self.id = str(uuid.uuid4())
        self.max_power = power
        self.current_power = power
        self.speed = speed

    def restore_power(self):
        self.current_power = min(self.max_power, self.current_power + int(self.max_power * 0.4))

    def loss_power(self):
        self.current_power = self.current_power - int(self.max_power * 0.3)

    @abc.abstractmethod
    def eat(self, jungle: Jungle):
        raise NotImplementedError

    def if_animal_can_search_food(self):
        return self.current_power > 0

    def catch(self, prey: Animal):
        return prey.speed < self.speed

    def kill(self, prey: Animal):
        return prey.current_power < self.current_power



class Predator(Animal):
    def eat(self, jungle: Jungle):
        if not self.if_animal_can_search_food():
            jungle.remove_animal(self)
            return

        prey = jungle.get_random_animal()
        if prey.id == self.id:
            self.loss_power()
            return
        is_killed = False
        is_caught = False
        if self.catch(prey):
            is_caught = True
            if self.kill(prey):
                jungle.remove_animal(prey)
                is_killed = True
        if not is_caught or not is_killed:
            self.loss_power()
            prey.loss_power()


class Herbivorous(Animal):

    def eat(self, jungle: Jungle):
        if self.if_animal_can_search_food():
            self.restore_power()
        else:
            jungle.remove_animal(self)


class Jungle:

    def __init__(self):
        self.animals: Dict[str, Animal] = dict()
        self.number = -1

    def __getitem__(self, item):
        length = len(self.animals)
        if self.number >= length - 1:
            self.number = -1
            raise StopIteration
        self.number += 1
        return list(self.animals.values())[self.number]

    def get_random_animal(self):
        return random.choice(list(self.animals.values()))

    def any_predator_left(self):
        if any(isinstance(animal, Predator) for animal in jungle.animals.values()):
            return True
        return False

    def add_animal(self, animal: Animal):
        self.animals[animal.id] = animal

    def remove_animal(self, animal: Animal):
        self.animals.pop(animal.id)


def animal_generator():
    while True:
        if random.randint(1, 2) == 1:
            yield Herbivorous(power=random.randint(20, 100), speed=random.randint(20, 100))
        else:
            yield Predator(power=random.randint(20, 100), speed=random.randint(20, 100))


if __name__ == "__main__":
    gen = animal_generator()
    jungle = Jungle()
    for i in range(10):
        jungle.add_animal(next(gen))

    while True:
        if not jungle.any_predator_left():
            break
        for animal in jungle:
            animal.eat(jungle=jungle)


#if __name__ == "__main__":
    # Create jungle
    # Create few animals
    # Add animals to jungle
    # Iterate throw jungle and force animals to eat until no predators left
    # animal_generator to create a random animal

