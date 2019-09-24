def reward_function(params):
    
    import math
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    progress = params['progress']
    on_track = params['all_wheels_on_track']
    
    # CONSTS
    MIN_REWARD = 1e-3
    MAX_REWARD = 1e2
    DIRECTION_THRESHOLD = 10.0
    ABS_STEERING_THRESHOLD = 30
    MAX_SPEED = 8.0
    speed_slug = 0.01 * MAX_SPEED
    speed_slow = 0.11 * MAX_SPEED
    speed_moderate = 0.33 * MAX_SPEED
    speed_fast = 0.80 * MAX_SPEED
    
    def on_track_reward(current_reward, on_track):
        if not on_track:
            current_reward = MIN_REWARD
        else:
            current_reward = MAX_REWARD
        return current_reward
    
    def distance_from_center_reward(current_reward, track_width, distance_from_center):
        # Calculate 3 markers that are at varying distances away from the center line
        marker_1 = 0.1 * track_width
        marker_2 = 0.25 * track_width
        marker_3 = 0.5 * track_width

        # Give higher reward if the car is closer to center line and vice versa
        # Pretty much the center
        if distance_from_center <= marker_1:
           current_reward = 0.99
        elif distance_from_center <= marker_2:
            current_reward = 0.33
        elif distance_from_center <= marker_3:
            current_reward = 0.11
        else:
            current_reward = 1e-3           # likely crashed/ close to off track
        return current_reward
        
    def complete_lap(current_reward, progress):
        # promote complete laps
        if progress == 100.0:
            current_reward *= 1000
        return current_reward
    
    def like_sanic(current_reward, speed):
        # promote speediness
        if speed <= speed_slug:
            current_reward *= 0.9          # bad boy
        elif speed <= speed_slow:
            current_reward *= 1.1
        elif speed <= speed_moderate:
            current_reward *= 1.33
        elif speed <= speed_fast:
            current_reward *= 1.5
        else:
            current_reward = MIN_REWARD          ## slow down do not let it get too fast
        return current_reward
        
    def straight_line_reward(current_reward, steering, speed):
        # Positive reward if the car is in a straight line going fast
        if abs(steering) < 0.1 and speed > speed_moderate:
            current_reward *= 1.2
        return current_reward
    
    def throttle_reward(current_reward, speed, steering):
        # Decrease throttle while steering
        if speed > speed_moderate - (0.4 * abs(steering)):
            current_reward *= 0.8
        return current_reward

    import math 
    reward = math.exp(-6 * distance_from_center)
    reward = on_track_reward(reward, on_track)  # stay on track
    reward = distance_from_center_reward(reward, track_width, distance_from_center) # stay center
    reward = complete_lap(reward, progress) # promote full laps
    reward = like_sanic(reward, speed)  # promote going moderate speed, penalize sluggish and too fast
    reward = straight_line_reward(reward, steering, speed)  # promote going fast in a straight line
    reward = throttle_reward(reward, speed, steering) # penalize turning when going moderate speed
    # need to implement v
    #reward = steering_reward(reward, steering)
    #
    #reward = distance_from_center_reward(reward, track_width, distance_from_center)
    return float(reward)

    def straight_line_reward(current_reward, steering, speed):
        # Positive reward if the car is in a straight line going fast
        if abs(steering) < 0.1 and speed > speed_moderate:
            current_reward *= 1.2
        return current_reward
    
    def throttle_reward(current_reward, speed, steering):
        # Decrease throttle while steering
        if speed > speed_moderate - (0.4 * abs(steering)):
            current_reward *= 0.8
        return current_reward
 
    reward = math.exp(-6 * distance_from_center)
    reward = on_track_reward(reward, all_wheels_on_track)  # stay on track (additive)
    reward = distance_from_center_reward(reward, track_width, distance_from_center) # stay center
    reward = complete_lap(reward, progress) # promote full laps
    reward = like_sanic(reward, speed)  # promote going moderate speed, penalize sluggish and too fast
    reward = straight_line_reward(reward, steering, speed)  # promote going fast in a straight line
    reward = throttle_reward(reward, speed, steering) # penalize turning when going moderate speed
    return float(reward)
