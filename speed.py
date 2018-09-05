class Speed:
    SIMULATION_SPEED = 1

    @classmethod
    def set_sim_speed(cls, value):
        cls.SIMULATION_SPEED = value

    @classmethod
    def get_sim_speed(cls):
        if (cls.SIMULATION_SPEED < 0):
            cls.SIMULATION_SPEED = -1/cls.SIMULATION_SPEED
        elif (cls.SIMULATION_SPEED == 0):
            cls.SIMULATION_SPEED = 1
        return cls.SIMULATION_SPEED
