import random

class CircuitGenerator(object):

    

    """ Generates a string of 3*number_of_gates length number representing gate types and position in a quantum circuit """

    def __init__(self, number_of_gates):
        self.integer_string = []
        self.number_of_gates = number_of_gates
        self.string_length = number_of_gates*3

    def generateGateString(self):
        # Returns a randomly generated string representation of given number of qbits

        for i in range(self.string_length):
            if(i%3==0):
                self.integer_string.append(random.randrange(0,5))
            else:
                self.integer_string.append(random.randrange(0,3))

        for i in range (0, int(self.string_length/3)):
            int_index = i*3

            if(self.integer_string[int_index]==0 and self.integer_string[int_index+1] == self.integer_string[int_index + 2]):
                if(self.integer_string[int_index+1]== 0):
                    self.integer_string[int_index+1]=random.randrange(1,3)
                elif (self.integer_string[int_index+1]== 1):
                    self.integer_string[int_index+2]=0 # TODO - hardcoded
                elif (self.integer_string[int_index+1]== 2):
                    self.integer_string[int_index+2]=random.randrange(0,2)
        print(self.integer_string)


        return self.integer_string

    def generateCircuitFromString(self, circuit):
        # Parsing integer string and converting it to gates

        for i in range (0, int(self.string_length/3)):
            gate_index = i*3

            a=self.integer_string[gate_index]
            b=self.integer_string[gate_index+1]
            c=self.integer_string[gate_index+2]

            if (a==0):
                circuit.cx(b,c)
            elif (a==1):
                circuit.x(b)
            elif (a==2):
                circuit.h(b)
            elif (a==3):
                circuit.y(b)
            elif (a==4):
                circuit.z(b)
            

        circuit.measure(0,0)




