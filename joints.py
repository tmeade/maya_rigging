import maya.cmds as cmds


def scale_joints_by_curve(spline_ik_handle):
    print 'spline_ik_handle'
    start_joint = cmds.listConnections('{}.startJoint'.format(spline_ik_handle))[0]
    end_effector = cmds.listConnections('{}.endEffector'.format(spline_ik_handle))[0]
    ik_curve = cmds.listConnections('{}.inCurve'.format(spline_ik_handle, plugs=True))[0]
    ik_curve_shape = cmds.listRelatives(ik_curve, shapes=True)[0]

    scale_factor_node = calculate_scale_factor(ik_curve_shape)

    last_joint = cmds.listRelatives(end_effector, parent=True)[0]
    joints_to_scale = get_joints_in_chain_reverse(
                                                    start_joint,
                                                    last_joint,
                                                    joints_to_scale=[last_joint])

    for joint in joints_to_scale:
        cmds.connectAttr('{}.outputX'.format(scale_factor_node), '{}.scaleX'.format(joint))

    return joints_to_scale


def get_joints_in_chain_reverse(start_joint, end_joint, joints_to_scale=list()):
    parent_joint = None
    if end_joint != start_joint:
        parent_joint = cmds.listRelatives(end_joint, parent=True)[0]
        joints_to_scale.append(parent_joint)
        get_joints_in_chain_reverse(start_joint, parent_joint, joints_to_scale)

    return joints_to_scale


def calculate_scale_factor(ik_curve_shape):

    curve_info_node = cmds.createNode('curveInfo', n='spline_ik_curve_info')
    cmds.connectAttr(
                    '{}.worldSpace[0]'.format(ik_curve_shape),
                    '{}.inputCurve'.format(curve_info_node)
                    )

    curve_lenght_rest = cmds.getAttr('{}.arcLength'.format(curve_info_node))
    divide_node = cmds.createNode('multiplyDivide', name='scale_length_factor_multDivide')
    cmds.connectAttr('{}.arcLength'.format(curve_info_node), '{}.input1X'.format(divide_node))
    cmds.setAttr('{}.input2X'.format(divide_node), curve_lenght_rest)
    cmds.setAttr('{}.operation'.format(divide_node), 2)

    return divide_node
