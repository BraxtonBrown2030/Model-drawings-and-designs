import maya.cmds as cmds

# Select joints and controls
sl = cmds.ls(sl=True)
parent_cntrl = sl[0]
child_cntrl = sl[1]

# Create controls for each selected joint
selected_joints = cmds.ls(sl=True)
for joint in selected_joints:
    if "_jnt" in joint:
        ctrlName = joint.replace("_jnt", "_ctrl")
    else:
        ctrlName = joint + "_ctrl"

    ctrl = cmds.circle(nr=(0, 1, 0), r=3, n=ctrlName)[0]
    group = cmds.group(ctrl, n=ctrl + "_Grp")
    cmds.matchTransform(group, joint)

    # Create groups and match transforms
    child_cntrl_grp = cmds.listRelatives(child_cntrl, parent=True)[0]

    # Create parent constraints
    p_constarnt1 = cmds.parentConstraint(parent_cntrl, child_cntrl_grp, mo=True, skipTranslate=["x", "z", "y"], weight=1)[0]
    p_constarnt2 = cmds.parentConstraint(parent_cntrl, child_cntrl_grp, mo=True, skipRotate=["x", "z", "y"], weight=1)[0]
    cmds.scaleConstraint(parent_cntrl, child_cntrl_grp, weight=1)

    # Add attributes if they don't exist
    if not cmds.attributeQuery('FollowTranslate', node=child_cntrl, exists=True):
        cmds.addAttr(child_cntrl, ln='FollowTranslate', at='double', min=0, max=1, dv=1)
        cmds.setAttr('%s.FollowTranslate' % (child_cntrl), e=True, keyable=True)

    if not cmds.attributeQuery('FollowRotate', node=child_cntrl, exists=True):
        cmds.addAttr(child_cntrl, ln='FollowRotate', at='double', min=0, max=1, dv=1)
        cmds.setAttr('%s.FollowRotate' % (child_cntrl), e=True, keyable=True)

    # Connect attributes
    cmds.connectAttr('%s.FollowTranslate' % (child_cntrl), '%s.%sW0' % (p_constarnt1, parent_cntrl), f=True)
    cmds.connectAttr('%s.FollowRotate' % (child_cntrl), '%s.%sW0' % (p_constarnt2, paren