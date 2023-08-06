import gym
from gym import error, spaces, utils
from collections import OrderedDict
import pandas as pd
import numpy as np
import os
import glob

import cv2 as cv

SPACES = 10
MOVE_REWARD = -1
HUNTER_REWARD = -300
TARGET_REWARD = 25

# Screen constants

HEIGHT, WIDTH = 720, 720
UHEIGHT, UWIDTH = HEIGHT//(SPACES+2), WIDTH//(SPACES+2)
DARK_GREEN = (21, 89, 33)
MAZE_FILE = "Open_Maze.csv"

#Text parameters

font                    = cv.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText  = (10,HEIGHT-UHEIGHT//2)
fontScale               = 0.5
fontColor               = (255,255,255)
thickness               = 2
lineType                = 2

main_dir = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], os.pardir))

class OpenEnv(gym.Env):
    metadata = {'render.modes': ['human', 'video', 'rgb_array']}

    class AnimatedObject():
        """Internal object to generate the interactive objects"""

        def __init__(self, pos = None):
            if not pos:
                self.x = np.random.randint(0, SPACES)
                self.y = np.random.randint(0, SPACES)
            else:
                self.x = pos[0]
                self.y = pos[1]

        def __str__(self):
            return f"{self.x}, {self.y}"

        def __sub__(self, other):
            return np.array([self.x-other.x, self.y-other.y], np.int32)

        def move(self, x, y):
            self.x += x
            self.y += y

        def action(self, choice):
            '''
            Gives us 8 total movement options. (0,1,2,3,4,5,6,7)
            '''
            actions = {
            0: (1,0),
            1: (1,1),
            2: (0,1),
            3: (-1,1),
            4: (-1,0),
            5: (-1,-1),
            6: (0,-1),
            7: (1,-1)
            }

            x, y = actions.get(choice)
            self.move(x,y)

        def newpos(self, x, y):
            self.x = x
            self.y = y

    def __init__(self, width=SPACES, height=SPACES):

        # Load Maze
        maze_file = os.path.join(main_dir, 'envs', 'maze', MAZE_FILE)
        self.maze = pd.read_csv(maze_file, header = None)

        #Load Images
        pathimages = os.path.join(main_dir, 'images', '*.png')

        self.images = {}
        for file in glob.glob(pathimages):
            figname = os.path.split(file)[1][:-4]
            self.images[figname] = cv.imread(file, cv.IMREAD_UNCHANGED)
            self.images[figname] = cv.resize(self.images[figname], (UHEIGHT, UWIDTH), interpolation = cv.INTER_AREA)

        self.frames = []

        # Animated Objects for the environment
        self.target = None
        self.player = None
        self.hunter = None

        # Set rewards for the game

        self.movereward = MOVE_REWARD
        self.huntereward = HUNTER_REWARD
        self.targetreward = TARGET_REWARD

        self.action = None
        self.reward = 0
        self.done = False
        self.info = {}
        self.action_space = spaces.Discrete(8)

        # The player is only able to observer:
        #  - The distance between him and the hunter
        #  - The dstance between him and the target

        self.observation_space = spaces.Dict({
        'distanceTarget': spaces.Box(low=-SPACES + 1, high=SPACES - 1, shape=(2,), dtype=np.int32),
        'distanceEnemy':spaces.Box(low=-SPACES + 1, high=SPACES - 1, shape=(2,), dtype=np.int32)})
        self.isrendering = False
        self.deterministic = True

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

        frame = np.zeros((HEIGHT,WIDTH,4), np.uint8)
        frame[:] = (21, 89, 33, 255)

        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                if self.maze.iloc[i,j] == 1:
                    OpenEnv.__overlay_image(frame, self.images['wall'], i*UWIDTH, j*UHEIGHT)

        # Expected Actions:
        # 0: Right movement
        # 1: Up-Right movement
        # 2: Up movement
        # 3: Up-Left movement
        # 4: Left movement
        # 5: Down-Left movement
        # 6: Down movement
        # 7: Down-Right movement


        player = OpenEnv.__rotate_image(self.images['rat'], (self.action - 6)*45)
        x = self.player.x + 1
        y = 10 - self.player.y
        OpenEnv.__overlay_image(frame, player, x*UWIDTH, y*UHEIGHT)
        x = self.hunter.x + 1
        y = 10 - self.hunter.y
        OpenEnv.__overlay_image(frame, self.images['cat'], x*UWIDTH, y*UHEIGHT)
        x = self.target.x + 1
        y = 10 - self.target.y
        OpenEnv.__overlay_image(frame, self.images['cheese'], x*UWIDTH, y*UHEIGHT)

        cv.putText(frame,'Current Score: ' + str(self.reward) , bottomLeftCornerOfText,
                    font, fontScale, fontColor, thickness, lineType)

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

      # Player movement

      self.action = action
      self.player.action(action)

      pos = np.clip([self.player.x, self.player.y], 0, 9)
      self.player.newpos(pos[0], pos[1])

      obs = OrderedDict([('distanceEnemy', self.hunter - self.player),
      ('distanceTarget', self.target - self.player)])

      self.reward += self.movereward

      if (obs['distanceEnemy'] == np.array([0, 0])).all():
          self.reward += self.huntereward
          self.done = True
      if (obs['distanceTarget'] == np.array([0, 0])).all():
          self.reward += self.targetreward
          self.done = True

      return obs, self.reward, self.done, self.info

    def reset(self):
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

        # REVIEW: Save the info?

        self.info = {}


        if not self.deterministic:
            self.target = self.AnimatedObject()
            self.player = self.AnimatedObject()
            self.hunter = self.AnimatedObject()
        else:
            self.target = self.AnimatedObject([9,9])
            self.player = self.AnimatedObject([0,0])
            self.hunter = self.AnimatedObject([4,4])

        return OrderedDict([('distanceEnemy', self.hunter - self.player),
        ('distanceTarget', self.target - self.player)])

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

            cv.imshow("Open Environment - Rat runner", frame)
            cv.waitKey(25)

            if self.done:
                cv.destroyAllWindows()

        elif mode == 'rgb_array':

            self.frames.append(frame[:,:,:3])
            if self.done:
                return self.frames


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
            super(OpenEnv, self).render(mode=mode)

    def close(self):
      """Override close in your subclass to perform any necessary cleanup.

      Environments will automatically close() themselves when
      garbage collected or when the program exits.
      """
      pass

    def setstochastic(self, stoc = True):
        self.deterministic = stoc

    def setrewards(self, movereward = MOVE_REWARD,
                    targetreward = TARGET_REWARD, huntereward = HUNTER_REWARD):
        """ Change the rewards values in the environment.


        """
        self.movereward = movereward
        self.targetreward = targetreward
        self.huntereward = huntereward

    def test(self):
        print(main_dir)
