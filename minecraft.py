import ursina
import ursina.prefabs.first_person_controller

# Initialize Ursina engine first before creating components
app = ursina.Ursina()
player = ursina.prefabs.first_person_controller.FirstPersonController()
ursina.Sky(texture=ursina.load_texture("assets/sky.png"))

voxel_selected = 1

textures = [
    None, #placeholder 0
    ursina.load_texture("assets/grass_uv.png"),    #Key 1
    ursina.load_texture("assets/dirt_uv.png"),     #Key 2
    ursina.load_texture("assets/wood_uv.png"),     #Key 3
    ursina.load_texture("assets/stone_uv.png"),    #Key 4
    ursina.load_texture("assets/brick_uv.png"),    #Key 5
]

texture_icons = [
    None, #placeholder 0
    ursina.load_texture("assets/grass.png"),    #Key 1
    ursina.load_texture("assets/dirt.png"),     #Key 2
    ursina.load_texture("assets/wood.png"),     #Key 3
    ursina.load_texture("assets/stone.png"),    #Key 4
    ursina.load_texture("assets/brick.png"),    #Key 5
]

models = {
    "cube": "assets/cube.obj",
    "tree" : "assets/tree.glb",
    "pig" : "assets/pig.glb",
    "chicken" : "assets/chicken.glb",
}

animal_models = [models["chicken"], models["pig"]]

slot_entities = [None]*6
start_x = -0.45
spacing = 0.15

# Create the 5 inventory slots
for i in range(1, 6):
    slot_x = start_x + i * spacing
    slot_entities[i] = ursina.Entity(
        parent = ursina.camera.ui,
        model = "quad",
        texture = texture_icons[i],
        scale = 0.10,
        position = (slot_x, -0.4)
    )

# Create an outline box that highlights the active slot
selector_outline = ursina.Entity(
    parent = ursina.camera.ui,
    model = "quad",
    color = ursina.color.light_gray,  # Outline highlight color
    scale = 0.12,                # Slightly bigger than the slot square
    z = 0.1,                     # Places it slightly behind the texture block layer
    position = (slot_entities[voxel_selected].x, -0.4)
)

class Voxel(ursina.Button): #minecraft blocks are basically buttons (click to do something)
    def __init__(self, position, texture):
        super().__init__(
            parent = ursina.scene, 
            color = ursina.color.white,
            highlight_color = ursina.color.light_gray, 
            position = position,
            model = models["cube"], 
            texture = texture,
            origin_y = 0.5, 
            scale = 0.5
        )

class Prop(ursina.Entity): #trees, chickens, pigs
    def __init__(self, position, model, scale):
        super().__init__(
            parent = ursina.scene,
            position = position,
            model = model,
            origin_y = 0.5,
            scale = scale,
            collider = "mesh" #wraps around the object
        )

def generate_map(num_trees=2, num_animals=5):
    num_tiles = 30
    for z in range(num_tiles):
        for x in range(num_tiles):
            Voxel(position=(x, 0, z), texture=textures[1])

    # Trees 
    for _ in range(num_trees):
        tree_x = ursina.random.randint(1, num_tiles-1)
        tree_z = ursina.random.randint(1, num_tiles-1)
        Prop(position=(tree_x, 1, tree_z), model=models["tree"], scale=5.5)

    # Animals
    for _ in range(num_animals):
        animal_x = ursina.random.randint(1, num_tiles-1)
        animal_z = ursina.random.randint(1, num_tiles-1)
        animal_model = ursina.random.choice(animal_models)
        Prop(position=(animal_x, 1, animal_z), model=animal_model, scale=0.1)

#ursina automatically looks for update/input functions
def input(key):
    global voxel_selected

    if key == "escape":
        ursina.application.quit()

    elif key in ['1', '2', '3', '4', '5']:
        voxel_selected = int(key)
        # Move the outline frame smoothly to match the selected slot's X coordinate
        selector_outline.x = slot_entities[voxel_selected].x

    # Mouse actions directly checking the hovered entity object
    if isinstance(ursina.mouse.hovered_entity, Voxel):
        if key == "left mouse down":
            Voxel(
                position = ursina.mouse.hovered_entity.position + ursina.mouse.normal, 
                texture = textures[voxel_selected]
            )
        elif key == "right mouse down":
            ursina.destroy(ursina.mouse.hovered_entity)

generate_map()
app.run()
