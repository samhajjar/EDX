# Problem Set 8: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab
#from ps8b_precompiled_27 import *
''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between [0,1])        
        clearProb: Maximum clearance probability (a float between [0,1]).
        """
        assert maxBirthProb<=1 and maxBirthProb>=0, 'Probability should be in range [0,1]'
        assert clearProb<=1 and clearProb>=0, 'Probability should be in range [0,1]'
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        return random.random() < self.clearProb

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.getMaxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() < ( self.getMaxBirthProb() * (1 - popDensity) ):
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        else:
            raise NoChildException



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        assert type(maxPop)==int, 'maxPop should be an integer'
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        tempVirusList = self.viruses[:]
         
        for tempVirus in tempVirusList: #scan the temp list
            if tempVirus.doesClear():
                #print 'Virus died'
                self.viruses.remove(tempVirus) #remove from the original list
        #calculate the popDensity on the "survived" viruses
        popDensity = len(self.viruses)/float(self.maxPop)
        #copy again the "survived" viruses to a new list
        tempVirusList = self.viruses[:]
        #for each virus, run the reproduce method
        for tempVirus in tempVirusList:
            try:
                self.viruses.append(tempVirus.reproduce(popDensity))
            except NoChildException:
                continue
        return self.getTotalPop()

#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses=100, maxPop=1000, maxBirthProb=0.1, clearProb=0.05,
                          numTrials=100):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    #Instantiate the viruses first, the patient second
    viruses= [ SimpleVirus(maxBirthProb, clearProb) for i in range(numViruses) ]
    patient = Patient(viruses, maxPop)
    #Execute the patient.update method 300 times for 100 trials
    steps = 300
    countList = [0 for i in range(300)]
    for trial in range(numTrials):
        for timeStep in range(steps):
            countList[timeStep] += patient.update()
    avgList = [ countList[i]/float(numTrials) for i in range(steps) ]
    #Plot a diagram with xAxis=timeSteps, yAxis=average virus population
    xAxis = [ x for x in range(steps) ]
    pylab.figure()
    pylab.plot(xAxis, avgList, 'ro', label='Simple Virus')
    pylab.xlabel('Number of elapsed time steps')
    pylab.ylabel('Average size of the virus population')
    pylab.title('Virus growth in a patient without the aid of any drag')
    pylab.legend()
    pylab.show()


#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        assert mutProb<=1 and mutProb>=0, 'mutProb should be in range [0,1]'
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances.keys()

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances.get(drug,False)


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability: self.getMaxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb, clearProb, and mutProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but NOT
        srinol, and self.mutProb is 0.1, then there is a 10% chance
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb, clearProb and mutProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        self.offResistances = {}

        for r in activeDrugs:
            if self.resistances.get(r,0)==0 or self.resistances.get(r,0)==False :
                raise NoChildException

        if random.random() < self.getMaxBirthProb() * (1 - popDensity):
            for res in self.resistances.keys():
                if random.random() < 1-self.mutProb:
                    self.offResistances[res]=self.resistances[res]
                else:
                    self.offResistances[res]=not( self.resistances[res] )
            return ResistantVirus(self.maxBirthProb, self.clearProb, self.offResistances, self.mutProb)
        else:
            raise NoChildException

            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.drugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        counter = 0
        for virus in self.viruses:
            flag = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    flag = False
                    break
            if flag:
                counter += 1
        return counter


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        tempVirusList = self.viruses[:]
         
        for tempVirus in tempVirusList: #scan the temp list
            if tempVirus.doesClear():
                #print 'Virus died'
                self.viruses.remove(tempVirus) #remove from the original list
        #calculate the popDensity on the "survived" viruses
        popDensity = len(self.viruses)/float(self.maxPop)
        #Update the temp list with the "survived" viruses
        tempVirusList = self.viruses[:]
        #for each virus, run the reproduce method
        for tempVirus in tempVirusList:
            try:
                self.viruses.append( tempVirus.reproduce(popDensity, self.drugs) )
            except NoChildException:
                continue
        return self.getTotalPop()



#
# PROBLEM 5
#
def simulationWithDrug(numViruses=100, maxPop=1000, maxBirthProb=0.1, clearProb=0.05, resistances={'guttagonol': False},
                       mutProb=0.005, numTrials=100):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    steps = 300
    countListA = [0.0 for i in range(steps)]
    countListB = [0.0 for i in range(steps)]
    #Execute the TreatedPatient.update methods 300 times total
    #(aka 150 time-steps w/o drug and another 150 with drug) for 100 trials
    for trial in range(numTrials):
        #Instantiate the Resistant Viruses first, TreatedPatient second
        viruses = [ ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(numViruses) ]
        patient = TreatedPatient(viruses, maxPop)
        for timeStep in range(steps):
            if timeStep==150:
                patient.addPrescription('guttagonol')
            countListA[timeStep] += patient.update()
            countListB[timeStep] += patient.getResistPop(['guttagonol'])
            
    avgListA = [ countListA[i]/numTrials for i in range(steps) ]
    avgListB = [ countListB[i]/numTrials for i in range(steps) ]
    #Plot a diagram with xAxis=timeSteps, yAxis=average virus population
    pylab.figure()
    pylab.plot(range(steps), avgListA, 'ro', label='Virus w/o drug')
    pylab.plot(range(steps), avgListB, 'bo', label='Virus under drug')
    pylab.title('Virus growth in a patient without and with the aid of guttagonol')
    pylab.xlabel('Time step')
    pylab.ylabel('Average size of the virus population')
    pylab.legend(loc=0)
    pylab.show()

##v1 = ResistantVirus(1.0, 0.0, {'a':True, 'b':True, 'c':True, 'd':True}, 0.0)
##v2 = ResistantVirus(1.0, 0.0, {'a':True, 'b':True, 'c':True, 'd':False}, 0.0)
##v3 = ResistantVirus(1.0, 0.0, {'a':True, 'b':True, 'c':True, 'd':True}, 0.0)
##p = TreatedPatient([v1], 500)
##p.addPrescription('a')
##p.addPrescription('b')
##p.addPrescription('c')
##p.addPrescription('d')

##virus = ResistantVirus(1.0, 0.0, {}, 1.0)
##pat = TreatedPatient([virus], 10)
