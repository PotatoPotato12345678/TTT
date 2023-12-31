from tictactoe import *

title = "Tic tac toe board tester"

def print_header():
    print("-"*len(title))
    print(title)
    print("-"*len(title))

def main():
    tests = {"Empty board (handdrawn)": {
                "path":"tests/empty_board.jpg",
                "x_count": 0,
                "o_count": 0},
             "Empty board (computer drawn)": {
                "path":"tests/empty_board_2.jpg",
                "x_count": 0,
                "o_count": 0},
             "Empty board (camera, low light 1)": {
                "path":"tests/cam_lowlight_empty_1.jpg",
                "x_count": 0,
                "o_count": 0},
             "Empty board (camera, low light 2)": {
                "path":"tests/cam_lowlight_empty_2.jpg",
                "x_count": 0,
                "o_count": 0},
             "Empty board (camera, medium light 1)": {
                "path":"tests/cam_mediumlight_empty_1.jpg",
                "x_count": 0,
                "o_count": 0},
             "Empty board (camera, medium light 2)": {
                "path":"tests/cam_mediumlight_empty_2.jpg",
                "x_count": 0,
                "o_count": 0},
             "Empty board (camera, shadow 1)": {
                "path":"tests/cam_shadow_empty.jpg",
                "x_count": 0,
                "o_count": 0},
             "Camera, O=1": {
                "path":"tests/cam_1O.jpg",
                "x_count": 0,
                "o_count": 1},
             "Camera, O=2": {
                "path":"tests/cam_2O.jpg",
                "x_count": 0,
                "o_count": 2},
             "Camera, O=4": {
                "path":"tests/cam_4O.jpg",
                "x_count": 0,
                "o_count": 4},
             "Camera, O=4, X=1": {
                "path":"tests/cam_4O_1X.jpg",
                "x_count": 1,
                "o_count": 4},
             "Camera, O=4, X=2": {
                "path":"tests/cam_4O_2X.jpg",
                "x_count": 2,
                "o_count": 4},
             "Camera, O=6, X=3, v1": {
                "path":"tests/cam_6O_3X_1.jpg",
                "x_count": 3,
                "o_count": 6},
             "Camera, O=6, X=3, v2": {
                "path":"tests/cam_6O_3X_2.jpg",
                "x_count": 3,
                "o_count": 6},
             "One average x":{
                "path":"tests/one_average_x.jpg",
                "x_count": 1,
                "o_count": 0},
            "O=4 and X=3":{
                "path":"tests/4O_and_3X.jpg",
                "x_count": 3,
                "o_count": 4},
            "Two circles":{
                "path":"tests/two_circles.jpg",
                "x_count": 0,
                "o_count": 2},
            "Nine circles":{
                "path":"tests/nine_circles.jpg",
                "x_count": 0,
                "o_count": 9},
            "Nine crosses":{
                "path":"tests/nine_crosses.jpg",
                "x_count": 9,
                "o_count": 0},
            "Small empty board":{
                "path":"tests/small_empty_board.jpg",
                "x_count": 0,
                "o_count": 0},
            "Small, X=1":{
                "path":"tests/small_one_cross.jpg",
                "x_count": 1,
                "o_count": 0},
            "Small, X=6":{
                "path":"tests/small_six_cross.jpg",
                "x_count": 6,
                "o_count": 0},
            "FullHD, small, O=2, X=1":{
                "path":"tests/fullhd_small_2O_1X.jpg",
                "x_count": 1,
                "o_count": 2},
            "FullHD, small, O=3, X=3":{
                "path":"tests/fullhd_small_3O_3X.jpg",
                "x_count": 3,
                "o_count": 3},
            "Narrow lines, O=1, X=2":{
                "path":"tests/narrow_lines_1O_2X.jpg",
                "x_count": 2,
                "o_count": 1},
    }

    print_header()
    count = 0
    for title in tests:
        test = tests[title]
        image = cv2.imread(test["path"])
        status = []
        try:
            gameboard = Gameboard.detect_game_board(image, debug=False)
            status = gameboard.status()
        except Exception:
            status = []
        x_count = len([pos for pos in status if pos == "X"])
        o_count = len([pos for pos in status if pos == "O"])
        result = "*FAILED*"
        if (x_count == test["x_count"] and o_count == test["o_count"]):
            result = " PASSED "
            count += 1
        print("{0:40} {1:10}(O={2}, X={3})".format(title.upper(), result, o_count, x_count))
    print("\nOK! {0}/{1} tests passed".format(count, len(tests)))

if __name__=="__main__":
    main()