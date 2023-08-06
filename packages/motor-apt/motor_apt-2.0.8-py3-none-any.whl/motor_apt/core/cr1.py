from motor_apt.core.extended_controller import ExtendedController
from motor_apt.core.property_extensions import classproperty


class CR1(ExtendedController):
    """
    A controller for a CR1/M-Z7 rotation stage
    """
    def __init__(self, *args, **kwargs):
        if 'persist_enccount' not in kwargs:
            kwargs['persist_enccount'] = True
        super(CR1, self).__init__(*args, **kwargs)

    @classproperty
    def max_velocity(cls):
        # http://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=4134
        # Note that these values should be pulled from the APT User software,
        # as they agree with the real limits of the stage better than
        # what the website or the user manual states
        # required return type: float
        return 4.00024

    @classproperty
    def max_acceleration(cls):
        # http://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=4134
        # Note that these values should be pulled from the APT User software,
        # as they agree with the real limits of the stage better than
        # what the website or the user manual states
        # required return type: float
        return 4.00024

    @classproperty
    def enccnt(cls):
        # from the manual
        # encoder counts per revolution of the output shaft: 12288
        # steps per revolution: 48
        # gearbox ratio: 256
        # required return type: float
        return 48 * 256 * 48 / 360.0  # 1638.4

    @classproperty
    def T(cls):
        # from the manual
        # required return type: float
        return 2048/6e6

    def home(self, channel=1, wait=False):
        raise NotImplementedError("CR1 does not provide homing capabilities")

    def set_home_parameters(self, channel=1, direction=2, limit_switch=1, velocity=None, distance_offset=0):
        raise NotImplementedError("CR1 does not provide homing capabilities")

    def home_parameters(self, channel=1, raw=False):
        raise NotImplementedError("CR1 does not provide homing capabilities")


if __name__ == '__main__':
    cr = CR1()