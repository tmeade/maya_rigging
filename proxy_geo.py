cmds.SelectHierarchy()
selection = cmds.ls(sl=True)


for jnt in selection:
    if len(jnt.split('_')) == 3:
        base_name = 'proxy_geo_{}'.format(jnt.split('_')[-1])
    elif len(jnt.split('_')) == 4:
        base_name = 'proxy_geo_{}_{}'.format(jnt.split('_')[-2], jnt.split('_')[-1])
    elif len(jnt.split('_')) == 5:
        base_name = 'proxy_geo_{}_{}_{}'.format(jnt.split('_')[-3], jnt.split('_')[-2], jnt.split('_')[-1])

    if cmds.objExists(base_name):
        print('Match')
        cmds.parentConstraint(jnt, base_name)
    else:
        print('{} has no proxy geo match to {}'.format(jnt, base_name))
