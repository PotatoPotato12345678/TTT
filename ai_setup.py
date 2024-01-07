from tictactoe.utils import load_checkpoint
from tictactoe.model import Model
from tictactoe.environment import TicTacToe
import time

def data_delivery_change():
    path ="data_delivery.txt"
    elem =['']
    while True:
        time.sleep(1)
        with open(path) as f:
            l = f.read().replace("[","").replace("]","").replace("\'",'').replace(' ','').split(",")

            if elem == l or len(l)==1:
                continue;
            elem = l

            pos = str(pos_decision(elem))
        with open(path, mode='w') as f:
            f.write(pos)
            elem = []
            elem.append(pos)

def pos_decision(origBoard):
    args = {"field_size":4,"num_hidden_units":128,"num_layers":1,"dropout_probability":0.0,"algorithm":'deep_q_learning',"model_name":'agent_a'}
    model = Model(args=args)
    load_checkpoint(model=model, args=args)
    env = TicTacToe(size=args["field_size"])
    pos = env.play(model=model,origboard=origBoard)

    """
    upload pos variable to localhost
    """
    return pos

if __name__=="__main__":
    data_delivery_change()