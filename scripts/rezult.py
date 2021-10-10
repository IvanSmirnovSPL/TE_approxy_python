import error
import matplotlib.pyplot as plt

class REZULT:

    def __init__(self, num):
        self.num = num
        self.doc = open('../rez/doc_' + str(self.num) + '.txt', 'w')
        self.err_f = open('../rez/err_' + str(self.num) + '.txt', 'w')
        self.err_f.write('time e1 e2 e3' + '\n')
        self.err = error.ERROR()

    def draw(self, x, z1, z2, n, N):
        # z1 - numeric, z2 - analitic
        # T - period of saving
        T = 10
        if n % T == 0:
            plt.scatter(x, z1, label='numeric in '
                                 + str('%.4f' % ((n - 1) / (N - 1))) + ' seconds')
            plt.scatter(x, z2, label='analitic in '
                                 + str('%.4f' % ((n - 1) / (N - 1))) + ' seconds')
            plt.xlabel('x')
            plt.ylabel('function')
            plt.grid(True)
            plt.legend()
            plt.savefig('../rez/' + 'x_'+str(self.num)+'_'+str(n // T) + '.png')
            plt.close()


    def upgrade_error(self, n, N, a, b):
        self.err.calc_error(a, b)
        self.err_f.write(str("{:10.4e}".format((n - 1) / (N - 1))) + ' '
                + str("{:10.4e}".format(self.err.e1[-1])) + ' '
                + str("{:10.4e}".format(self.err.e2[-1])) + ' '
                + str("{:10.4e}".format(self.err.e3[-1])) + '\n')

    def finish(self):
        self.doc.close()
        self.err_f.close()