'''
Disclaimer: This solution is not scalable for creating a big world.
Creating a game like Minecraft requires specialized knowledge and is not as easy
to make as it looks.

You'll have to do some sort of chunking of the world and generate a combined mesh
instead of separate blocks if you want it to run fast. You can use the Mesh class for this.

You can then use blocks with colliders like in this example in a small area
around the player so you can interact with the world.
'''
import ursina
import ursina.prefabs.first_person_controller

app = ursina.Ursina()
player = ursina.prefabs.first_person_controller.FirstPersonController()

# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.
class Voxel(ursina.Button):
    def __init__(self, position):
        super().__init__(
            parent = ursina.scene, 
            color = ursina.color.white,
            highlight_color = ursina.color.light_gray,
            position = position,
            model = "cube",
            texture = "white_cube",
            # texture = ursina.load_texture("assets/grass.png"),
            origin_y = 0.5, 
        )

def generate_map():
    num_tiles = 30
    for z in range(num_tiles):
        for x in range(num_tiles):
            Voxel(position=(x, 0, z))

def input(key):
    if key == "escape":
        ursina.application.quit()
    
    if isinstance(ursina.mouse.hovered_entity, Voxel):
        if key == "left mouse down":
            Voxel(
                position = ursina.mouse.hovered_entity.position + ursina.mouse.normal, 
            )
        elif key == "right mouse down":
            ursina.destroy(ursina.mouse.hovered_entity)

generate_map()
app.run()

