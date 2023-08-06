import cmath
class complex_polar:
    def __init__(self, *args):
        if len(args) == 2:
            self.radius = args[0]
            self.angle = args[1]

        if len(args) == 1:
            self.radius = cmath.polar(args[0])[0]
            self.angle = cmath.polar(args[0])[1]

    def to_normal(self):
        return complex(real=self.radius*cmath.cos(self.angle),imag=self.radius*cmath.sin(self.angle))



    def __add__(self, other):
        #add 2 complex polar numbers
        if isinstance(other, self.__class__):
            return complex_polar(complex(
                    real = self.radius*cmath.cos(self.angle) + other.radius*cmath.cos(other.angle),
                    imag = self.radius*cmath.sin(self.angle) + other.radius*cmath.sin(other.angle)
            ))
        #add 2 complek polar and float or int
        elif isinstance(other,int) or isinstance(other,float):
            return complex_polar(complex(
                real=self.radius * cmath.cos(self.angle) + float(other),
                imag=self.radius * cmath.sin(self.angle)
            ))
        #exception
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __radd__(self, other):
        # add 2 complex polar numbers
        if isinstance(other, self.__class__):
            return complex_polar(complex(
                real=self.radius * cmath.cos(self.angle) + other.radius * cmath.cos(other.angle),
                imag=self.radius * cmath.sin(self.angle) + other.radius * cmath.sin(other.angle)
            ))
        # add 2 complek polar and float or int
        elif isinstance(other, int) or isinstance(other, float):
            return complex_polar(complex(
                real=self.radius * cmath.cos(self.angle) + float(other),
                imag=self.radius * cmath.sin(self.angle)
            ))
        # exception
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __sub__(self, other):
        #add 2 complex polar numbers
        if isinstance(other, self.__class__):
            return complex_polar(complex(
                    real = self.radius*cmath.cos(self.angle) - other.radius*cmath.cos(other.angle),
                    imag = self.radius*cmath.sin(self.angle) - other.radius*cmath.sin(other.angle)
            ))
        #add 2 complek polar and float or int
        elif isinstance(other,int) or isinstance(other,float):
            return complex_polar(complex(
                real=self.radius * cmath.cos(self.angle) - float(other),
                imag=self.radius * cmath.sin(self.angle)
            ))
        #exception
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __rsub__(self, other):
        #add 2 complex polar numbers
        if isinstance(other, self.__class__):
            return complex_polar(complex(
                    real = other.radius*cmath.cos(other.angle) - self.radius*cmath.cos(self.angle),
                    imag = other.radius*cmath.sin(other.angle) - self.radius*cmath.sin(self.angle)
            ))
        #add 2 complek polar and float or int
        elif isinstance(other,int) or isinstance(other,float):
            return complex_polar(complex(
                real = float(other) - self.radius * cmath.cos(self.angle),
                imag = -(self.radius * cmath.sin(self.angle))
            ))
        #exception
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __mul__(self, other):
        # add 2 complex polar numbers
        if isinstance(other, self.__class__):
            return complex_polar(
                self.radius * other.radius,
                self.angle + other.angle
            )
        # add 2 complek polar and float or int
        elif isinstance(other, int) or isinstance(other, float):
            return complex_polar(
                self.radius * float(other),
                self.angle
            )
        # exception
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __rmul__(self, other):
        # add 2 complex polar numbers
        if isinstance(other, self.__class__):
            return complex_polar(
                self.radius*other.radius,
                other.angle
            )
        # add 2 complek polar and float or int
        elif isinstance(other, int) or isinstance(other, float):
            return complex_polar(
                self.radius * float(other),
                self.angle
            )
        # exception
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __truediv__(self, other):
        # add 2 complex polar numbers
        if isinstance(other, self.__class__):
            return complex_polar(
                self.radius / other.radius,
                self.angle - other.angle
            )
        # add 2 complek polar and float or int
        elif isinstance(other, int) or isinstance(other, float):
            return complex_polar(
                self.radius / float(other),
                self.angle
            )
        # exception
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __rtruediv__(self, other):
        # add 2 complex polar numbers
        if isinstance(other, self.__class__):
            return complex_polar(
                self.radius / other.radius,
                other.angle - self.angle
            )
        # add 2 complek polar and float or int
        elif isinstance(other, int) or isinstance(other, float):
            return complex_polar(
                self.radius / float(other),
                -self.angle
            )
        # exception
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __pow__(self, num):
        if isinstance(num, int) or isinstance(num, float):
            return complex_polar(pow(self.radius,num),self.angle*num)

    def __str__(self):
        return str(self.radius) + "exp{" + str(self.angle) + "}"