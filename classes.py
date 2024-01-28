from math import floor
from random import random, randint

def map(input_value, in1, in2, out1, out2): # standart map fonksiyonu
    return (input_value - in1) * (out2 - out1) / (in2 - in1) + out1

def new_char():
    c = randint(63, 122)    
    if c == 63: c = 32      
    if c == 64: c = 46          
    return chr(c)           

class Chromosome:
    def __init__(self, targt):
        self.genes = []
        self.fitness = 0
        self.target = targt 
        for i in range(len(self.target)):
            self.genes.append(new_char())
    
    def fit_func(self): # uygunluk fonksiyonu
        score = 0
        for gene, targt in zip(self.genes, self.target):
            if gene == targt:
                score += 1 
        self.fitness = score / len(self.target) 
    
    def crossover(self, partner): # caprazlama
        child = Chromosome(self.target)
        mid_point = randint(0, len(self.genes)-1)
        for i in range(len(self.genes)):
            if i > mid_point: child.genes[i] = self.genes[i]
            else: child.genes[i] = partner.genes[i]
        return child
        
    def mutate(self, mutation_rate): # mutasyon
        for i in range(len(self.genes)):
            if random() < mutation_rate:
                self.genes[i] = new_char()
            
    def get_phrase(self):
        return "".join(self.genes)

class Monkeys:
    def __init__(self, pop_size, m_rate, target):
        self.mutation_rate = m_rate
        self.generation = 0
        self.best_score_global = 1
        self.best_score_local = {"fit": 0, "index": 0}
        self.best_phrase = ""
        self.finished = False
        self.mating_pool = []

        self.monkeys = []
        for i in range(pop_size):
            self.monkeys.append(Chromosome(target)) 

        self.calc_fitness()

    def calc_fitness(self): # uygunluk degerlerini hesapla
        max_fitness = 0
        index = 0
        for monkey in self.monkeys:
            monkey.fit_func()
            if monkey.fitness > max_fitness:
                max_fitness = monkey.fitness
                index = self.monkeys.index(monkey)
        self.best_score_local["fit"] = max_fitness
        self.best_score_local["index"] = index

    def natural_selection(self): # dogal secilim
        self.mating_pool = []
        for monkey in self.monkeys:
            fitness = map(monkey.fitness, 0, self.best_score_local["fit"], 0, 1)
            n = floor(fitness * 100)
            for i in range(n):
                self.mating_pool.append(monkey)

    def generate(self): # yeni bireylerin olusturulmasi
        m_pool_size = len(self.mating_pool) - 1
        for x in range(len(self.monkeys)):
            i = randint(0, m_pool_size)
            j = randint(0, m_pool_size) 
            partner1 = self.mating_pool[i]
            partner2 = self.mating_pool[j]
            child = partner1.crossover(partner2)
            child.mutate(self.mutation_rate)
            self.monkeys[x] = child
        self.generation += 1

    def evaluate(self): # degerlendirme
        best_index = self.best_score_local["index"]
        self.best_phrase = self.monkeys[best_index].get_phrase()
        if self.best_score_local["fit"] == self.best_score_global:
            self.finished = True
    

    def is_finished(self): # bitti mi?
    	return self.finished

    # Yardimci Fonksiyonlar #

    def get_average(self):    
        count = 0
        for monkey in self.monkeys:
            count += monkey.fitness
        return count / len(self.monkeys)

    def get_best_phrase(self):
    	return self.best_phrase

    def get_generation(self):
    	return str(self.generation)



