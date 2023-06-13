##################################################################################################
#                                                                                                #
#   AUTHOR: Marc Srramia                                                                         #
#                                                                                                #
#   version +1: Eugeni Blas [Adaptacó del programa DecidimOptim per poder fer la                 #
#               Comprovació Simulació Casos per Enquesta Pressupostos Participatius IMOP]        #
#                                                                                                #
##################################################################################################

import time
import cplex

class SimulacioDecidimOptimAudit:
    #This class is able to solve proposal selection problems using both optimisation and "rank and select" methodologies

    def __init__(self):
        self.input = None #The name of the raw data input file
        self.outputName = [] #The name of the output file
        for i in range(120):
            self.outputName.append("ExperimentData/Simulacio/Simulacio" + str(i) + ".lp")
        self.output = []
        for i in range(120):
            self.output.append("")
        self.proposals = [] #The list of proposals
        self.supports = [] #The list of supports of the proposals
        self.costs = [] #The list of the costs of the proposals
        self.weights = [] #The list of the weights of the criteria(1st pos:community opinion, 2nd pos: cost)
        self.budget = None #The maximum budget allowed to spend
        self.info = ""
        self.select = []
        self.ctrlSelect =[]
        self.indexCall = 0
         



    def inputData(self, dfilepath,select=None, ctrlSelect=None, indexCall=None):
        self.select = select
        self.ctrlSelect = ctrlSelect
        self.indexCall = indexCall
        costs = [8.5,7.25,7,6.5,5.5,5.25,5,4.75,4.5,3.25]
        self.proposals = ["p1","p2","p3","p4","p5","p6","p7","p8","p9","p10"]
        self.supports = [15245,10223,8432,4044,1950,970,481,235,112,53]
        for i in select:
            self.costs.append(costs[i-1])
        self.weights= [1,0]
        self.budget=23

        self.input = open(dfilepath, "r")
        self.input.close()
        replace = str(indexCall) + ".lp"
        #self.outputName = dfilepath.replace(".txt", replace)
        print("++++++" + str(self.outputName[self.indexCall]))
        

    def readData(self, dfilepath):
        #Reads raw data from a file

        self.input = open(dfilepath, "r")
        reading = None
        for line in self.input:
            if line[-1] == "\n":
                line = line[:-1]
            if line in ["Proposals", "Supports", "Costs", "Budget", "Weights"]:
                reading = line
            elif line != "":
                if reading == "Proposals":
                    self.proposals.append(line)
                elif reading == "Supports":
                    self.supports.append(int(line))
                elif reading == "Costs":
                    self.costs.append(int(line))
                elif reading == "Budget":
                    self.budget = int(line)
                elif reading == "Weights":
                    self.weights.append(float(line))
        self.input.close()
        replace = str(self.indexCall) + ".lp"
        #self.outputName = dfilepath.replace(".txt", ".lp")
        self.outputName = dfilepath.replace(".txt", replace)

    def writeLP(self, LPfilename = None, rels = False, values = False):
        #Writes the LP file, the file that the optimiser can read and solve
        if LPfilename:
            self.outputName = LPfilename
        self.output[self.indexCall] = open(self.outputName[self.indexCall], "w")
        print("+++2+++" +str(self.outputName[self.indexCall]))
        if self.budget and self.proposals:
            if len(self.proposals) == len(self.supports) and len(self.proposals) == len(self.costs):
                self.output[self.indexCall].write("Maximize\n\n")
                self.writeOptFunction()
                self.output[self.indexCall].write("\n\nSubject To\n\n")
                self.writeConstraints()
                self.output[self.indexCall].write("\nBinaries\n\n")
                self.writeBinaries()
                self.output[self.indexCall].write("\nEnd")
            else:
                 "Missing input data"
        else:
            print("No input")
        self.output[self.indexCall].close()

    def writeOptFunction(self):
        #Writes the maximisation function of the optimisation process

        maxSupport = max(self.supports)
        w_s = self.weights[0]
        w_c = self.weights[1]
        for i in range(len(self.supports)):
            supportParameter = (w_s*float(self.supports[i]))/float(maxSupport)
            costParameter = (w_c*float(self.costs[i]))/float(self.budget)
            if i != 0:
                self.output[self.indexCall].write(' + ')
            #self.output.write('{0:.8f}'.format(float(supportParameter)) + ' p_' + str(i+1) + ' - ' + '{0:.8f}'.format(float(costParameter)) + ' p_' + str(i+1))
            self.output[self.indexCall].write('{0:.8f}'.format(float(supportParameter)) + ' p_' + str(i+1))
        #self.output.write(' + ' + str(w_c) + ' y')


    def writeConstraints(self):
        #Writes constraints to the LP, that is incompatibilities between proposals, proposal generalisation
        # and budget limitations
        #Selected norms cannot exceed budget
        for i in range(len(self.costs)):
            if i!= 0:
                self.output[self.indexCall].write(" + ")
            self.output[self.indexCall].write(str(self.costs[i])+ " p_"+str(i+1))
        self.output[self.indexCall].write(" <= "+str(self.budget)+"\n")

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
           self.output[self.indexCall].write("p_"+str(n)+"\n")
           n += 1
        #self.output.write("y"+ "\n")

    def solve(self, problem_lp = None, problem_sol = None, timeLim = 3600, outputSup = None, outputCost = None, outputNum = None, show = False):
        # Receives a LP file and solves it. It exports the answer to a .sol file and also shows it.
        # You can specify the time limit with timeLim.
        returnOK ="DONT WORK+++"
        if not problem_lp:
            problem_lp = self.outputName[self.indexCall]
        if not problem_sol:
            problem_sol = self.outputName[self.indexCall].replace(".lp", ".sol")

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
            ctrlSelectCplex = [0,0,0,0,0,0,0,0,0,0]
            i = 0
            for varName, varValue in enumerate(m.solution.get_values()):
                #if varName != y_name:
                if varValue == 1:
                    status = "Accepted"
                    selected.append("p_"+str(varName+1))
                    spent += self.costs[varName]
                    total_support += self.supports[varName]
                    ctrlSelectCplex[i] = 1
                else:
                    status = "Rejected"
                    not_selected.append("p_" + str(varName + 1))
                print("p_"+str(varName+1) + ' : ' + status)
                i += 1

            
            if self.ctrlSelect == ctrlSelectCplex:
                self.Ok = 1
                print("+OK++++++++++++++++++")
                returnOK = "OK"
            else:    
                self.Ok = 0
                print("+NOK++++++++++++++++++")
                print(str(self.ctrlSelect)+str(ctrlSelectCplex))
                returnOk = "NOK " + str(ctrlSelectCplex)

            if outputSup and outputCost and outputNum:
                outputSup.write(str(self.budget) + "," + str(total_support)+"\n")
                outputCost.write(str(self.budget) + "," + str(spent)+"\n")
                outputNum.write(str(self.budget) + "," + str(len(selected)) + "\n")


            if show:
                self.info += "\n-----------------\nOptimal solution:\n-----------------\n\n"
                self.info += "Selected proposals: " + str(selected)+"\n"
                self.info += "Not selected proposals: " + str(not_selected)+"\n"
                self.info += "Number of selected proposals: " + str(len(selected)) + "\n"
                self.info += "Support for selected proposals: " + str(total_support)+"\n"
                self.info += "Cost of selected proposals: " + str(spent)+" ("+str(float(spent)/float(self.budget)*100)+"%)\n"

        except cplex.exceptions.CplexError:
            outputSup.write(str(self.budget) + "," + str(0)+"\n")
            outputCost.write(str(self.budget) + "," + str(0)+"\n")
            outputNum.write(str(self.budget) + "," + str(0) + "\n")
            print('Sorry')

        return(returnOK)

    #def solveNoOptimisation(self, outputSup = None, outputCost = None, outputNum = None, show = False):
        #Solves a proposal selection problem with the "rank and select" method

    #    wzipped = zip(self.supports, self.proposals, self.costs)
        # zipped.sort(reverse=True)
    #    zipped = sorted(wzipped, key = lambda x : x[0],reverse=True)
        # Experzipped = zip(list(wzipped).sort(reverse=True))
    #    self.supports, self.proposals, self.costs = zip(*zipped)
    #    spent = 0
    #    total_support = 0
    #    selected = []
    #    not_selected = []
    #    i = 0
    #    while i < len(self.proposals) and spent+self.costs[i] < self.budget:
    #        selected.append(self.proposals[i])
    #        total_support += self.supports[i]
    #        spent += self.costs[i]
    #        i += 1
    #    while i < len(self.proposals):
    #        not_selected.append(self.proposals[i])
    #        i += 1
    #    if outputNum and outputCost and outputSup:
    #        outputSup.write(str(self.budget)+","+str(total_support)+"\n")
    #        outputCost.write(str(self.budget)+","+str(spent)+"\n")
    #        outputNum.write(str(self.budget) + "," + str(len(selected)) + "\n")
    #    if show:
    #        self.info += "\n----------------\nR&S (citizen satisfaction) solution:\n----------------\n\n"
    #        self.info += "Selected proposals: "+str(selected)+"\n"
    #        self.info += "Not selected proposals: "+str(not_selected)+"\n"
    #        self.info += "Number of selected proposals: " + str(len(selected)) + "\n"
    #        self.info += "Support for selected proposals: "+str(total_support)+"\n"
    #        self.info += "Cost of selected proposals: "+str(spent)+" ("+str(float(spent)/float(self.budget)*100)+"%)\n"

    def show_info(self):
        print(self.info)

    def erase_info(self):
        self.info = ""

def main():
    problem = SimulacioDecidimOptimAudit()
    datafile = None
    while not datafile:
        datafileW = input("Input file for optimisation?\n")
        datafile = "ExperimentData/" + datafileW + "/" + datafileW + ".txt"
        if datafile.count(".") != 1:
            datafile = None
            print("Incorrect file name, name should be something like file.txt")
    #problem.readData(datafile)
    problem.inputData(datafile,[8,5,7,9,4,10,6,3,1,2],[1,1,1,1,0,1,0,0,0,0],1) #only for testing this program
    problem.writeLP()
    problem.solve(show = True)
    #problem.solveNoOptimisation(show = True)
    problem.show_info()

if __name__ == "__main__":
    main()
