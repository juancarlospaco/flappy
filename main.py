# -*- coding: utf-8 -*-
"""Flappy Bird like Game"""


# imports
from random import randint
from bge.logic import (getCurrentScene, restartGame,
                       getCurrentController, keyboard)


# constants
list_of_obstacles, obstacle_interval = [], 15
next_obstacle = current_distance = score = velocity = 0
bird = getCurrentScene().addObject("bird", getCurrentController().owner)


################################################################################


def make_more_obstacles():
    """Makes more obstacles and put them inside camera view"""
    global next_obstacle, obstacle_interval
    obj = getCurrentScene().addObject("obstacles", getCurrentController().owner)
    obj.worldPosition[0] += 20  # Create new object and place it
    next_obstacle += obstacle_interval
    list_of_obstacles.append(obj)  # Append new objecto to list_of_obstacles
    obj.worldPosition[2] = randint(9, 22)  # obstacle height


def clear_the_obstacles():
    """Clean out the obstacles outside of camera view"""
    for index, obstacle in enumerate(list_of_obstacles):  # iterate obstacles
        if list_of_obstacles[index].worldPosition[0] < -20:  # if outside camera
            list_of_obstacles[index].endObject()  # end object
            del list_of_obstacles[index]  # delete references to it


def scroll_the_obstacles(speed=0.1):
    """Scroll the obstacles on screen"""
    global current_distance
    current_distance += speed
    for the_obstacle in list_of_obstacles:  # iterate list_of_obstacles
        the_obstacle.worldPosition[0] -= speed  # scroll the obstacles on screen


def is_dead():
    """Die if collide with obstacles or screen borders"""
    return (bird.localPosition[2] < 5 or bird.localPosition[2] > 25 or  # limits
            bird.controllers[0].sensors['Near'].positive)  # touched an obstacle


def rotate_the_bird():
    """Rotate the bird player to make the flap animation"""
    return 90 - (velocity * 70) if velocity > 0 else 90 + (-velocity * 60)


def calculate_score():
    """Calculate the total score integer"""
    return abs(current_distance // obstacle_interval - 1)  # get score integer


def main():
    """Main Game Loop"""
    global velocity
    # if user is pressing the Key make bird flap faster else fall down slowly
    if keyboard.events[146] is 1 or keyboard.events[32] is 1:  # UP or SPACEBAR
        velocity, bird['frame'] = 0.25, 0
    else:
        bird['frame'] += 1
        bird.worldPosition[2] += velocity
        velocity -= 0.02
    # Make new obstacles else move the existing obstacles and increase score
    if current_distance > next_obstacle:
        make_more_obstacles()
    else:
        scroll_the_obstacles()
        bird['rot'] = rotate_the_bird()
        score = getCurrentScene().objects['score']['Text'] = calculate_score()
    # if is dead restart as game over else clean obstacles out of camera view
    if is_dead():
        restartGame()
    else:
        clear_the_obstacles()


################################################################################


if __name__ in "__main__":
    print(__doc__)
