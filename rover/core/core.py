#Writting by Brandon Hawkinson and Timothy Parks
#atlasCore is an interactive shell tool to run, debug and change states of the rover from multiple input sources.

from multiprocessing import Pool

def f(x) : 
    return x*x

if __name__ == '__main__':
    p = Pool(5)
    print(p.map(f, [1,2,3]))
    