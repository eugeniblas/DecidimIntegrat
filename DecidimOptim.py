##################################################################################################
#                                                                                                #
#   AUTHOR: Marc Serramia                                                                        #
#                                                                                                #
#   versio +1: Eugeni Blas - [Integrated Model: Inclusion of Value alignement]                   #
#                                                                                                #
##################################################################################################

import time
import cplex
import os


class DecidimOptim:
    #This class is able to solve proposal selection problems using both optimisation and "rank and select" methodologies

    def __init__(self):
        self.input = None #The name of the raw data input file
        self.outputName = None #The name of the output file
        self.output = None #The oputput file itself
        self.proposals = [] #The list of proposals
        self.supports = [] #The list of supports of the proposals
        self.costs = [] #The list of the costs of the proposals
        self.values =[] #The list of the values (economic policy) of the proposals
        self.weights = [] #The list of the weights of the criteria(1st pos:citizen satisfaction, 2nd pos: cost (OBSOLETE), 3th pos: value alignement (PARAMETRIZED: w_v = 1- w_s))
        self.budget = None #The maximum budget allowed to spend
        self.info = ""


    def readData(self, dfilepath):
        #Reads raw data from a file
        self.input = open(dfilepath, "r")
        reading = None
        for line in self.input:
            if line[-1] == "\n":
                line = line[:-1]
            if line in ["Proposals", "Supports", "Costs", "Values", "Budget", "Weights"]:
                reading = line
            elif line != "":
                if reading == "Proposals":
                    self.proposals.append(line)
                elif reading == "Supports":
                    self.supports.append(int(line))
                elif reading == "Costs":
                    self.costs.append(int(line))
                elif reading == "Values":
                    self.values.append(float(line))
                elif reading == "Budget":
                    self.budget = int(line)
                elif reading == "Weights":
                    self.weights.append(float(line)) 
        self.input.close()

        self.outputName = dfilepath.replace(".txt", ".lp")
        print(self.outputName)


    def writeLP(self, LPfilename = None, rels = False, values = False):
        #Writes the LP file, the file that the optimiser can read and solve
        if LPfilename:
            self.outputName = LPfilename
        self.output = open(self.outputName, "w")
        if self.budget and self.proposals:
            if (len(self.proposals) == len(self.supports) and len(self.proposals) == len(self.costs) and
                len(self.proposals) == len(self.values)):
                self.output.write("Maximize\n\n")
                self.writeOptFunction()
                self.output.write("\n\nSubject To\n\n")
                self.writeConstraints()
                self.output.write("\nBinaries\n\n")
                self.writeBinaries()
                self.output.write("\nEnd")
            else:
                 "Missing input data"
        else:
            print("No input")
        self.output.close()


    def writeOptFunction(self):
        #Writes the maximisation function of the optimisation process 
        #Implement (version +1) new Integrated Model with value-alignement
        maxSupport = max(self.supports)
        maxValue = max(self.values)        
        w_s = self.weights[0]
        #w_c = self.weights[1]
        #w_v = self.weights[2]
        w_v = 1 - w_s
        for i in range(len(self.supports)):
            supportParameter = (w_s*float(self.supports[i]))/float(maxSupport)             
            #costParameter = (w_c*float(self.costs[i]))/float(self.budget)
            valueParameter = (w_v*float(self.values[i]))/float(maxValue)  
            #parameter = supportParameter + valueParameter         
            if i != 0:
                self.output.write(' + ')
            self.output.write('{0:.8f}'.format(float(supportParameter)) + ' p_' + str(i+1) + ' + ' + 
                              '{0:.8f}'.format(float(valueParameter)) + ' p_' + str(i+1))
            #self.output.write('{0:.8f}'.format(float(parameter)) + ' p_' + str(i+1))
                              
        #                      ' - ' +
        #                      '{0:.8f}'.format(float(costParameter)) + ' p_' + str(i+1))
        #self.output.write(' + ' + str(w_c) + ' y')
       

    def writeConstraints(self):
        #Writes constraints to the LP, that is incompatibilities between proposals, proposal generalisation
        # and budget limitations

        #Selected norms cannot exceed budget
        for i in range(len(self.costs)):
            if i!= 0:
                self.output.write(" + ")
            self.output.write(str(self.costs[i])+ " p_"+str(i+1))
        self.output.write(" <= "+str(self.budget)+"\n")

        #Removed this part (version +1)
        #Minimisation of budget through maximisation of formula and this constraint
        #for i in range(len(self.proposals)):
         #   if i != 0:
          #      self.output.write(' + ')
           # self.output.write('p_' + str(i+1))
        #self.output.write(' - y >= ' + '0\n')
        #for i in range(len(self.proposals)):
         #   if i != 0:
          #      self.output.write(' + ')
           # self.output.write('p_' + str(i+1))
        #self.output.write(' ' + str(-len(self.proposals) - 1) + ' y <= 0\n')


    def writeBinaries(self):
        #Writes the Binaries part in the LP file
        n=1
        for p in self.proposals:
           self.output.write("p_"+str(n)+"\n")
           n += 1
        #self.output.write("y"+ "\n")


    def solve(self, problem_lp = None, problem_sol = None, timeLim = 3600, outputOmega = None, show = False):
        # Receives a LP file and solves it. It exports the answer to a .sol file and also shows it.
        # You can specify the time limit with timeLim.

        if not problem_lp:
            problem_lp = self.outputName
        if not problem_sol:
            problem_sol = self.outputName.replace(".lp", ".sol")

        try:

            m = cplex.Cplex(problem_lp)

            m.parameters.timelimit.set(timeLim)
            start_time = time.time()
            m.solve()
            final_time = time.time() - start_time

            m.solution.write(problem_sol)

            print(100 * '_')
            print('\n')
            print('Solved in ' + str(final_time) + ' seconds.')

            if 'w_v' in m.variables.get_names():
                print('Solved VMPNSPLB problem. Here the results:')
            elif 'y' in m.variables.get_names():
                print('Solved MPNSPLB problem. Here the results:')
            else:
                print('Solved MPNSP problem. Here the results:')

            #y_name = len(m.solution.get_values())-1
            selected = []
            not_selected = []
            spent = 0
            total_support = 0
            total_value = 0 
            ctrlSelect = [] #indicador binari de seleccionat/no seleccionat    
            
                     
            for varName, varValue in enumerate(m.solution.get_values()):
                #although  varValue is a binary variable, sometimes cplex
                # could returns a float 
                if round(varValue) == 1:
                    status = "Accepted"
                    selected.append("p_"+str(varName+1))
                    spent += self.costs[varName]
                    total_support += self.supports[varName]
                    total_value += self.values[varName]    
                    ctrlSelect.append(1)
                else:
                    status = "Rejected"
                    not_selected.append("p_" + str(varName + 1))
                    ctrlSelect.append(0)
                print("p_"+str(varName+1) + ' : ' + status)
            #total_value = float(total_value)/float(maxValue*spent)*100       
            #case omega
            if outputOmega: 
                totalValueEdit = int(total_value*100000)
                line = "w," + str(self.weights[0]) + "," 
                for prop in ctrlSelect:
                    line += str(prop) + ","
                line += str(total_support) + "," + str(totalValueEdit) + ","
                line += str(spent) + "," + str(len(selected)) + "\n"
                outputOmega.write(line)                

            if show:
                self.info += "\n-----------------\nOptimal solution:\n-----------------------------------------------\n\n"
                self.info += "Selected proposals: " + str(selected)+"\n"
                self.info += "Not selected proposals: " + str(not_selected)+"\n"
                self.info += "Number of selected proposals: " + str(len(selected)) +"\n"
                self.info += "Support for selected proposals: " + str(total_support) +"\n"
                self.info += "Value Alignement for selected proposals: " + str(total_value)+"\n"
                self.info += "Cost of selected proposals: " + str(spent) + " (" +str(float(spent)/float(self.budget)*100)+"%)\n"

        except cplex.exceptions.CplexError:
            outputOmega(str(self.weights[0]) + "," + str(0)+"\n")
            print('Sorry')


    def solveNoOptimisation(self, outputOmega = None, show = False):
        #Solves a proposal selection problem with the "rank and select" method with citizen-satisfaction
        wzipped = zip(self.supports, self.proposals, self.costs, self.values)
        #zipped.sort(reverse=True)
        #zipped = sorted(wzipped, key = lambda x : x[0],reverse=True)
        zipped = sorted(wzipped, key = lambda x: (-x[0],x[2]))
        # Experzipped = zip(list(wzipped).sort(reverse=True))
        sortSupports, sortProposals, sortCosts, sortValues = zip(*zipped)
        spent = 0
        total_support = 0
        total_value = 0
        selected = []
        not_selected = []
        ctrlSelect = [] #indicador binari de seleccionat/no seleccionat 
        i = 0
        while i < len(sortProposals) and spent+sortCosts[i] < self.budget:
            selected.append(sortProposals[i])
            total_support += sortSupports[i]
            total_value += sortValues[i]
            spent += sortCosts[i]
            ctrlSelect.append(1)
            i += 1
        while i < len(sortProposals):
            not_selected.append(sortProposals[i])
            ctrlSelect.append(0)
            i += 1
        if outputOmega:
            totalValueEdit = int(total_value*100000)
            line = "s," + "0,"  
            for sup in ctrlSelect:
                line += str(sup) + ","
            line += str(total_support) + "," + str(totalValueEdit) + "," 
            line += str(spent) + "," + str(len(selected)) + "\n"
            outputOmega.write(line)  
        if show:           
            self.info += "\n-----------------\nRank and Select (citizen satisfaction) solution:\n----------------\n\n"            
            self.info += "Selected proposals: "+str(selected)+"\n"
            self.info += "Not selected proposals: "+str(not_selected)+"\n"
            self.info += "Number of selected proposals: " + str(len(selected)) + "\n"
            self.info += "Support for selected proposals: " +str(total_support)+"\n"
            self.info += "Value Alignement for selected proposals: " + str(total_value)+"\n"
            self.info += "Cost of selected proposals: "+str(spent)+" ("+str(float(spent)/float(self.budget)*100)+"%)\n"


    def solveNoOptimisationValue(self, outputOmega=None, show = False):
        #Solves a proposal selection problem with the "rank and select" method method with value-alignement
        i = 0
        listProposals=[]
        for p in self.proposals:            
            listProposals.append(i)
            i += 1
        wzipped = zip(self.supports, self.proposals, self.costs, self.values, listProposals)
        #zipped.sort(reverse=True)
        #zipped = sorted(wzipped, key = lambda x : x[3],reverse=True)
        zipped = sorted(wzipped, key = lambda x: (-x[3],x[2]))
        # Experzipped = zip(list(wzipped).sort(reverse=True))
        sortSupports, sortProposals, sortCosts, sortValues, listProposals = zip(*zipped)

        spent = 0
        total_support = 0
        total_value = 0
        selected = []
        not_selected = []
        ctrlSelect = [] #indicador binari de seleccionat/no seleccionat
        for p in listProposals:
            ctrlSelect.append(0) 
        i = 0
        
        while i < len(sortProposals) and spent+sortCosts[i] < self.budget:
            selected.append(sortProposals[i])
            total_support += sortSupports[i]
            total_value += sortValues[i]
            spent += sortCosts[i]
            ctrlSelect[listProposals[i]]=1
            i += 1
        while i < len(self.proposals):
            not_selected.append(sortProposals[i])
            ctrlSelect[listProposals[i]]=0
            i += 1
        if outputOmega:
            totalValueEdit = int(total_value*100000)
            line = "v," + "0,"  
            for prop in ctrlSelect:
                line += str(prop) + ","
            line += str(total_support) + "," + str(totalValueEdit) + ","  
            line += str(spent) + "," + str(len(selected)) + "\n"
            outputOmega.write(line) 
    
        if show:
            self.info += "\n-----------------\nRank and Select (value alignement) solution:\n--------------------\n\n"
            self.info += "Selected proposals: "+str(selected)+"\n"
            self.info += "Not selected proposals: "+str(not_selected)+"\n"
            self.info += "Number of selected proposals: " + str(len(selected)) + "\n"
            self.info += "Support for selected proposals: " +str(total_support)+"\n"
            self.info += "Value Alignement for selected proposals: " + str(total_value)+"\n"
            self.info += "Cost of selected proposals: "+str(spent)+" ("+str(float(spent)/float(self.budget)*100)+"%)\n"


    def show_info(self):
        print(self.info)

    def erase_info(self):
        self.info = ""

def main():
    problem = DecidimOptim()
    datafile = None
    while not datafile:
        wd = os.getcwd()
        nameFile = input("District Name:\n")
        datafile = wd +"/ExperimentData/"+ nameFile + "/" + nameFile + ".txt"
        print(datafile)
        #datafile = input("Input file for optimisation?\n")
        if datafile.count(".") != 1:
            datafile = None
            print("Incorrect file name, name should be something like file.txt")
    problem.readData(datafile)
    problem.writeLP()
    problem.solve(show = True)
    problem.solveNoOptimisation(show = True)
    problem.solveNoOptimisationValue(show = True)

    problem.show_info()


if __name__ == "__main__":
    main()
