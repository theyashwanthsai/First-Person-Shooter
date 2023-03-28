from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()

# Create a ground plane
ground = Entity(model='plane', scale=(20,1,20), texture='grass', collider='box')

# Create some walls
wall1 = Entity(model='cube', scale=(1,3,20), position=(-9,1,0), texture='brick', collider='box')
wall2 = Entity(model='cube', scale=(1,3,20), position=(9,1,0), texture='brick', collider='box')
wall3 = Entity(model='cube', scale=(20,3,1), position=(0,1,-9), texture='brick', collider='box')
wall4 = Entity(model='cube', scale=(20,3,1), position=(0,1,9), texture='brick', collider='box')

# Create a target
target = Entity(model='cube', scale=(1,3,3), position=(0,1,0), texture='white_cube', collider='box')

# Create the player
player = FirstPersonController()

# Add a crosshair
crosshair = Entity(parent=camera.ui, model='quad', scale=0.025, position=(0,0,-0.1), color=color.red, texture='crosshair')

# Create a weapon
class Gun(Entity):
    def _init_(self):
        super()._init_(
            parent=camera.ui,
            model='cube',
            origin_y=-0.5,
            color=color.dark_gray,
            scale=(0.1, 0.2, 0.5),
            position=(0.6, -0.4, 0),
        )
        self.bullet_speed = 50
        self.bullet_lifetime = 0.5
        self.bullets = []

    def shoot(self):
        bullet = Entity(
            parent=scene,
            model='sphere',
            color=color.white,
            scale=0.2,
            position=self.position,
            direction=camera.forward * self.bullet_speed,
        )
        self.bullets.append(bullet)
        invoke(self.remove_bullet, bullet, delay=self.bullet_lifetime)

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)
        destroy(bullet)

gun = Gun()

def update():
    # Move the target randomly
    target.x += random.uniform(-0.1, 0.1)
    target.z += random.uniform(-0.1, 0.1)

    # Check if the player has hit the target
    if player.intersects(target).hit:
        target.color = color.red
        if held_keys['left mouse']:
            target.visible = False

    # Check if the player is shooting
    if held_keys['left mouse']:
        gun.shoot()

app.run()
