import cv2
import numpy as np
import math
import imutils
import sys
import pdb
import random
from datetime import datetime
from time import sleep

from random import randint

from scipy.spatial import distance as dist

PLAYERS = ["X","O"]

class GameEngine(object):
    def __init__(self, dobot_manager=None, debug=0):
        self._dm = dobot_manager
        self.gameboard = ["?"]*16
        self.currentbuffer = 0
        self._gameboard = None # temporary variable for opencv board
        self.moves = []
        self.diff = None
        self.debug = debug
        self._winning_combinations = (
        [1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16],
        [1,5,9,13],[2,6,10,14],[3,7,11,15],[4,8,12,16],
        [1,6,11,16],[4,7,10,13]
        )
        self.player, self.enemy = self._ask_player_letter()
        self.currentplayer = self._decide_initial_player()

        if self._dm != None:
            self._dm.camera.movej_nooffset(self._dm, wait=1)
    
    def _is_board_empty(self):
        print(self._gameboard.status())
        unique = list(set(self._gameboard.status()))
        if (len(unique) == 1) and unique[0] == "?":
            return True
        return False
    
    def _is_game_won(self):
        for player in PLAYERS:
            for combos in self._winning_combinations:
                if (self.gameboard[combos[0]] == player and self.gameboard[combos[1]] == player and self.gameboard[combos[2]] == player):
                    return player
        if "?" not in self.gameboard:
            return "tie"
        return None

    def _is_game_won_player(self, player, board):
        for combos in self._winning_combinations:
            if (board[combos[0]] == player and board[combos[1]] == player and board[combos[2]] == player):
                return True

        return False

    def _get_free_position(self):
        board = self.gameboard
        free = [i for i,pos in enumerate(board) if pos=="?"]
        return random.choice(free)

    def _get_all_free_pos(self, board):
        free = [i for i, pos in enumerate(board) if pos == "?"]
        return free

    def _decide_initial_player(self):
        return random.choice(PLAYERS)

    def _ask_player_letter(self):
        player = input("Do you want to play as [O] or X? ")
        if (player.lower() == "x"):
            player="X"
            enemy="O"
        else:
            player="O"
            enemy="X"
        return (player, enemy)

    def _is_move_valid(self, move):
        pos = -1
        try:
            pos = int(move)
        except:
            return None
        if self.gameboard[pos] == "?":
            return pos
        return None

    def _update_board(self, pos, player):
        self.gameboard[pos] = player
        self._gameboard.positions[pos].draw_symbol_on_position(player, pos)

    def update_ai_board(self,pos,player, board):
        board[pos] = player
        return board

    def _ask_player_move(self):
        valid = False
        before = self.gameboard
        while (not valid):
            if self._dm != None:
                wait = input("Place token on board. Then press [enter]")
                try:
                    self._parse_gameboard(use_camera=True, gameboard_file="")
                    status = self._gameboard.status()
                except Exception as e:
                    print("ERROR: Unable to parse gameboard. Exception was: " + str(e))
                    status = before
                poslist = [i for i,v in enumerate(zip(before,status)) if v[0] not in PLAYERS and v[0] != v[1]]
                pos=-1
                if len(poslist)==0:
                    print("No new token detected. Please adjust the position.")
                    continue
                elif len(poslist)>1:
                    print("No cheating!")
                    pdb.set_trace()
                    continue
                pos = poslist[0]
                valid_pos = self._is_move_valid(pos)
                if (valid_pos != None):
                    valid = True
                    self._update_board(valid_pos, self.player)
                    self.currentplayer = self.enemy
            else:
                pos = input("Enter position [0-8]: ")
                valid_pos = self._is_move_valid(pos)
                if (valid_pos != None):
                    valid=True
                    self._update_board(valid_pos, self.player)
                    self.currentplayer = self.enemy

    def _make_move(self):
        print(self.currentplayer)
        if self.currentplayer == self.player:
            self._ask_player_move()
        else:
            self._ai_make_move()

    def init_gameboard_ai(self):
        #board = ["X", "?", "?", "O", "?", "O", "?", "X", "?"]
        board = 16*["?"]
        self.gameboard = board
        return board

    def _change_player(self,player):
        if player == "X":
            return "O"
        else:
            return "X"

    def minimax(self, newBoard, player):
        available_pos = self._get_all_free_pos(newBoard)
        if self._is_game_won_player("X", newBoard):
            score = 0
            return score
        elif self._is_game_won_player("O", newBoard):
            score = 100
            return score
        elif len(available_pos) == 0:
            score = 50
            return score

        if player == "O":
            bestVal = 0
            for var in available_pos:
                # print("Making move: " + str(var))
                newBoard = self.update_ai_board(var, player, newBoard)
                moveVal = self.minimax(newBoard, "X")
                newBoard = self.update_ai_board(var, "?", newBoard)
                bestVal = max(bestVal, moveVal)
            return bestVal


        if player == "X":
            bestVal = 100
            for var in available_pos:
                # print("Making move: " + str(var))
                newBoard = self.update_ai_board(var, player, newBoard)
                moveVal = self.minimax(newBoard, "O")
                newBoard = self.update_ai_board(var, "?", newBoard)
                bestVal = min(bestVal, moveVal)
            return bestVal



    def make_best_move(self, board, player,difficulty):
        if difficulty == "Easy":
            diff_random = 25
        elif difficulty == "Medium":
            diff_random = 50
        elif difficulty == "Hard":
            diff_random = 75
        else:
            diff_random = 100
        # Generate random
        rnum = randint(0, 100)
        # Find available moves
        initValue = 50
        best_choices = []

        available_pos = self._get_all_free_pos(board)
        if len(available_pos)==9 and diff_random == 100:
            return 4
        if rnum > diff_random:
            move = random.choice(available_pos)
            return move

        else:
            if player == "O":
                for move in available_pos:
                    board = self.update_ai_board(move, player, board)
                    moveVal = self.minimax(board, self._change_player(player))
                    board = self.update_ai_board(move, "?", board)

                    if moveVal > initValue:
                        best_choices = [move]
                        return move
                    elif moveVal == initValue:
                        best_choices.append(move)
            else:
                for move in available_pos:
                    board = self.update_ai_board(move, player, board)
                    moveVal = self.minimax(board, self._change_player(player))
                    board = self.update_ai_board(move, "?", board)

                    if moveVal < initValue:
                        best_choices = [move]
                        return move
                    elif moveVal == initValue:
                        best_choices.append(move)

            if len(best_choices)>0:
                return random.choice(best_choices)
            else:
                return random.choice(available_pos)



    def _ai_make_move(self):
        origBoard = self.gameboard
        print(origBoard)
        pos = self.make_best_move(origBoard,self.enemy,self.diff) 
        #pos = self._get_free_position()
        if self._dm != None:
            self._dm.buffer[self.currentbuffer].pick(self._dm)
            #self._dm.camera.movej_nooffset(self._dm, wait=0)
            self._dm.slot[pos].place(self._dm)
            self._dm.camera.movej_nooffset(self._dm, wait=0)
            self.currentbuffer += 1
        self._update_board(pos, self.enemy)
        self.currentplayer = self.player
       
    def show_gameboard(self, gameboard=None):
        if gameboard==None:
            t = self.gameboard
        else:
            t = gameboard
        print("{0} {1} {2} {3}".format(t[0], t[1], t[2], t[3]))
        print("{0} {1} {2} {3}".format(t[4], t[5], t[6], t[7]))
        print("{0} {1} {2} {3}".format(t[8], t[9], t[10], t[11]))
        print("{0} {1} {2} {3}".format(t[12], t[13], t[14], t[15]))

    def _parse_gameboard(self, use_camera, gameboard_file):
        if use_camera==False:
            image = cv2.imread(gameboard_file)
        else:
            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            ret_val, image = cam.read()
            #cv2.imwrite(datetime.now().strftime("%H%M%S.jpg"), image)
            cam.release()
            cv2.destroyAllWindows()
        #if self._gameboard != None:
        #   self._gameboard = Gameboard.update_gameboard(self._gameboard)
        self._gameboard = Gameboard.detect_game_board(image, debug=self.debug)


    def start(self, use_camera=False, gameboard_file="games/default.jpg"):
        self._parse_gameboard(use_camera, gameboard_file)
        if not self._is_board_empty():
            raise Exception("Board is not empty. Please clear board.")

        # Print board status
        ai_player = self.enemy
        hu_player = self.player

        difficulty = int(input(" 1: Easy \n 2: Medium \n 3: Hard \n 4: Expert \n Choose a difficulty: "))
        if difficulty == 1:
            self.diff = "Easy"
        elif difficulty == 2:
            self.diff = "Medium"
        elif difficulty == 3:
            self.diff = "Hard"
        else:
            self.diff = "Expert"
        while (not self._is_game_won()):
            try:
                self._parse_gameboard(use_camera, gameboard_file)
            except Exception as e:
                print("Unable to detect game board.")
                sleep(1)
                continue
            print("Your move player {0}".format(self.currentplayer))
            #pdb.set_trace()
            self._make_move()
            self.show_gameboard()
        winner = self._is_game_won()
        if (winner == "tie"):
            print("GAME OVER! IT WAS A TIE!")
        elif (winner == self.player):
            print("YOU WON!")
            if self._dm != None:
                self._dm.set_speed(velocity=20)
                self._dm.pose.move_nooffset(self._dm, wait=0.5)
                self._dm.set_speed()
        else:
            print("GAME OVER! YOU LOST!")
            if self._dm != None:
                self._dm.set_speed(velocity=50)
                for i in range(3):
                    self._dm.pose.movej_nooffset(self._dm, wait=0)
                    self._dm.camera.movej_nooffset(self._dm, wait=0)


class Gameposition(object):
    def __init__(self, src_image, bin_image, title, positions, debug=False):
        self.source = src_image
        self.image = bin_image
        self.id = str(id(self))
        self.title = title
        self.symbol = "?"
        self.area = None
        self.positions = positions
        self.solidity = None
        self.debug = debug
        self._process_subimage(positions)

    def _process_subimage(self, positions):
        #4-by-4 field
        (tl, tr, bl, br) = tuple(positions)
        self.startpos = list(tl)
        self.endpos = list(br)
        dx = int(round(dist.euclidean(tl, tr),0))
        dy = int(round(dist.euclidean(tl, bl),0))
        
        # NOTE: self.image.shape returns [y,x] and not [x,y]
        if (self.endpos[0] > self.image.shape[1]):
            self.endpos[0] = list(self.image.shape)[1]
        if (self.endpos[1] > self.image.shape[0]):
            self.endpos[1] = list(self.image.shape)[0]
        self.startpos = tuple(self.startpos)
        self.endpos = tuple(self.endpos)
        self.roi = self.image[self.startpos[1]:self.endpos[1], self.startpos[0]:self.endpos[0]]
        
        self.roi_in_source = self.source[self.startpos[1]:self.endpos[1], self.startpos[0]:self.endpos[0]]
        self.area = dx*dy
        #print("{0}, Total area: {1} - TL(x,y) = {2},{3}, BR(x,y) = {4},{5}".format(self.title, self.area, self.startpos[0],self.startpos[1],self.endpos[0],self.endpos[1]))

        """
        source = cv2.imread("games/field.jpg")
        cv2.rectangle(source, (self.startpos[0],self.startpos[1]), (self.endpos[0],self.endpos[1]), (255,0,0), 2)
        position_title = self.title
        cv2.imwrite("images/area/" +  position_title+".jpg",source)
        """

    def draw_rectangle_on_image(self, image=None):
        if (type(image) != np.ndarray):
            image = self.image
        cv2.rectangle(image, self.startpos, self.endpos, (255,0,0), 1)
        coordinate = (int((self.endpos[0]+self.startpos[0])/2), int((self.endpos[1]+self.startpos[1])/2))
        font = cv2.FONT_HERSHEY_SIMPLEX
        black = (0,0,0)
        cv2.putText(self.source, self.title, coordinate, font, 2, black, 2, cv2.LINE_AA)

    def draw_symbol_on_position(self, symbol, position):
        coordinate = tuple(self.positions[0])
        font = cv2.FONT_HERSHEY_SIMPLEX
        black = (0,0,0)
        cv2.putText(self.source, symbol, coordinate, font, 4, black, 2, cv2.LINE_AA)
    
    def is_checked(self):
        return False
    
    def detect_symbol(self, avg_area=None):
        """ Attempts to detect a symbol in self.roi
        based on:
        * https://gurus.pyimagesearch.com/lesson-sample-advanced-contour-properties/
        * http://qtandopencv.blogspot.com/2015/11/analyze-tic-tac-toe-by-computer-vision.html
        """
        imgcopy = self.roi.copy()
        cnts = cv2.findContours(imgcopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        lSolidity = []
        #if self.title == "mm":
        #    pdb.set_trace()
        for (i, c) in enumerate(cnts):
            # compute the area of the contour along with the bounding box
            # to compute the aspect ratio
            area = cv2.contourArea(c)
            # if there are multiple contours detected, check if the detected contour is at
            # least 6% of total area
            # also ignore the contour if it is larger than 70% of total area or less than 6% of total area
            ratio = area/self.area
            if ((len(cnts) > 1 and i>=0 and (area < self.area*0.01)) or ratio > 0.70 or ratio < 0.06):
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            # compute the convex hull of the contour, then use the area of the
            # original contour and the area of the convex hull to compute the
            # solidity
            hull = cv2.convexHull(c)
            hullArea = cv2.contourArea(hull)
            if (hullArea == 0):
                hullArea = 0.01
            solidity = area / float(hullArea)
            self.solidity = solidity
            lSolidity.append(solidity)
            found = False
            if (self._detect_if_o(solidity)):
                self.symbol = "O"
                found = True
            elif (self._detect_if_x(solidity)):
                found = True
                self.symbol = "X"
            
            if found:
                if self.debug>0:
                    print("{0}: Contours: {1}, Solidity: {2}, Ratio: {3}, Detected: {4}".format(self.title, len(cnts), solidity, ratio, self.symbol))
                    img = self.roi_in_source.copy()
                    cv2.drawContours(img,[c],0,(0,255,0),-1)
                    cv2.imshow(self.title, img)
                if self.debug>1:
                    cv2.waitKey(0)
                break
        if (self.symbol in ("O","X")):
            cv2.putText(self.roi_in_source, self.symbol, (int(x+(w/2)), int(y+(h/2))), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 255), 4)
            return True
        return False
    
    def _detect_if_x(self, solidity):
        if (solidity > 0.30 and solidity < 0.9):
            return True
        return False
    
    def _detect_if_o(self, solidity):
        if (solidity > 0.9):
            return True
        return False
        

class Gameboard(object):
    boardtype = "4x4"
    def __init__(self, img_source, img_binary, intersection_width, intersection_points, gameboard=None, debug=False):
        self.source = img_source
        self.binary = img_binary
        self.intersection_width = intersection_width
        self.intersection_points = intersection_points
        self.intersection_mask = None
        self.debug = debug
        
        self.positions = []
        self._calculate_positions()
        #self.intersection_mask = gameboard.intersection_mask
        #self.intersection_points = gameboard.intersection_points
        
        self._draw_positions()
        self._detect_symbols()
        if debug > 0:
            cv2.waitKey(0)

    def __repr__(self):
        jeje = str(self.status())
        return jeje

    def draw_symbol_on_slot(self, symbol, slot):
        pass

    def status(self):
        return [pos.symbol for pos in self.positions]

    def _detect_symbols(self):
        for position in self.positions:
            position.detect_symbol()

    def _draw_positions(self):
        for position in self.positions:
            position.draw_rectangle_on_image(self.source)
        if self.debug>0:
            cv2.imshow("Game positions", self.source)
        if self.debug>1:
            cv2.waitKey(0)

    def _order_points(self, unordered_points):
        # for 4-by-4 field
        pts = np.array(unordered_points,dtype=int)

        # Sort by X coordinates
        xSorted = pts[np.argsort(pts[:,0]),:]
        # Grab left-most and right-most points from the sorted x-coordinates
        leftMost = xSorted[:5, :]
        centerLeft = xSorted[5:10, :]
        centerMost = xSorted[10:15, :]
        centerRight = xSorted[15:20, :]
        rightMost = xSorted[20:25, :]

        # Sort left-most according to Y-coordinates to find top left and bottom left
        leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
        (p11,p21,p31,p41,p51) = leftMost

        centerLeft = centerLeft[np.argsort(centerLeft[:, 1]), :]
        (p12,p22,p32,p42,p52) = centerLeft

        centerMost = centerMost[np.argsort(centerMost[:, 1]), :]
        (p13,p23,p33,p43,p53) = centerMost

        centerRight = centerRight[np.argsort(centerRight[:, 1]), :]
        (p14,p24,p34,p44,p54) = centerRight

        (p15,p25,p35,p45,p55) = rightMost[np.argsort(rightMost[:, 1]), :]

        sorted_positions = np.array([p11,p12,p13,p14,p15,p21,p22,p23,p24,p25,p31,p32,p33,p34,p35,p41,p42,p43,p44,p45,p51,p52,p53,p54,p55],dtype=int)
        return sorted_positions

    def _slope(self, a, b):
        return float((b[1]-a[1])/(b[0]-a[0]))

    def _create_line(self, p1, p2, vertical=True):
        p = [0,0]
        q = list(self.source.shape[0:2])
        if not vertical:
            tmp = q[0]
            q[0] = q[1]
            q[1] = tmp
            
        if (p1[0] != p2[0]):
            m = self._slope(p1,p2)
            # y = m * x + b
            # b = y - (m*x)
            b = p1[1] - m*p1[0]
            p[1] = int(m * p[0] + b)
            q[1] = int(m * q[0] + b)
        else:
            p[0] = p2[0]
            q[0] = p2[0]
        p = tuple(p)
        q = tuple(q)
        return (p,q)

    def _create_mask(self, ordered_intersection_points):
        pts = ordered_intersection_points
        l1 = self._create_line(list(pts[0]), list(pts[2]))
        l2 = self._create_line(list(pts[1]), list(pts[3]))
        l3 = self._create_line(list(pts[0]), list(pts[1]), vertical=False)
        l4 = self._create_line(list(pts[2]), list(pts[3]), vertical=False)

        mask = np.zeros(self.source.shape, self.source.dtype)

        white = (255,255,255)
        black = (0,0,0)
        cv2.line(mask,l1[0],l1[1],white,int(self.intersection_width*1.1))
        cv2.line(mask,l2[0],l2[1],white,int(self.intersection_width*1.1))
        cv2.line(mask,l3[0],l3[1],white,int(self.intersection_width*1.1))
        cv2.line(mask,l4[0],l4[1],white,int(self.intersection_width*1.1))
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        #invert mask
        mask = cv2.bitwise_not(mask)
        
        if self.debug > 2:
            cv2.imshow("mask", mask)
            cv2.waitKey(0)
        self.binary = cv2.bitwise_and(self.binary, mask)

    def _calculate_positions(self):
        intersections = self._order_points(self.intersection_points)# all intersections contai
        """
            [1,  2,  3,  4]
            [5,  6,  7,  8]
            [9, 10, 11, 12]
            [13,14, 15, 16]

             ------>x
            |
            |
            |
            |
            ↓
            y
        """

        locations =[]
        w = 3
        for i in range(20):
            if (i+1)%5 == 0:
                continue;
            
            intersections[i][0]+=w
            intersections[i][1]+=w
            intersections[i+1][0]-=w
            intersections[i+1][1]+=w
            intersections[i+5][0]+=w
            intersections[i+5][1]-=w
            intersections[i+6][0]-=w
            intersections[i+6][1]-=w

            locations.append(
                [
                [intersections[i][0],intersections[i][1]],
                [intersections[i+1][0],intersections[i][1]],
                [intersections[i+5][0],intersections[i+5][1]],
                [intersections[i+6][0],intersections[i+6][1]]
                ]
            )

        
        source = cv2.imread("images/toma.jpg")
        for l in locations:
            cv2.rectangle(source,l[0],l[3],(255,0,0),2)
        cv2.imwrite("images/intersections/ikuta.jpg",source)
        

        for i in range(16):
            self.positions.append(
                    Gameposition(self.source, self.binary, "rc" + str(i),locations[i] , self.debug))
            

    @staticmethod
    def _get_center_position_of_rectangle(x1,x2,y1,y2):
        return (x1+int((x2-x1)/2), int(y1+(y2-y1)/2))

    @staticmethod
    def _preprocess_image_to_binary(image, debug=False):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thres, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        kernel = np.array((
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]
        ), dtype="int")
        binary = cv2.erode(binary, kernel)
        # Invert the image
        binary = 255-binary
        if debug > 2:
            cv2.imshow("binary",binary)
            cv2.waitKey(0)
        return binary

    @staticmethod
    def update_gameboard(gameboard):
        source = gameboard.source
        binary = gameboard.binary
        w = gameboard.intersection_width
        positions = gameboard.positions
        return Gameboard(source, binary, w, positions, gameboard=gameboard)
        
    @staticmethod
    def detect_game_board(source, debug=False):
        image = Gameboard._preprocess_image_to_binary(source, debug)
        # Defining a kernel length
        kernel_length = np.array(image).shape[1]//8
        # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
        verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
        # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
        hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
        # A kernel of (4 X 4) ones
        kernel = np.array((
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]), dtype="int")
        # Morphological operation to detect vertical lines from an image
        img_temp1 = cv2.erode(image, verticle_kernel, iterations=1)
        verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=1)
        if debug > 3:
            cv2.imshow("vlines", verticle_lines_img)
            cv2.waitKey(0)
        # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv2.erode(image, hori_kernel, iterations=1)
        horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=1)
        if debug > 3:
            cv2.imshow("hlines", horizontal_lines_img)
            cv2.waitKey(0)
        intersections = cv2.bitwise_and(verticle_lines_img, horizontal_lines_img)
        if debug > 2:
            cv2.imshow("intersections", intersections)
            cv2.waitKey(0)
        # Create a mask, combine verticle and horizontal lines
        mask = verticle_lines_img + horizontal_lines_img
        # Find contours
        contours, hierarchy = cv2.findContours(intersections, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Find center positions, order = bottom left, bottom right, upper left, upper right
        positions = []
        red = (0,0,255)
        blue = (255,0,0)
        for i,cnt in enumerate(contours):
            boardweight = 0.1 # decrease this for finer detection
            approx = cv2.approxPolyDP(cnt, boardweight*cv2.arcLength(cnt, True), True)

            cv2.drawContours(source,[cnt],0,red,-1)
            if debug>3:
                cv2.imshow("Showing game board intersection {0}".format(i+1),source)
                cv2.waitKey(0)
            if len(approx) == 4:
                # get the bounding rect
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(source, (x,y), (x+w,y+h), (255,0,0), 1)
                if debug>1:
                    cv2.imshow("rectangle", source)
                    cv2.waitKey(0)
                center = Gameboard._get_center_position_of_rectangle(x, x+w, y, y+h)
                positions.append(center)
            else:
                raise Exception("Unable to detect game board intersections. Try to adjust the weight.")
        if (len(positions) != 25):
            raise Exception("Unable to detect 4x4 game board")
        #if (len(positions) != 4):
        #    raise Exception("Unable to detect 3x3 game board")
        return Gameboard(source, image, w, positions, debug=debug)