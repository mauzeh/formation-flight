def get_pi():

    i = 0
    pi_i = 0
    position = 0
    decimal = 0

    while True:

        if i % 2:
            pi_i = pi_i - 4 * (1 / float(1 + 2*i))
        else:
            pi_i = pi_i + 4 * (1 / float(1 + 2*i))

        decimal_old = decimal
        decimal = str(pi_i)[position]
        
        if decimal == decimal_old or decimal == '.':
            position = position + 1
            decimal = '*'

        if position >= 7:
            break
        
        i = i + 1
    
    return pi_i

print get_pi()