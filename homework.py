from typing import Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

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
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.distance,
                           self.speed,
                           self.calories)


class Running(Training):
    """Тренировка: бег."""
    calorie_1: float = 18
    calorie_2: float = 20
    min_in_hour = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий: бег."""
        return ((self.calorie_1 * self.get_mean_speed() - self.calorie_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.min_in_hour)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    walk_1: float = 0.035
    walk_2: float = 0.029
    walk_3: float = 2
    min_in_hour = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий: спортивная ходьба."""
        return ((self.walk_1 * self.weight
                + (self.get_mean_speed() ** self.walk_3
                 // self.height) * self.walk_2 * self.weight)
                * self.duration * self.min_in_hour)


class Swimming(Training):
    """Тренировка: плавание."""
    swm_tr_1: float = 1.1
    swm_tr_2: float = 2
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
        return ((self.get_mean_speed() + self.swm_tr_1)
                * self.swm_tr_2 * self.weight)


def read_package(self, workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return (training_dict[workout_type](*data))


def main(training: Union[Swimming, Running, SportsWalking]) -> None:
    """Главная функция."""

    info = training.show_training_info()
    return info.get_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
