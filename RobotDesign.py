import FreeCAD as App
import Part
import time
from FreeCAD import Vector, Rotation

# Create a new document
doc = App.newDocument("VerticalRobotArm")

# Parameters
base_radius = 40.0
base_height = 15.0

link_width = 15.0  # Square cross-section
link1_height = 100.0
link2_height = 80.0
link3_height = 50.0

joint_radius = 12.0
joint_length = 25.0

# Create the base cylinder
base = doc.addObject("Part::Cylinder", "Base")
base.Radius = base_radius
base.Height = base_height

# Create first link (vertical rectangular prism)
link1 = doc.addObject("Part::Box", "Link1")
link1.Length = link_width
link1.Width = link_width
link1.Height = link1_height
# Position at center of base
link1.Placement.Base = Vector(-link_width/2, -link_width/2, base_height)

# Create first joint
joint1_z_pos = base_height + link1_height
joint1 = doc.addObject("Part::Cylinder", "Joint1")
joint1.Radius = joint_radius
joint1.Height = joint_length
# Position horizontally centered on top of link1
joint1.Placement.Base = Vector(0, joint_radius, joint1_z_pos)

joint1.Placement.Rotation = Rotation(Vector(1, 0, 0), 90)

joint2_z_pos = joint1_z_pos + (joint_radius)
# Create second link
link2 = doc.addObject("Part::Box", "Link2")
link2.Length = link_width
link2.Width = link_width
link2.Height = link2_height
# Position on top of first joint
link2.Placement.Base = Vector(-link_width/2, -link_width/2, joint2_z_pos)

# Create second joint
joint2_z_pos = joint1_z_pos + link1_height
joint2 = doc.addObject("Part::Cylinder", "Joint2")
joint2.Radius = joint_radius
joint2.Height = joint_length
# Position horizontally centered on top of link2
joint2.Placement.Base = Vector(0, joint_radius, joint2_z_pos)
joint2.Placement.Rotation = Rotation(Vector(1, 0, 0), 90)

joint3_z_pos = joint2_z_pos
# Create third link (top link)
link3 = doc.addObject("Part::Box", "Link3")
link3.Length = link_width
link3.Width = link_width
link3.Height = link3_height
# Position on top of second joint
link3.Placement.Base = Vector(-link_width/2, -link_width/2, joint3_z_pos)

# Add small connection piece at base (red part in the image)
connector = doc.addObject("Part::Box", "Connector")
connector.Length = 10.0
connector.Width = 5.0
connector.Height = 10.0
connector.Placement.Base = Vector(-5.0, -2.5, base_height - 5.0)

# Set connector color to red
if hasattr(connector, "ViewObject"):
    connector.ViewObject.ShapeColor = (1.0, 0.0, 0.0)  # RGB for red

# Function to rotate joints for simulation
def rotate_joint(joint_num, angle_deg):
    """
    Rotate a joint by the specified angle in degrees
    and rotate all dependent links and joints together
    
    Parameters:
    joint_num: 1 or 2 (which joint to rotate)
    angle_deg: angle in degrees
    """
    if joint_num == 1:
        # Store the original positions for calculations
        original_joint1_pos = Vector(joint1.Placement.Base.x + joint_length/2,
                                    joint1.Placement.Base.y + joint_radius/2,
                                    joint1.Placement.Base.z)
        
        # Create rotation object
        rot = Rotation(Vector(0, 1, 0), angle_deg)
        
        # Rotate joint1
        joint1.Placement.Rotation = Rotation(Vector(1, 0, 0), 90).multiply(rot)
        
        # Calculate new position and rotation for link2
        # Link2 should rotate with joint1 around the pivot point
        
        # Vector from joint1 center to link2 center before rotation
        link2_center_original = Vector(0, 0, link2_height/2)
        
        # Rotate this vector
        link2_center_rotated = rot.multVec(link2_center_original)
        
        # New position for link2
        new_link2_pos = Vector(
            original_joint1_pos.x - link_width/2,
            original_joint1_pos.y - link_width/2,
            original_joint1_pos.z + link2_center_rotated.z - link2_height/2
        )
        
        # Update link2 position and apply the same rotation
        link2.Placement.Base = new_link2_pos
        link2.Placement.Rotation = rot
        
        # Joint2 should be at the top of link2 and rotate with it
        joint2_offset = Vector(link_width/2, link_width/2, link2_height)
        joint2_offset_rotated = rot.multVec(joint2_offset)
        
        new_joint2_pos = Vector(
            new_link2_pos.x + joint2_offset_rotated.x - joint_length/2,
            new_link2_pos.y + joint2_offset_rotated.y - joint_radius/2,
            new_link2_pos.z + joint2_offset_rotated.z
        )
        
        # Update joint2
        joint2.Placement.Base = new_joint2_pos
        joint2.Placement.Rotation = Rotation(Vector(1, 0, 0), 90).multiply(rot)
        
        # Link3 needs to rotate and move with joint2
        new_link3_pos = Vector(
            new_joint2_pos.x + joint_length/2 - link_width/2,
            new_joint2_pos.y + joint_radius/2 - link_width/2,
            new_joint2_pos.z
        )
        
        # Update link3
        link3.Placement.Base = new_link3_pos
        link3.Placement.Rotation = rot
        
    elif joint_num == 2:
        # Get current rotation of joint1/link2
        current_rot = link2.Placement.Rotation
        
        # Store the original position of joint2 for calculations
        original_joint2_pos = Vector(joint2.Placement.Base.x + joint_length/2,
                                    joint2.Placement.Base.y + joint_radius/2,
                                    joint2.Placement.Base.z)
        
        # Create new rotation for joint2
        new_rot = Rotation(Vector(0, 1, 0), angle_deg)
        
        # Rotate joint2
        joint2.Placement.Rotation = Rotation(Vector(1, 0, 0), 90).multiply(
                                   current_rot.multiply(new_rot))
        
        # Calculate new position for link3
               
        # Vector from joint2 center to link3 center before this rotation
        link3_center_original = Vector(0, 0, link3_height/2)
        
        # Rotate this vector with the new rotation
        link3_center_rotated = new_rot.multVec(link3_center_original)
        
        # Transform using current rotation of the arm
        link3_center_final = current_rot.multVec(link3_center_rotated)
        
        # New position for link3
        new_link3_pos = Vector(
            original_joint2_pos.x - link_width/2,
            original_joint2_pos.y - link_width/2,
            original_joint2_pos.z + link3_center_final.z - link3_height/2
        )
        
        # Update link3 position and apply combined rotation
        link3.Placement.Base = new_link3_pos
        link3.Placement.Rotation = current_rot.multiply(new_rot)
    
    doc.recompute()

# Create a group for all components
arm_group = doc.addObject("App::DocumentObjectGroup", "VerticalRobotArm")
arm_group.addObjects([base, link1, joint1, link2, joint2, link3, connector])

# Recompute the document
doc.recompute()

# Set view
try:
    import FreeCADGui
    FreeCADGui.ActiveDocument.ActiveView.viewAxonometric()
    FreeCADGui.SendMsgToActiveView("ViewFit")
except:
    # Running in console mode without GUI
    print("Running in console mode")

print("Vertical robot arm created successfully!")
print("You can use the rotate_joint(joint_num, angle) function to simulate joint movement")
print("Example: rotate_joint(1, 45) will rotate the first joint by 45 degrees")

time.sleep(5)
rotate_joint(2,45)
