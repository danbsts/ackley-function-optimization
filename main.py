import random
import math
import numpy as np

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

def calculate_fitness(population):
  result = []
  for x,desvio in population:
    term1 = (-20)* math.exp( (-0.2) *math.sqrt(square_sum(x)/30.0) )
    term2 = -math.exp(cos_sum(x)/30.0)
    y =  term2 + math.exp(1) +term1 + 20.0 
    result.append((x,desvio,y))
  return result

def mutate(child):
  # TODO - implement method
  return None

def parent_selection(population):
  # TODO - implement method
  return None
    
def survival_selection(population):
  # TODO - implement method
  return None
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
        if individual[1] == 1:
            return individual[0]
    
    return None

def ackley_function_optimization():
    population = init_population(100)
    population_fitness = calculate_fitness(population)
    solution = eval(population_fitness)
    count = 0
    while solution == None and count < 10000:
        # parents = parent_selection(population_fitness)
        # children = cut_and_crossfill(parents)
        # children = list(map(lambda child: mutate(child) if random.random() <= 0.4 else child, children)) 
        # children = calculate_fitness(children)
        # population_fitness.append(children[0])
        # population_fitness.append(children[1])
        # population_fitness = survival_selection(population_fitness)
        # solution = eval(population_fitness)
        count += 1
    if count == 10000:
        return -1
    else:
        total_converged = len(list(filter(lambda x : x[1] == 1, population_fitness)))
        return (count, total_converged, calculate_mean(population_fitness,1), calculate_std(population_fitness,1))

def calculate_mean(generations, pos):
    return np.mean(list(map(lambda x : x[pos], generations)))

def calculate_std(generations, pos):
    return np.std(list(map(lambda x : x[pos], generations)))

if __name__ == "__main__":
  a = []
  b = []
  for i in range(30):
    a.append(0)
  desvio = 2
  b.append((a,desvio))
  j = calculate_fitness(b)
  j.sort(key=lambda tup: tup[2], reverse=False)
  for i in j:
    print(i)

  # generation_infos = []
  # for i in range(30):
  #     generation_infos.append(ackley_function_optimization())
  # print("Quantidade de convergências: ", 30 - len(list(filter(lambda x : x[0] == -1, generation_infos))))
  # print('Media de iterações que o algoritmo convergiu: ', calculate_mean(generation_infos, 0), ' Desvio Padrão das iterações que o algoritmo convergiu :', calculate_std(generation_infos, 0))
  # print('Média de Indivíduos que convergiram por execução : ', calculate_mean(generation_infos, 1))
  # print('Media Fitness: ', calculate_mean(generation_infos, 2), ' Desvio Padrão Fitness:', calculate_std(generation_infos, 2))
