import random
import math
import numpy as np
from functools import reduce

successful_mutations = 0
total_mutations = 0
todo = 'divide'
deviation_constant = 0.8

def square_sum(vetor):
  sum = 0
  for (x, desvio) in vetor:
    sum += x*x
  return sum

def cos_sum(vetor):
  sum = 0
  for (x, desvio) in vetor:
    sum += math.cos(math.pi*2*x)
  return sum

def calculate_population_fitness(population):
  result = []
  for i in population:
    result.append(calculate_fitness(i))
  return result

def calculate_fitness(individual):
  term1 = (-20)* math.exp( (-0.2) *math.sqrt(square_sum(individual)/len(individual)) )
  term2 = -math.exp(cos_sum(individual)/len(individual))
  y =  term2 + math.exp(1) +term1 + 20.0 
  return (individual,y)

def get_constant():
  global total_mutations, successful_mutations, todo
  if total_mutations > 0 and successful_mutations / total_mutations < 0.2:
    todo = 'multiply'
  elif total_mutations > 0 and successful_mutations / total_mutations > 0.2:
    todo = 'divide'
  else:
    todo = 'keep'

def mutate(population): #1.899744051
  global todo, deviation_constant, successful_mutations, total_mutations
  new_population = []
  get_constant()
  successful_mutations = 0
  total_mutations = 0
  roleta = parent_selection(population)
  while(len(new_population) < 7 * len(population)):
    random_idx = spin_wheel(roleta, random.random())
    (parent_feature, parent_fitness) = population[random_idx]
    child = parent_feature[:]
    vector_mean = calculate_mean(parent_feature,0)
    order_of_greatness = math.floor(math.log(abs(vector_mean), 10))
    for idx, (feature, std_deviation) in enumerate(parent_feature):
      t = 1/pow(len(parent_feature), 0.5)
      t_line = 1/pow((2*pow(len(parent_feature), 0.5)), 0.5)
      new_std_deviation =  abs(std_deviation * math.exp((t * np.random.normal(0, 1)) + (t_line * np.random.normal(0,1))))
      if (order_of_greatness <= -4):
        new_std_deviation = math.pow(10, order_of_greatness)
      else:
        new_std_deviation = max(new_std_deviation, 1.5e-1)
      if todo == 'divide':
        new_std_deviation /= deviation_constant
      elif todo == 'multiply':
        new_std_deviation *= deviation_constant
      new_feature = max(min(feature + new_std_deviation*np.random.normal(0, 1), 15), -15)
      child[idx] = (new_feature, new_std_deviation)
      if(calculate_fitness(child)[1] >= parent_fitness):
        child[idx] = parent_feature[idx]
      else:
        successful_mutations += 1
      total_mutations += 1
    
    new_population.append(child)
  return new_population 

def spin_wheel(roleta, sorted_probability):
  for idx, probability in enumerate(roleta):
      if idx > 0:
          if(sorted_probability <= probability and sorted_probability > roleta[idx-1]):
              break
      else:
          if(sorted_probability <= probability):
              break
  return idx

def parent_selection(population):
  total_fitness = reduce(lambda x,y: x + y[1], population,0)
  parents = population
  roleta = []
  current_probability=0
  parents.sort(key=lambda tup: tup[1], reverse=False)
  for parent in parents:
        roleta.append(current_probability + (parent[1]/total_fitness)) 
        current_probability = roleta[-1]
  parents = []
  return roleta
    
def survival_selection(new_population, population_size):
  new_population.sort(key=lambda tup: tup[1])
  return new_population[:population_size]

def init_population(population_size):
    population = []
    while population_size > 0:
        child = []
        for i in range(30):
          child.append((min((random.random() * 31), 30) - 15, np.random.normal(0,1)))
        population.append(child)
        population_size -= 1
    return population

def eval(population_fitness):
    for individual in population_fitness:
        if individual[1] == 0:
            return individual[0]
    return None

def ackley_function_optimization():
  global todo, total_mutations, successful_mutations
  population_size = 10
  iterations = 2000
  population = init_population(population_size)
  population_fitness = calculate_population_fitness(population)
  solution = eval(population_fitness)
  count = 0
  while solution == None and count < iterations:
      children = mutate(population_fitness)
      children_fitness = calculate_population_fitness(children)
      population_fitness = survival_selection(children_fitness, population_size)
      solution = eval(population_fitness)
      if count % 20 == 0: print(count, '->', population_fitness[0][1], todo, '--', successful_mutations/total_mutations, 'dis->',calculate_mean(list(map(lambda x: x[0], population_fitness)), 1))
      count += 1
  return (population_fitness[0][1], calculate_mean(population_fitness,1), calculate_std(population_fitness, 1))


def calculate_mean(generations, pos):
    return np.mean(list(map(lambda x : x[pos], generations)))

def calculate_std(generations, pos):
    return np.std(list(map(lambda x : x[pos], generations)))

if __name__ == "__main__":
  generation_infos = []
  for i in range(5):
      generation_infos.append(ackley_function_optimization())
  print(generation_infos)
  print("Quantidade de convergências: ", len(list(filter(lambda x : x[0] == 0, generation_infos))))
  print('Media de fitness dos melhores indivíduos de cada execução: ', calculate_mean(generation_infos, 0), ' Desvio Padrão dos melhores indivíduos de cada execução :', calculate_std(generation_infos, 0))
  print('Media Fitness: ', calculate_mean(generation_infos, 1), ' Desvio Padrão Fitness:', calculate_std(generation_infos, 2))
