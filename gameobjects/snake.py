class SnakeSegment():
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class Snake():
    def __init__(self, display, block_size, pos_x=300, pos_y=300):
        self.color = (64, 78, 30)
        self.display = display
        self.block_size = block_size
        self.x_velocity = 0
        self.y_velocity = (-1)*self.block_size
        self.segments = []
        self.segments.append(SnakeSegment(pos_x, pos_y))
        self.prev_x_vel = 0
        self.prev_y_vel = 0


    def turn_left(self):
        if self.x_velocity > 0:
            return
        self.x_velocity = (-1)*self.block_size
        self.y_velocity = 0

    def turn_right(self):
        if self.x_velocity < 0:
            return
        self.x_velocity = self.block_size
        self.y_velocity = 0

    def turn_down(self):
        if self.y_velocity < 0:
            return
        self.y_velocity = self.block_size
        self.x_velocity = 0

    def turn_up(self):
        if self.y_velocity > 0:
            return
        self.y_velocity = (-1)*self.block_size
        self.x_velocity = 0

    def add_segment(self):
        self.segments.append(SnakeSegment(self.segments[-1].pos_x, self.segments[-1].pos_y))

    # SUMA PREDKOSCI DO POZYCJI

    def move(self):
        next_x_pos = self.segments[0].pos_x + self.x_velocity
        next_y_pos = self.segments[0].pos_y + self.y_velocity
        self.segments.pop()
        self.segments.insert(0, SnakeSegment(next_x_pos, next_y_pos))

    # RESET
    def reset_snake(self):
        self.segments = []
        self.segments.append(SnakeSegment(300, 300))
        self.x_velocity = 0
        self.y_velocity = (-1)*self.block_size