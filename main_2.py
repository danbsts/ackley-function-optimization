import random
import math
import numpy as np

successful_mutations = 0
total_mutations = 0
todo = 'divide'
deviation_constant = 0.8

def square_sum(vetor):
  sum = 0
  for x in vetor:
    sum += x*x
  return sum

def cos_sum(vetor):
  sum = 0
  for x in vetor:
    sum += math.cos(math.pi*2*x)
  return sum

def calculate_population_fitness(population):
  result = []
  for i in population:
    result.append(calculate_fitness(i))
  return result

def calculate_fitness(individual):
  (x, desvio) = individual
  term1 = (-20)* math.exp( (-0.2) *math.sqrt(square_sum(x)/len(x)) )
  term2 = -math.exp(cos_sum(x)/len(x))
  y =  term2 + math.exp(1) +term1 + 20.0 
  return (x,desvio,y)

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
  while(len(new_population) < 7 * len(population)):
    random_idx = random.randint(0, len(population) - 1)
    (parent_feature, std_deviation, parent_fitness) = population[random_idx]
    std_deviation = max(std_deviation, 1.55e-1)
    new_std_deviation =  abs(std_deviation * math.exp((1/pow(len(parent_feature), 0.5)) * np.random.normal(0, 1)))
    if todo == 'divide':
      new_std_deviation /= deviation_constant
    elif todo == 'multiply':
      new_std_deviation *= deviation_constant
    child_feature = []
    for i in range(len(parent_feature)):
        child_feature.append(max(min(parent_feature[i] + np.random.normal(0, new_std_deviation), 15), -15))
    child = (child_feature, new_std_deviation)
    child_fitness = calculate_fitness(child)
    if child_fitness[2] < parent_fitness:
      successful_mutations += 1
    total_mutations += 1
    new_population.append(child)
  return new_population

def parent_selection(population):
  parents = []
  while len(parents) < len(population):
    random_number = random.randint(len(population)) - 1
    parents.append(population[random_number])
    population.pop(random_number)
  return parents
    
def survival_selection(new_population, population_size):
  new_population.sort(key=lambda tup: tup[2])
  return new_population[:population_size]

def init_population(population_size):
    population = []
    while population_size > 0:
        child = []
        for i in range(30):
          child.append(min((random.random() * 31), 30) - 15)
        population.append((child, np.random.normal(0, 1)))
        population_size -= 1
    return population

def eval(population_fitness):
    for individual in population_fitness:
        if individual[2] == 0:
            return individual[0]
    return None

def ackley_function_optimization():
  global todo, total_mutations, successful_mutations
  population_size = 20
  iterations = 10000
  population = init_population(population_size)
  population_fitness = calculate_population_fitness(population)
  solution = eval(population_fitness)
  count = 0
  while solution == None and count < iterations:
      children = mutate(population_fitness)
      children_fitness = calculate_population_fitness(children)
      population_fitness = survival_selection(children_fitness, population_size)
      solution = eval(population_fitness)
      print(count, '->', population_fitness[0][2], todo, '--', successful_mutations/total_mutations, 'dis->',population_fitness[0][1])
      count += 1
      if count % 30 == 0: print("\033[H\033[J")
  if count == iterations:
      return (-1, 0, 1000, 0)
  else:
      total_converged = len(list(filter(lambda x : x[2] == 0, population_fitness)))
      return (count, total_converged, calculate_mean(population_fitness,2), calculate_std(population_fitness,2))

def calculate_mean(generations, pos):
    return np.mean(list(map(lambda x : x[pos], generations)))

def calculate_std(generations, pos):
    return np.std(list(map(lambda x : x[pos], generations)))

if __name__ == "__main__":
  generation_infos = []
  for i in range(1):
      generation_infos.append(ackley_function_optimization())
  print(generation_infos)
  print("Quantidade de convergências: ", 1 - len(list(filter(lambda x : x[0] == -1, generation_infos))))
  print('Media de iterações que o algoritmo convergiu: ', calculate_mean(generation_infos, 0), ' Desvio Padrão das iterações que o algoritmo convergiu :', calculate_std(generation_infos, 0))
  print('Média de Indivíduos que convergiram por execução : ', calculate_mean(generation_infos, 1))
  print('Media Fitness: ', calculate_mean(generation_infos, 2), ' Desvio Padrão Fitness:', calculate_std(generation_infos, 2))
