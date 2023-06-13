##################################################################################################
#                                                                                                #
#   AUTHOR: Marc Serramia                                                                        #
#                                                                                                #
#   versio +1: Eugeni Blas - [Integrated Model: Inclusion of Value alignement]                   #
#                                                                                                #
##################################################################################################

import os

class DecidimProblemBuilder:
    #Given a range of budgets this class will build all the LP files for the proposal selection problems with those
    #budgets

    def __init__(self, original, weights, buildpath):
        #self.minbudget = minb #The minimum budget to start building LPs
        #self.maxbudget = maxb #The maximum budget to stop building LPs
        #self.increment = increment #The subsequent increment of budget between LP builds
        self.originalPath = original #Path to the original
        self.buildPath = buildpath #Directory for the generated files
        self.names = [] #List to be filled with the filenames of the generated LP files
        self.weights = weights #Problem weights to use optionaly (1st pos:citizen satisfaction, 2nd pos: cost (OBSOLETE), 3th pos: value alignement)

    
    def build(self):
        #This method builds each LP file, it takes an original LP file and only changes the weights  
        originalFile = open(self.originalPath, "r")
        fileContent = originalFile.readlines()
        originalFile.close()
        #budgets = list(range(self.minbudget, self.maxbudget, self.increment))   
        #budgets.append(self.maxbudget)
        self.buildPath = self.buildPath+self.originalPath.split("/")[-1]
        for omega in range(11):
            fileContent[2] = str(omega/10) +"\n"
            newfilename = self.buildPath.replace(".txt", "omega"+str(omega)+".txt")
            self.names.append(newfilename)
            newfile = open(newfilename, "w+")
            for line in fileContent:
                newfile.write(line)
            newfile.close()


    def getFileNames(self):
        return self.names


def main():
    wd = os.getcwd()
    folder = wd +"/ExperimentData/"+input("District Name:\n")+"/"
    original = folder + folder.split("/")[-2] + ".txt"
    buildpath =folder+"Data/"
    builder = DecidimProblemBuilder(original,[0.5, 0, 0.5], buildpath)
    builder.build()


if __name__ == "__main__":
        main()