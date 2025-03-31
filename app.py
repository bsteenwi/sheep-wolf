from agents import GrassPatch, Sheep, Wolf
from model import WolfSheep
from mesa.experimental.devs import ABMSimulator
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)

def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "size": 25,
    }

    if isinstance(agent, Wolf):
        portrayal["color"] = "tab:orange"
        portrayal["marker"] = ">"
        portrayal["zorder"] = 2
    elif isinstance(agent, Sheep):
        portrayal["color"] = "white"
        portrayal["marker"] = "o"
        portrayal["zorder"] = 2
    elif isinstance(agent, GrassPatch):
        if agent.fully_grown:
            portrayal["color"] = "tab:green"
        else:
            portrayal["color"] = "tab:brown"
        portrayal["marker"] = "s"
        portrayal["size"] = 75

    return portrayal


model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "grass": {
        "type": "Select",
        "value": True,
        "values": [True, False],
        "label": "grass regrowth enabled?",
    },
    "grass_regrowth_time": Slider("Grass Regrowth Time", 20, 1, 50),
    "initial_sheep": Slider("Initial Sheep Population", 100, 10, 300),
    "sheep_reproduce": Slider("Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01),
    "initial_wolves": Slider("Initial Wolf Population", 10, 5, 100),
    "wolf_reproduce": Slider(
        "Wolf Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
    ),
    "wolf_gain_from_food": Slider("Wolf Gain From Food Rate", 20, 1, 50),
    "sheep_gain_from_food": Slider("Sheep Gain From Food", 4, 1, 10),
}


def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def post_process_lines(ax):
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.9))


space_component = make_space_component(
    wolf_sheep_portrayal, draw_grid=False, post_process=post_process_space
)
lineplot_component = make_plot_component(
    {"Wolves": "tab:orange", "Sheep": "tab:cyan", "Grass": "tab:green"},
    post_process=post_process_lines,
)

def clear_console():
    print("\033[H\033[J", end="")

def print_console_grid(model):
    width = model.grid.width
    height = model.grid.height

    clear_console()  # Clears console for better visualization

    for y in range(height):
        row = ""
        for x in range(width):
            cell = model.grid[(x, y)]

            # Retrieve grass state
            grass = next((a for a in cell.agents if isinstance(a, GrassPatch)), None)
            # Base appearance
            base_char = "\033[33m.\033[0m"  # Default to brown (dead grass)
            if grass and grass.fully_grown:
                base_char = "\033[32m#\033[0m"  # Green if fully grown

            # Check for animals
            wolf_present = any(
                isinstance(agent, Wolf) and getattr(agent, "alive", True)
                for agent in cell.agents
            )
            sheep_present = any(
                isinstance(agent, Sheep) and getattr(agent, "alive", True)
                for agent in cell.agents
            )

            # Prioritize wolves > sheep > grass
            if wolf_present:
                cell_char = "\033[38;5;208mW\033[0m"
            elif sheep_present:
                cell_char = "\033[97mS\033[0m"
            else:
                cell_char = base_char

            row += cell_char + " "
        print(row)

import time

def get_user_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a valid positive integer.")

# Get user inputs
grid_size = get_user_input("Enter grid size: ")
num_sheep = get_user_input("Enter number of sheep: ")
num_wolves = get_user_input("Enter number of wolves: ")
steps = get_user_input("Enter number of steps: ")

print(f"Starting simulation with Grid Size: {grid_size}, Sheep: {num_sheep}, Wolves: {num_wolves}, Steps: {steps}\n")

simulator = ABMSimulator()
model = WolfSheep(simulator=simulator, grass=True, width=grid_size, height=grid_size, initial_sheep=num_sheep, initial_wolves=num_wolves)
# Placeholder for simulation loop
for step in range(steps):
    # Simulate a step (Replace with actual model simulation logic)
    model.step()
    clear_console()
    print_console_grid(model)
    # Print statistics for the current step
    # Count the number of wolves, sheep, and fully grown grass patches
    num_wolves = len(model.agents_by_type[Wolf])
    num_sheep = len(model.agents_by_type[Sheep])
    num_fully_grown_grass = sum(
        1 for agent in model.agents_by_type[GrassPatch] if agent.fully_grown
    )
    print(f"Step {step}: Sheep={num_sheep}, Wolves={num_wolves}, Fully Grown Grass={num_fully_grown_grass}")
    time.sleep(0.2)

# page = SolaraViz(
#     model,
#     components=[space_component, lineplot_component],
#     model_params=model_params,
#     name="Wolf Sheep",
#     simulator=simulator,
# )
# page  # noqa