__author__ = 'Janek Krukowski'
from algo import *

def main():
    p1 = ProcManagerFirst(n_proc=10)
    p2 = ProcManagerSecond(n_proc=10)
    p3 = ProcManagerThird(n_proc=10)
    p1.run()
    p2.run()
    p3.run()
    print p1.avg(), p2.avg(), p3.avg()

if __name__ == "__main__":
    main()