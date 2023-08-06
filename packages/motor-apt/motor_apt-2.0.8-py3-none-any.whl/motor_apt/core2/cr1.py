from motor_apt.core2.controller import Controller


class CR1(Controller):
    """
    A controller for a CR1/M-Z7 rotation stage
    """

    @property
    def max_velocity(self):
        # http://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=4134
        # Note that these values should be pulled from the APT User software,
        # as they agree with the real limits of the stage better than
        # what the website or the user manual states
        # required return type: float
        return 4.00024

    @property
    def max_acceleration(self):
        # http://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=4134
        # Note that these values should be pulled from the APT User software,
        # as they agree with the real limits of the stage better than
        # what the website or the user manual states
        # required return type: float
        return 4.00024

    @property
    def enccnt(self):
        # from the manual
        # encoder counts per revolution of the output shaft: 12288
        # steps per revolution: 48
        # gearbox ratio: 256
        # required return type: float
        return 48 * 256 * 48 / 360.0  # 1638.4

    @property
    def T(self):
        # from the manual
        # required return type: float
        return 2048/6e6