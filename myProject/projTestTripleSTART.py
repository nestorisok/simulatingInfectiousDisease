import numpy as np
import random
import matplotlib.pyplot as plt

from csv import writer

def run_simulation(): # GRID_SIZE(X*Y), numOfPatients, initInfectedNum
    
    # Grid 
    GRID_SIZE = 100
    grid = [[np.nan for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] # np.nan for visual (make white square in heatmap)

    # Patient Class
    class Patient:

        def __init__(self, patientNum, sick, posX, posY):
            self.patientNum = patientNum
            self.sick = sick
            self.posX = posX
            self.posY = posY

        def move(self): # 8 Directional movement
            dir =   [(-1,0), (1,0), (0,-1),(0,1), # up/down L/R
                    (-1,-1), (-1,1), (1,-1), (1,1)] # diag
            random.shuffle(dir)
            for nx, ny in dir:
                new_x = self.posX + nx
                new_y = self.posY + ny
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and np.isnan(grid[new_x][new_y]):
                    grid[self.posX][self.posY] = np.nan
                    grid[new_x][new_y] = self.patientNum
                    self.posX = new_x
                    self.posY = new_y
                    break

        def infect_near(self):  # 8 Directional movement
            infected = 0        # how many Patient[N] infected
            dir =   [(-1,0), (1,0), (0,-1),(0,1), # up/down L/R
                    (-1,-1), (-1,1), (1,-1), (1,1)] # diag
            for nx, ny in dir:
                near_x = self.posX + nx
                near_y = self.posY + ny
                if 0 <= near_x < GRID_SIZE and 0 <= near_y < GRID_SIZE and not np.isnan(grid[near_x][near_y]):  # check if in grid/isn't empty
                    nbr = grid[near_x][near_y]      # grabs patient num from list
                    if not patient_list[nbr].sick:
                        patient_list[nbr].sick = True
                        infected += 1
            
            return infected     # returns "     "
        
        

 #   Populate Grid w people
    MAX_PATIENTS = 6000
    tot_infected = 0
    new_infected = 0

    patient_list = []
    for i in range(MAX_PATIENTS):
        while True:
            x = random.randint(0, GRID_SIZE-1)
            y = random.randint(0, GRID_SIZE-1)
            if np.isnan(grid[x][y]):
                patient = Patient(patientNum = i, sick = False, posX = x, posY = y)     # init new patient and add patient to list
                patient_list.append(patient)
                grid[x][y] = i      # grid[x][y] holds patient num
                break


    #   Display Grid
    def plot_grid():
        display_grid = np.full((GRID_SIZE, GRID_SIZE), np.nan)
    
        for el in patient_list:     # go through list and either 1/0 if sick or not at Grid[X][Y]
            if el.sick:
                display_grid[el.posX][el.posY] = 1
            else:
                display_grid[el.posX][el.posY] = 0


        plt.imshow(display_grid, cmap='coolwarm', interpolation='nearest', extent=[0, GRID_SIZE, 0, GRID_SIZE])
        plt.axis([0, GRID_SIZE, 0, GRID_SIZE])
        plt.title(f"Step: {timestep}\nNew: {new_infected}, Total: {tot_infected}")
        plt.pause(.2)
        plt.clf()



    # Init Patient[0] with sickness
    patient_list[0].sick = True
    tot_infected += 1
    new_infected += 1
    timestep = 0

    patient_list[1].sick = True
    tot_infected += 1
    new_infected += 1

    patient_list[2].sick = True
    tot_infected += 1
    new_infected += 1

    timestep = 0

    # Newly infected and Total infected files
    newlyFile = 'newlyInfTRIPLE.csv'
    totFile = 'totInfTRIPLE.csv'

    new_val_arr = []    # Arr for newlyInfected[Timestep] = new_infected
    tot_inf_arr = []    # Arr for totalInfected[Timestep] = tot_infected

    while(tot_infected < MAX_PATIENTS):     # While the totalInfected <

        
        plot_grid()  # Show the current grid state
        #print(f"Step {timestep}(Total infected: {tot_infected}),(New infected: {new_infected})")       # 

        new_val_arr.append(new_infected)
        # Writes Total Infected to CSV
        tot_inf_arr.append(tot_infected)
        

        new_infected = 0

        for el in patient_list:
            el.move()

        
        for el in patient_list:
            if el.sick:
                new_infected += el.infect_near()


        tot_infected += new_infected

        timestep += 1


    #print(f"Step {timestep}(Total infected: {tot_infected}),(New infected: {new_infected})")
    plot_grid()


    new_val_arr.append(new_infected)
    tot_inf_arr.append(tot_infected)
        

    # Add last row to file
    with open(totFile, 'a', newline= '') as csvfile:
        csv_writer = writer(csvfile)
        csv_writer.writerow(tot_inf_arr)

    with open(newlyFile, 'a', newline = '') as csvfile:
        csv_writer = writer(csvfile)
        csv_writer.writerow(new_val_arr)


run_simulation()