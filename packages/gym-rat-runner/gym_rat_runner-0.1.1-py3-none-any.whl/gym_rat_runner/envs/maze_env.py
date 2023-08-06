import gym
from gym import error, spaces, utils
from collections import OrderedDict
from typing import Optional
import pandas as pd
import numpy as np
import  os
import glob
import random

import cv2 as cv

#Environment rewards

MOVE_REWARD = -1
HUNTER_REWARD = -300
TARGET_REWARD = 25

#Screen constants

UNIT = 50                           # Units for the renderization
GREEN = (21, 89, 33, 255)           # Background color
DARK_GREEN = (47, 68, 52, 255)
MAZE_FILE = "Maze1.csv"             # Maze file for the renderization

#Text parameters

font                    = cv.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText  = (10, 18*UNIT - UNIT//3)
fontScale               = 1
fontColor               = (255,255,255)
thickness               = 2
lineType                = 2

main_dir = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], os.pardir))

class MazeEnv(gym.Env):
    """docstring for MazeEnv."""

    metadata = {'render.modes': ['human', 'video', 'rgb_array']}

    class AnimatedObject():
        """
        Internal object to support interactive objects in the environment.
        """

        def __init__(self, pos = None):
            self.x = pos[0]
            self.y = pos[1]

            self.pos = (self.x, self.y)

        def __str__(self):
            return f"{self.x}, {self.y}"

        def __sub__(self, other):
            return np.array([self.x-other.x, self.y-other.y], np.int32)

        def move(self, x, y):
            self.x += x
            self.y += y
            self.pos = (self.x, self.y)

        def action(self, choice):
            """
            Gives the AnimatedObject the option to move in 8 directions.
            """

            actions = {
            0: (0,1),
            1: (-1,1),
            2: (-1,0),
            3: (-1,-1),
            4: (0,-1),
            5: (1,-1),
            6: (1,0),
            7: (1,1)
            }

            x, y = actions.get(choice)
            self.move(x,y)

        def newpos(self, x, y):
            self.x = x
            self.y = y
            self.pos = (self.x, self.y)

    def __init__(self):
        super(MazeEnv, self).__init__()

        #Load Maze
        maze_file = os.path.join(main_dir, 'envs', 'maze', MAZE_FILE)
        self.maze = pd.read_csv(maze_file, header = None)

        self.availablepos = []
        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                if self.maze.iloc[i,j] != 1:
                    self.availablepos.append([i,j])

        # Updates based on the Maze
        bottomLeftCornerOfText = (10, self.maze.shape[1]*UNIT - UNIT//2)

        #Load Images
        pathimages = os.path.join(main_dir, 'images', '*.png')

        self.images = {}
        for file in glob.glob(pathimages):
            figname = os.path.split(file)[1][:-4]
            self.images[figname] = cv.imread(file, cv.IMREAD_UNCHANGED)
            self.images[figname] = cv.resize(self.images[figname], (UNIT, UNIT), interpolation = cv.INTER_AREA)

        self.frames = []
        self.fps = 40

        # Animated Objects for the environment
        self.target = None
        self.player = None
        self.hunter = None

        # Set rewards for the game

        self.movereward = MOVE_REWARD
        self.huntereward = HUNTER_REWARD
        self.targetreward = TARGET_REWARD

        # range of Vision
        self.playervision = 40
        self.huntervision = 8

        self.action = 0  # The player enters in the maze in the Right direction.
        self.reward = 0
        self.done = False
        self.info = {}
        self.action_space = spaces.Discrete(8)

        self.stoc_rate = 0.2

        # The player is able to observer:
        #  - The cartesian position of himself.
        #  - The Hunter's position.
        #  - The Target's position.
        # NOTE: The value -1 for the hunter means that the player is unable to
        # see the Hunter.

        self.observation_space = spaces.Dict({
        "position": spaces.Box(low=np.array([0,0]), high=np.array(self.maze.shape), dtype=np.int32),
        "hunter": spaces.Box(low=np.array([-1,-1]), high=np.array(self.maze.shape), dtype=np.int32),
        "target": spaces.Box(low=np.array([0,0]), high=np.array(self.maze.shape), dtype=np.int32)
        })
        self.randompos = False

    def __overlay_image(img, img_overlay, x, y):
        """Overlay `img_overlay` onto `img` at (x, y) and blend using the alpha on boths images.

        """
        # Image ranges
        y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
        x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

        # Overlay ranges
        y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
        x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

        # Exit if nothing to do
        if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
            return

        # Blend overlay within the determined ranges
        img_crop = img[y1:y2, x1:x2]
        img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]

        alphaoverlay = img_overlay[y1o:y2o, x1o:x2o, 3]/255.0
        alphaunderlay = 1 - alphaoverlay

        for color in range(3):
            img_crop[:,:,color] = (alphaoverlay*img_overlay_crop[:,:,color] +
                                    alphaunderlay*img_crop[:,:,color])

    def __rotate_image(image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
        return result

    def __generateframe(self):

        height, width = self.maze.shape

        frame = np.zeros((height*UNIT, width*UNIT,4), np.uint8)
        frame[:] = DARK_GREEN
        greenblock = np.zeros((UNIT, UNIT,4), np.uint8)
        greenblock[:] = GREEN

        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                x = self.player.x - i
                y = self.player.y - j
                if self.maze.iloc[i,j] == 1:
                    MazeEnv.__overlay_image(frame, self.images['wall'], j*UNIT, i*UNIT)
                elif np.sqrt((x**2)+(y**2)) <= self.playervision:
                    MazeEnv.__overlay_image(frame, greenblock, j*UNIT, i*UNIT)


        # Expected Actions:
        # 0: Right movement
        # 1: Up-Right movement
        # 2: Up movement
        # 3: Up-Left movement
        # 4: Left movement
        # 5: Down-Left movement
        # 6: Down movement
        # 7: Down-Right movement

        player = MazeEnv.__rotate_image(self.images['rat'], (self.action - 6)*45)
        x = self.player.x
        y = self.player.y
        MazeEnv.__overlay_image(frame, player, y*UNIT, x*UNIT)
        x = self.player.x - self.hunter.x
        y = self.player.y - self.hunter.y
        if np.sqrt((x**2)+(y**2)) <= self.playervision:
            x = self.hunter.x
            y = self.hunter.y
            cat = MazeEnv.__rotate_image(self.images['cat'], (self.hunter_direction - 6)*45)
            MazeEnv.__overlay_image(frame, cat, y*UNIT, x*UNIT)
        x = self.target.x
        y = self.target.y
        MazeEnv.__overlay_image(frame, self.images['cheese'], y*UNIT, x*UNIT)

        cv.putText(frame,'Current Score: ' + str(self.reward),  bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)

        return frame

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action (object): an action provided by the agent

        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """

        # Expected Actions:
        # 0: Right movement
        # 1: Up-Right movement
        # 2: Up movement
        # 3: Up-Left movement
        # 4: Left movement
        # 5: Down-Left movement
        # 6: Down movement
        # 7: Down-Right movement

        actions = {
        0: (0,1),
        1: (-1,1),
        2: (-1,0),
        3: (-1,-1),
        4: (0,-1),
        5: (1,-1),
        6: (1,0),
        7: (1,1)
        }

        # Hunter movement


        prow, pcol = self.player.pos
        hrow, hcol = self.hunter.pos

        x = prow - hrow
        y = pcol - hcol

        if np.sqrt((x**2)+(y**2)) > self.huntervision:
            self.movehunter()

        else:
            self.movehunter()
            if self.player.pos != self.hunter.pos:
                self.movehunter()

        # Player movement
        if self.player.pos != self.hunter.pos:
            if self.spec.nondeterministic and random.uniform(0, 1) <= self.stoc_rate:
                self.action = random.choice(range(0,8))
            else:
                self.action = action

            # NOTE: Add Hunter movement before Player movement

            self.player.action(self.action)

            row, col = actions.get(self.action)
            crow, ccol = self.player.pos

            # Check Player colisions with walls and correct position if necessary.

            if self.maze.iloc[self.player.pos] == 1:

                if 'wall_colisions' in self.info.keys():
                    self.info['wall_colisions'] += 1
                else:
                    self.info['wall_colisions'] = 1

                if row != 0 and col != 0:
                    if self.maze.iloc[crow-row, ccol] != 1:
                        self.player.newpos(crow-row, ccol)
                    elif self.maze.iloc[crow, ccol-col] != 1:
                        self.player.newpos(crow, ccol-col)
                    else:
                        self.player.newpos(crow-row, ccol-col)
                else:
                    self.player.newpos(crow-row, ccol-col)

            if ccol < 0:
                self.player.newpos(crow, 33)
            elif ccol > 32:
                self.player.newpos(crow, 0)

            self.reward += self.movereward

        # Colision with the Hunter
        if self.player.pos == self.hunter.pos:
            self.reward += self.huntereward
            self.done = True

        # Colision with Target
        if self.player.pos == self.target.pos:
            self.reward += self.targetreward
            self.done = True



        return self.getObservation(), self.reward, self.done, self.info

    def reset(self, seed: Optional[int] = None):
        """Resets the environment to an initial state and returns an initial
        observation.

        Note that this function should not reset the environment's random
        number generator(s); random variables in the environment's state should
        be sampled independently between multiple calls to `reset()`. In other
        words, each call of `reset()` should yield an environment suitable for
        a new episode, independent of previous episodes.

        Returns:
          observation (object): the initial observation.
        """

        self.done = False
        self.reward = 0

        random.seed(seed)


        self.info = {}

        if self.randompos:
            # NOTE: Proabably will need to be redone
            random.shuffle(self.availablepos)
            self.target = self.AnimatedObject(self.availablepos[0])
            self.player = self.AnimatedObject(self.availablepos[1])
            self.hunter = self.AnimatedObject(self.availablepos[2])
        else:
            self.target = self.AnimatedObject([5,32])
            self.player = self.AnimatedObject([5,1])
            self.hunter = self.AnimatedObject([2,16])
            self.hunter_direction = 6

        return self.getObservation()

    def render(self, mode='human', videofile=None):
        """Renders the environment.

        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:

        - human: render to the current display or terminal and
        return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
        representing RGB values for an x-by-y pixel image, suitable
        for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
        terminal-style text representation. The text can include newlines
        and ANSI escape sequences (e.g. for colors).
        - video: Return a mov file unsing the Apple's version of the MPEG4 part 10/H.264 through the openvc library

        Note:
          Make sure that your class's metadata 'render.modes' key includes
            the list of supported modes. It's recommended to call super()
            in implementations to use the functionality of this method.

        Args:
          mode (str): the mode to render with

        Example:

        class MyEnv(Env):
          metadata = {'render.modes': ['human', 'rgb_array']}

          def render(self, mode='human'):
              if mode == 'rgb_array':
                  return np.array(...) # return RGB frame suitable for video
              elif mode == 'human':
                  ... # pop up a window and render
              else:
                  super(MyEnv, self).render(mode=mode) # just raise an exception
        """

        frame = self.__generateframe()

        if mode == 'human':

            cv.imshow("Maze Environment - Rat runner", frame)
            cv.waitKey(int((1/self.fps)*1000))

            if self.done:
                cv.destroyAllWindows()

        elif mode == 'rgb_array':
            self.frames.append(frame[:,:,:3])
            if self.done:
                frames = self.frames
                self.frames = []
                return frames

        elif mode == 'video':
            self.frames.append(frame[:,:,:3])
            if self.done:
                out = cv.VideoWriter(videofile,cv.VideoWriter_fourcc(*"avc1"), 20, (WIDTH, HEIGHT), True)
                for i in range(len(self.frames)):
                     out.write(self.frames[i])
                out.release()
                cv.destroyAllWindows()
                self.frames = []

        else:
            super(MazeEnv, self).render(mode=mode)

    def close(self):
        """Override close in your subclass to perform any necessary cleanup.

        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        pass

    def setrewards(self, movereward = MOVE_REWARD, targetreward = TARGET_REWARD, huntereward = HUNTER_REWARD):

        """Change the rewards values in the environment.
        """
        self.movereward = movereward
        self.targetreward = targetreward
        self.huntereward = huntereward

    def setfieldvision(self, range):
        self.playervision = range

    def setframepersec(self, fps = 40):
        self.fps = fps

    def getObservation(self):

        position = ('position',
                    np.array([self.player.x, self.player.y],
                    dtype='int32'))
        x = self.player.x - self.hunter.x
        y = self.player.y - self.hunter.y

        if np.sqrt((x**2)+(y**2)) <= self.playervision:
            x = self.hunter.x
            y = self.hunter.y
        else:
            x = -1
            y = -1

        hunter = ('hunter', np.array([x, y], dtype='int32'))

        target = ('target',
                    np.array([self.target.x, self.target.y],
                    dtype='int32'))

        return OrderedDict([position, hunter, target])

    def movehunter(self):

        actions = {
        0: (0,1),
        1: (-1,1),
        2: (-1,0),
        3: (-1,-1),
        4: (0,-1),
        5: (1,-1),
        6: (1,0),
        7: (1,1)
        }

        min_choices = self.hunter_direction - 2
        max_choices = self.hunter_direction + 3

        if  min_choices < 0:
            min_choices = 0
        if  max_choices > 8:
            max_choices = 8

        hunter_choices = list(range(min_choices, max_choices))

        if len(hunter_choices) < 6:
            if max_choices == 8:
                otherchoices = list(range(0,5-len(hunter_choices)))
            else:
                otherchoices = list(range(3+len(hunter_choices), 8))
            hunter_choices = hunter_choices +  otherchoices

        prow, pcol = self.player.pos
        hrow, hcol = self.hunter.pos

        # Remove wall colisions
        new_hunter_choices = hunter_choices.copy()
        for choice in hunter_choices:
            row, col = actions.get(choice)
            x = hrow+row
            y = hcol+col
            if self.maze.iloc[x, y] == 1.0:
                new_hunter_choices.remove(choice)
            elif y <= 0 or y >= 33:
                new_hunter_choices.remove(choice)

            hunter_choices = new_hunter_choices

        x = prow - hrow
        y = pcol - hcol

        if len(hunter_choices) == 0:
            if self.hunter_direction <= 3:
                new_direction = self.hunter_direction + 4
            else:
                new_direction = self.hunter_direction - 4

            self.hunter_direction = new_direction

        elif np.sqrt((x**2)+(y**2)) > self.huntervision:
            choice = random.choice(hunter_choices)
            self.hunter.action(choice)
            self.hunter_direction = choice
        else:
            check = pd.Series(dtype = 'float')
            for choice in hunter_choices:
                row, col = actions.get(choice)
                x = hrow+row - prow
                y = hcol+col - pcol

                check = pd.concat([check,
                                   pd.Series(index = [choice],
                                             data = [np.sqrt((x**2)+(y**2))],
                                             dtype = 'float')
                                  ])
            check.sort_values(ascending=True, inplace = True)
            self.hunter.action(check.index[0])
            self.hunter_direction = check.index[0]

    def randomposition(self, randompos = True):
        self.randompos = randompos

    def setstoc_rate(self, rate = 0.2):
        self.stoc_rate = rate
