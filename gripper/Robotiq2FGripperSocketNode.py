from robotiq_gripper import RobotiqGripper


class RobotiqCGripper:

    PORT = 63352

    def __init__(self, gripper_ip, speed: int = 10, force: int = 10) -> None:
        self.gripper_ip = gripper_ip
        self.speed = speed
        self.force = force
        self.gripper = RobotiqGripper()

    def wait_for_connection(self) -> bool:
        self.gripper.connect(self.gripper_ip, RobotiqCGripper.PORT)

    def reset(self) -> None:
        self.gripper._reset()
        self.close()

    def activate(self, timeout: float = 30) -> bool:
        del timeout
        self.gripper.activate(auto_calibrate=True)
        return True

    def stop(self, block: bool, timeout: float) -> bool:
        # This is used to update the cur state.
        del block, timeout
        self._blocking_move(self._pos)
        return True

    def open(self, vel=0.1, force=100, block=False, timeout=10) -> None:
        del vel, force, block, timeout
        pos = self.gripper.get_open_position()
        self._blocking_move(pos)
        return True

    def close(self, vel=0.1, force=100, block=False, timeout=10) -> None:
        del vel, force, block, timeout
        pos = self.gripper.get_closed_position()
        self.gripper.move_and_wait_for_pos(pos, self.speed, self.force)

    def object_detected(self) -> bool:
        return self._status == RobotiqGripper.ObjectStatus.STOPPED_INNER_OBJECT

    def is_opened(self) -> bool:
        return self.gripper.is_open()

    def _blocking_move(self, pos: int) -> None:
        self._pos, self._status = self.gripper.move_and_wait_for_pos(
            pos, self.speed, self.force)
