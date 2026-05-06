from world.world_generator import WorldGenerator

# Test 1D world
generator = WorldGenerator(world_size=4, world_dimension=1)
world = generator.generate_world()

print("1D World:")
for place in world[0]:
    print(f"  Type: {place.place_type.value}, Score: {place.value}")

# Test 2D world
generator_2d = WorldGenerator(world_size=4, world_dimension=2)
world_2d = generator_2d.generate_world()

print("\n2D World:")
for row in world_2d:
    for place in row:
        print(f"  Type: {place.place_type.value}, Score: {place.value}", end=" | ")
    print()