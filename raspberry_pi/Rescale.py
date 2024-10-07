def map_clothes_to_leds(num_clothes, num_leds):
    # Mapping from clothes to LEDs
    constant = num_clothes / num_leds
    clothes_to_leds = {}
    leds_to_clothes = {i: [] for i in range(1, num_leds + 1)}

    for i in range(num_clothes):
        # Assigning each cloth to an LED
        led_index = (i // constant) % num_leds + 1  # First two clothes share LED 1, next two LED 2, etc.
        clothes_to_leds[i + 1] = led_index
        leds_to_clothes[led_index].append(i + 1)
    
    return clothes_to_leds, leds_to_clothes


# Example usage
num_clothes = int(input("Enter number of clothes: "))
num_leds = int(input("Enter number of LEDs available: "))
clothes_to_leds, leds_to_clothes = map_clothes_to_leds(num_clothes, num_leds)

print("Clothes to LEDs mapping:", clothes_to_leds)
#print("LEDs to Clothes mapping:", leds_to_clothes)












    





