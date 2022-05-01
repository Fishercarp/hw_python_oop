from dataclasses import dataclass
from typing import Dict, Sequence, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        """Информация о тренировке."""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR = 60
    """"Переводит часы в минуты."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получаем дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIE_1: int = 18
    CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий: бег."""
        duration_in_min: float = self.duration * self.MIN_IN_HOUR
        return ((self.CALORIE_1 * self.get_mean_speed() - self.CALORIE_2)
                * self.weight / self.M_IN_KM * duration_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_1: float = 0.035
    WALK_2: float = 0.029
    WALK_3: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий: спортивная ходьба."""
        minute = self.duration * self.MIN_IN_HOUR
        """"Переводим часы в минуты"""
        return ((self.WALK_1 * self.weight
                + (self.get_mean_speed() ** self.WALK_3 // self.height)
                * self.WALK_2 * self.weight) * minute)


class Swimming(Training):
    """Тренировка: плавание."""
    SWM_TR_1: float = 1.1
    SWM_TR_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Получить среднюю скорость движения при плавании."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_distance(self) -> float:
        """Получить дистанцию в км. при плавании."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_spent_calories(self):
        """Количество затраченных калорий при плавании."""
        return ((self.get_mean_speed() + self.SWM_TR_1)
                * self.SWM_TR_2 * self.weight)


def read_package(workout_type: str,
                 data: Sequence[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    packages: Dict[str, Training] = {'SWM': Swimming,
                                     'RUN': Running,
                                     'WLK': SportsWalking}
    return packages[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
