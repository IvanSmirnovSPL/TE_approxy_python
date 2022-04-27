def double2str(a):
    return str('%.3f' % a)



def make_latex_table(err_dots, err_scale, path):
    f = open(path, 'w')
    f.write(r'\begin{table}[h!]' + '\n')
    f.write(r'\begin{tabular}{|c|c|c|}' + '\n')
    f.write(r'\centering' + '\n')
    f.write(r'\hline' + '\n')
    f.write(r'& $1 / \sqrt{\text{dots number}}$ & $1 / \text{scale}$ \\ \hline' + '\n')
    f.write(r'$e_1$ &' +  double2str(err_dots[0])  + '&' +  double2str(err_scale[0]) + r'\\ \hline' + '\n')
    f.write(r'$e_2$ &' +  double2str(err_dots[1])  + '&' +  double2str(err_scale[1]) + r'\\ \hline' + '\n')
    f.write(r'$e_3$ &' +  double2str(err_dots[2])  + '&' +  double2str(err_scale[2]) + r'\\ \hline' + '\n')
    f.write(r'\end{tabular}' + '\n')
    f.write(r'\end{table}' + '\n')
    f.close()