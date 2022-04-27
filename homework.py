from typing import Union

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, 
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
    training_type: str = 'Default'
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
        """Получить дистанцию в км."""
        return self.action * Training.LEN_STEP / Training.M_IN_KM
                

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / (self.duration * 60)
                      

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
                
        return InfoMessage(self.training_type,
                           self.duration,
                           self.distance,
                           self.speed,
                           self.calories)


class Running(Training):
    """Тренировка: бег."""    
    training_type: str = 'Running'
    calorie_1: float = 18
    calorie_2: float = 20 
    

    def __init__(self, action: int,
                 duration: float, 
                 weight: float) -> None:
        super().__init__(action, duration, weight)
        
    
    def get_spent_calories(self) -> float:
        """Количество затраченных калорий: бег."""
        
        return ((Running.calorie_1 * self.get_mean_speed() - Running.calorie_2) 
        * self.weight / Training.M_IN_KM * self.duration * 60)           
               

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    training_type: str = 'SportsWalking'
    walk_1: float = 0.035
    walk_2: float = 0.029   
    

    def __init__(self, action: int, 
                 duration: float, 
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        height: float
        self.height: float = height
        

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий: спортивная ходьба."""
        return ((SportsWalking.walk_1 * self.weight 
                + (self.get_mean_speed() **2 // self.height) * SportsWalking.walk_2 * self.weight) 
                * (self.duration * 60))             
        
            
class Swimming(Training):
    """Тренировка: плавание."""
    training_type: str = "Swimming"
    swm_tr_1 = 1.1
    swm_tr_2 = 2
    LEN_STEP = 1.38

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
        return self.length_pool * self.count_pool / Training.M_IN_KM / (self.duration * 60)

    def get_distance(self) -> float:
        """Получить дистанцию в км. при плавании.""" 
        return self.action * Swimming.LEN_STEP / Training.M_IN_KM      
                

    def get_spent_calories(self):
        """Количество затраченных калорий при плавании."""  
        return ((self.get_mean_speed() + Swimming.swm_tr_1) 
        * Swimming.swm_tr_2 * self.weight / (self.duration *60))         
    

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
        
    return training_dict[workout_type](*data)


def main(training: Union[Swimming, Running, SportsWalking]) -> None:
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