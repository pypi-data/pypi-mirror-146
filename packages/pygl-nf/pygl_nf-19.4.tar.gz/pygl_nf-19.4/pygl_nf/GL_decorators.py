import GL
import colorama


def T_Text_(function):
    def Wraper(*args):
        if type(args[1])!=GL.Text_:
                raise ValueError(colorama.Fore.RED+'One of the arguments must be of type (Text_)'+colorama.Fore.RESET)
        return function(*args)
    return Wraper