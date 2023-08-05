import os 
import colorama


def T_Text_(function):
    import GL
    def Wraper(*args):
        if type(args[1])!=GL.Text_:
                os.system('cls')
                raise ValueError(colorama.Fore.RED+'One of the arguments must be of type (Text_)'+colorama.Fore.RESET)
        return function(*args)
    return Wraper

def T_Mouse_(function):
    import GL
    def Wraper(*args):
        if type(args[1])!=GL.Sub_events_.Mouse_init:
                os.system('cls')
                raise ValueError(colorama.Fore.RED+'One of the arguments must be of type (Mouse_)'+colorama.Fore.RESET)
        return function(*args)
    return Wraper
