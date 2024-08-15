from PIL import Image, ImageDraw, ImageEnhance, ImageSequence
import math
import time
import os
import random 
class Time:
    def __init__(self, current_time, minute, second):
        self.current_time = current_time
        self.min = minute
        self.sec = second

class Font:
    def __init__(self):
        Image = Image.open("sprites/fonts.png")
        for pixel in Image.getdata():
            print(pixel)



class Generate:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.next_update = -1
        self.last_minute = -1
        self.gif_idx = -1
        self.in_gif = False
        self.gif = None
        self.next_gif = -1
    def create_image(self, current_time):      
        if current_time > self.next_update:
            # Generate a new background image
            
            self.generate_background(current_time)
            self.next_update = (current_time + 300) % 86400  # Update every 5 minutes

        # Load the background image
       

        if self.last_minute != current_time % 60:
            # Update the clock display every minute
            self.last_minute = current_time % 60
            self.draw_clock(current_time)

        
        
        
        
        if self.gif_idx != -1:
            
            image = Image.open("clock.png").convert("RGBA")
            gif_frame = self.gif[self.gif_idx].convert("RGBA")
            image.alpha_composite(gif_frame, (0, 0))
            image.save("overlayed_gif.png")
            
            delay = self.gif[self.gif_idx].info.get('duration', 100)  # Default to 100ms if no delay is set
            time.sleep(delay / 1000)
            self.gif_idx += 1
            if self.gif_idx >= len(self.gif):
                self.gif_idx = -1
            
        else:
            # Load a GIF every 5 minutes
            if current_time > self.next_gif:
                image = Image.open("clock.png").convert("RGBA")

                gif_directory = "sprites/gifs/"
                gif_files = os.listdir(gif_directory)
                random_gif_file = random.choice(gif_files)
                gif = Image.open(os.path.join(gif_directory, random_gif_file))

                
                self.gif_idx = 0
                self.gif = [f.copy() for f in ImageSequence.Iterator(gif)]
                self.next_gif = (current_time + 30) % 86400
                gif_frame = self.gif[self.gif_idx].convert("RGBA")
                self.gif_idx += 1
                image.alpha_composite(gif_frame, (0, 0))
                image.save("overlayed_gif.png")

            
        
    
    
    
    
    
    def draw_clock(self,current_time):
        image = Image.open("background.png").convert("RGBA")
        draw = ImageDraw.Draw(image)
        hour = current_time // 3600 % 12 + 1
        minute = (current_time % 3600) // 60
        
        hour_digit1 = hour // 10
        hour_digit2 = hour % 10
        minute_digit1 = minute // 10
        minute_digit2 = minute % 10
        digits = [Image.open(f"sprites/font/{i}.png") for i in range(10)]
        colon = Image.open("sprites/font/c.png")
        
    # Paste the digit images onto the background image
        if hour_digit1 == 0:
            offset = 13
        else:
            offset = 16
        hour_digit1_position = (offset, 4)
        hour_digit2_position = (offset+7, 4)
        colon_position = (offset+14, 4)
        minute_digit1_position = (offset+18, 4)
        minute_digit2_position = (offset+25, 4)
        
        if hour_digit1 != 0:
            image.alpha_composite(digits[hour_digit1], (hour_digit1_position))
       
        image.alpha_composite(digits[hour_digit2], (hour_digit2_position))
        image.alpha_composite(digits[minute_digit1], (minute_digit1_position))
        image.alpha_composite(digits[minute_digit2], (minute_digit2_position))
        image.alpha_composite(colon, colon_position)
        
        # Draw the clock hands
        image.save("clock.png")






    def get_sun_moon_position(self, current_time):
        # Calculate the sun and moon positions based on time
        # Assume sun moves from left (sunrise at 6 AM) to right (sunset at 6 PM)
        # Moon moves opposite, from right (moonrise at 6 PM) to left (moonset at 6 AM)
        
        
        
        if 6 <= current_time < 18:
            # Daytime: Sun is visible
            sun_x = int((current_time - 6) / 12 * self.width)
            sun_y = int(self.height * (1 - math.sin((current_time - 6) / 12 * math.pi)))
            moon_x = -100  # Hide moon
            moon_y = -100
           
        else:
            # Nighttime: Moon is visible
            moon_x = int(((current_time - 18) % 12) / 12 * self.width)
            moon_y = int(self.height  * (1 - math.sin(((current_time - 18) % 12) / 12 * math.pi)))
            sun_x = -100  # Hide sun
            sun_y = -100

        return (sun_x, sun_y), (moon_x, moon_y)

    def interpolate(self, color1, color2, factor):
        return tuple(int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))

    def generate_background(self,  current_time):
        
        img = Image.new('RGB', (self.width, self.height), (135, 206, 235)).convert("RGBA")  # Sky blue background
        draw = ImageDraw.Draw(img)
        current_time /= 3600  
        # Define color key points for day, sunset, and night
        morning_color = (18, 78, 137)  # Light Sky Blue (Morning)
        noon_color = (0, 153, 219)     # Cornflower Blue (Noon)
        evening_color = (18, 78, 137)    # Dark Slate Blue (Evening)
        night_color = (24, 20, 37)
        sunset_color = (247, 118, 37)  # Orange
        if 6 <= current_time < 12:
            factor = (current_time - 6) / 6  # 0 at 6 AM, 1 at 12 PM
            base_color = self.interpolate(morning_color, noon_color, factor)
        elif 12 <= current_time < 20:
            factor = (current_time - 12) / 6  # 0 at 12 PM, 1 at 6 PM
            base_color = self.interpolate(noon_color, evening_color, factor)
        elif 20 <= current_time < 24:
            factor = (current_time % 18) / 6  # 0 at 6 PM, 1 at 12 AM or 6 AM
            base_color = self.interpolate(evening_color, night_color, factor)

        elif 0 <= current_time < 6:
            factor = (current_time % 18) / 6  # 0 at 6 PM, 1 at 12 AM or 6 AM
            base_color = self.interpolate(night_color, morning_color, factor)
               
        
        sun_pos, moon_pos = self.get_sun_moon_position(current_time)
        # Fill the background with the calculated color
        for y in range(self.height):
            if 6 <= current_time < 18:
                # During the day, interpolate between sky blue and sunset orange near the sun
                factor = (y / self.height) * (sun_pos[1] / self.height /2)
                background_color = self.interpolate(base_color, sunset_color, factor)

            else:
                # During the night, keep the night sky color
                factor = (y / self.height) * (moon_pos[1] / self.height /2)
                background_color = self.interpolate(base_color, sunset_color, factor)
            
            draw.line([(0, y), (self.width, y)], fill=background_color)
 
        
        # Draw the sun
        sun_color = (254, 231, 97)  # Yellow
        draw.ellipse((sun_pos[0] - 2, sun_pos[1] - 2, sun_pos[0] + 2, sun_pos[1] + 2), fill=sun_color)
        grass = Image.open("./sprites/grass.png").convert("RGBA")
        
        # Draw the moon
        moon_color = (219, 203, 220)  # White
        draw.ellipse((moon_pos[0] - 2, moon_pos[1] - 2, moon_pos[0] + 2, moon_pos[1] + 2), fill=moon_color)
        
        if  current_time < 6:
            # Brighten the grass during the day
            brightness_factor = max((current_time)/ 6, .2)

            enhancer = ImageEnhance.Brightness(grass)
            grass = enhancer.enhance(brightness_factor)
            
        if current_time > 18:
            brightness_factor = max(((24 - current_time) % 6)/ 6, .2)
            enhancer = ImageEnhance.Brightness(grass)
            grass = enhancer.enhance(brightness_factor)
            
        img.alpha_composite(grass, (0,0))

       
        img.save("background.png")  



         


if __name__ == "__main__":
    i=0
    gen = Generate(64, 32)
    while(1):

       
        
        
        cur_time = i 
            
     
        img = gen.create_image(cur_time)
        i = (i + 100) % 86400
            

            




        
