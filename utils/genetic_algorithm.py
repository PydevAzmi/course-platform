import os
import django
import random

MUTATION_RATE = 0.02
GENERATIONS = 50
CROSSOVER_RATE = 0.7

def generate_genome(genome_length, course):
    genome = []
    for chapter in course.chapters.all():
        questions = list(chapter.questions.all())
        if len(questions) >= genome_length:
            genome.extend(random.sample(questions, genome_length))
        else:
            genome.extend(questions)  # Take all if fewer than the required
    return genome


def init_population(population_size, genome_length, course):
    population = []
    for _ in range(population_size):
        genome = generate_genome(genome_length, course)
        population.append(genome)
    return population


def fitness(genome, x1, x2, x3, y1, y2, y3):
    a1, a2, a3 = 0, 0, 0
    b1, b2, b3 = 0, 0, 0

    for question in genome:
        if question.difficulty == 'Simple':
            if question.objective == 'Remideing':
                a1 += 1
            elif question.objective == 'Understanding':
                a2 += 1
            elif question.objective == 'Creativity':
                a3 += 1
        elif question.difficulty == 'Difficult':
            if question.objective == 'Remideing':
                b1 += 1
            elif question.objective == 'Understanding':
                b2 += 1
            elif question.objective == 'Creativity':
                b3 += 1

    fitness_score = (
        (x1 - a1) ** 2 + (y1 - b1) ** 4 +
        (x2 - a2) ** 2 + (y2 - b2) ** 4 +
        (x3 - a3) ** 2 + (y3 - b3) ** 4
    )
    return fitness_score


def selection(population, fitness_scores):
    # Implementing Tournament Selection
    tournament_size = 5
    selected = random.sample(list(zip(population, fitness_scores)), tournament_size)
    return min(selected, key=lambda x: x[1])[0]


def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 2)
    return parent1[:crossover_point] + parent2[crossover_point:]


def mutate(genome, course):
    if random.random() < MUTATION_RATE:
        random_chapter = random.choice(course.chapters.all())
        random_question = random.choice(list(random_chapter.questions.all()))
        mutation_index = random.randint(0, len(genome) - 1)
        genome[mutation_index] = random_question
    return genome


def generate_exam(course, question_per_chapter, x1, x2, x3, y1, y2, y3):
    genome_length = question_per_chapter
    population_size = course.chapters.count() * genome_length

    if population_size < (x1 + x2 + x3) + (y1 + y2 + y3):
        return ValueError("Difficulty level size is not equal to the given genome length.")

    population = init_population(population_size, genome_length, course)

    for g in range(GENERATIONS):
        fitness_scores = [fitness(genome, x1, x2, x3, y1, y2, y3) for genome in population]
        best_fitness = min(fitness_scores) 

        print(f"Generation {g} : Best Fitness: {best_fitness}")
        if best_fitness == 0:
            break

        # Selection and new population generation
        new_population = []
        while len(new_population) < population_size:
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)

            # Perform crossover and mutation
            if random.random() < CROSSOVER_RATE:
                child = crossover(parent1, parent2)
            else:
                child = parent1

            child = mutate(child, course)
            new_population.append(child)

        population = new_population

    # Return the best genome
    best_genome = selection(population, fitness_scores)
    return best_genome


if __name__ == "__main__":
    generate_exam()
