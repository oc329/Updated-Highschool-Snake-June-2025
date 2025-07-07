## Importing and initializing pygame
import pygame
pygame.init()

class FPSController:
    def __init__(self, fps_limit, graphics_refresh_rate = 125):
        """
        Initialize the FPSController with the specified FPS limit.
        """
        self.fps_limit = fps_limit
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.dt_sum = 0
        
        self.graphics_and_movement_refresh_rate = graphics_refresh_rate
        
        ## Handling Input Refresh Functionality
        self.handling_input_refresh_rate = graphics_refresh_rate  // 4 
        self.handling_input_dt_sum = 0

    def should_update_graphics_and_movement(self):
        """
        Returns True if the amount of time passed since the last movement refresh is greater than the refresh rate.
        """
        if self.dt_sum >= self.graphics_and_movement_refresh_rate:
            self.dt_sum = 0
            return True
        return False
    
    def get_current_fps(self):
        """
        Returns the current FPS (Frames Per Second).
        Current FPS is the average of the last 10 clock ticks (pygame.time.Clock() obj)
        """
        return self.clock.get_fps()
    
    def limit_fps(self):
        """
        Limit the frames per second using the specified FPS limit.
        """
        self.dt = self.clock.tick(self.fps_limit)
        self.dt_sum += self.dt
        self.handling_input_dt_sum += self.dt
    

class SnakeFPSController(FPSController):
    """
    FPS controller with added functionality to increase game speed 
    and cap the speed at a certain number of points
    """
    def __init__(self, fps_limit, points_to_get_to_max_speed = 15, graphics_refresh_rate = 125):
        super().__init__(fps_limit, graphics_refresh_rate) 
        self.lowest_refresh_rate_limit = graphics_refresh_rate * 7 // 10
        self.points_to_get_to_max_speed = points_to_get_to_max_speed
        self.incremental_speed_amount = (self.graphics_and_movement_refresh_rate -  self.lowest_refresh_rate_limit) // self.points_to_get_to_max_speed
    
    def increase_game_speed(self):
        """
        Decreases the movement and graphics refresh time so the game moves faster. 
        Ensures the rate does not fall below the predefined lower limit.

        """
        new_rate = self.graphics_and_movement_refresh_rate - self.incremental_speed_amount
        self.graphics_and_movement_refresh_rate = max(new_rate, self.lowest_refresh_rate_limit)
