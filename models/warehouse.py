class Warehouse:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        self.rack_positions = []
        self.start = (0, 0)

    def generate_layout(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if y % 2 == 0:
                    row.append('.')  # aisle
                else:
                    if x % 3 == 2:
                        row.append('.')  # vertical aisle
                    else:
                        row.append('R')
                        self.rack_positions.append((x, y))
            self.grid.append(row)

        # set start position
        sx, sy = self.start
        self.grid[sy][sx] = 'S'
    
    def get_access_points(self, rack_pos):
        x, y = rack_pos
        access_points = []

        directions = [
            (0, -1),  # atas
            (0, 1),   # bawah
            (-1, 0),  # kiri
            (1, 0)    # kanan
        ]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if self.is_walkable(nx, ny):
                access_points.append((nx, ny))

        return access_points

    def display(self):
        for row in self.grid:
            print(' '.join(row))

    def is_walkable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] in ['.', 'S']
        return False