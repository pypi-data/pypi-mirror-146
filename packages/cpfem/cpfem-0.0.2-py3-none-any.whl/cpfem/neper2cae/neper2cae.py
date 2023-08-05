# -*- coding: utf-8 -*-
import numpy as np
try:
    from abaqus import *
    from abaqusConstants import *
    from caeModules import *
    from driverUtils import executeOnCaeStartup
except ImportError:
    print("Without abaqus environment.")


def create_sketch_base(model_name='Model-1', width=1, height=1, center=[0, 0]):
    # =============================================================================
    # Sketch-Base
    # =============================================================================
    s = mdb.models[model_name].ConstrainedSketch(name='Sketch-Base',
                                                 sheetSize=200.0)
    s.rectangle(
        point1=(
            center[0] - width / 2,
            center[1] - height / 2),
        point2=(
            center[0] + width / 2,
            center[1] + height / 2))


def create_part(model_name='Model-1', part_name='PART-1', dimension=2, pdepth=0,
                pwidth=1, pheight=1, datumpointsfilename='', edgesfilename=''):
    # =============================================================================
    # create base shell
    # =============================================================================
    if dimension == 2:
        p = mdb.models[model_name].Part(name=part_name,
                                        dimensionality=TWO_D_PLANAR,
                                        type=DEFORMABLE_BODY)
        p.BaseShell(sketch=mdb.models[model_name].sketches['Sketch-Base'])
    elif dimension == 3:
        p = mdb.models[model_name].Part(name=part_name,
                                        dimensionality=THREE_D,
                                        type=DEFORMABLE_BODY)
        p.BaseSolidExtrude(
            sketch=mdb.models[model_name].sketches['Sketch-Base'], depth=pdepth)

    # =============================================================================
    # create grains
    # =============================================================================
    # read external datum points file and add datum points to cae model
    fid = open(datumpointsfilename, "r")
    # arrays of x, y, z coordinates of vertices
    arrx = np.zeros(shape=(0))
    arry = np.zeros(shape=(0))
    count = 1
    for line in fid:
        tempdata = line.split()
        # get x and y coordinate of datum point
        tempx = float(tempdata[1])
        tempy = float(tempdata[2])
        arrx = np.append(arrx, tempx)
        arry = np.append(arry, tempy)
        p.DatumPointByCoordinate(coords=(tempx, tempy, pdepth))
        count = count + 1
    fid.close()
    f = p.faces

    # define boundingbox to pick the entire upper face
    BoundBox1 = np.zeros(shape=(3))
    BoundBox2 = np.zeros(shape=(3))
    BoundBox1[0] = -0.1*pwidth
    BoundBox1[1] = -0.1*pheight
    BoundBox1[2] = 0.9*pdepth
    BoundBox2[0] = 1.1*pwidth
    BoundBox2[1] = 1.1*pheight
    BoundBox2[2] = 1.1*pdepth
    pickedFaces = f.getByBoundingBox(
        BoundBox1[0], BoundBox1[1], BoundBox1[2], BoundBox2[0], BoundBox2[1], BoundBox2[2])
    v, e, d = p.vertices, p.edges, p.datums
    # array that contains point at the boundary of edges
    # using .tess file numbering
    edgepoint1 = np.array([], dtype='uint64')
    edgepoint2 = np.array([], dtype='uint64')
    # array with the edge indices
    # counting only edges defined on the upper surface
    # and leaving 0 the ones on the corner edges
    edgeindex = np.array([], dtype='uint64')

    # read external edges file to cae model
    fied = open(edgesfilename, "r")
    count = 1
    for line in fied:
        InnerEdge = True  # flag to indicate that this is not an edge at the boundary of the surface
        f = p.faces
        pickedFaces = f.getByBoundingBox(
            BoundBox1[0], BoundBox1[1], BoundBox1[2], BoundBox2[0], BoundBox2[1], BoundBox2[2])
        v, e, d = p.vertices, p.edges, p.datums
        tempdata = line.split()
        # get indices of the datum points bounding the edge
        # indices start from 1
        # these are indices in the .tess file, not abaqus
        # corresponds to abaqus datum point number - 1
        temppoint1 = int(tempdata[1])
        # corresponds to abaqus datum point number - 1
        temppoint2 = int(tempdata[2])
        edgepoint1 = np.append(edgepoint1, np.uint64(temppoint1))
        edgepoint2 = np.append(edgepoint2, np.uint64(temppoint2))
        # is this an edge at the boundary?
        if (arrx[temppoint1-1] == arrx[temppoint2-1]):
            if (arrx[temppoint1-1] == 0.0 or arrx[temppoint1-1] == pwidth):
                InnerEdge = False
        if (arry[temppoint1-1] == arry[temppoint2-1]):
            if (arry[temppoint1-1] == 0.0 or arry[temppoint1-1] == pheight):
                InnerEdge = False
        if (InnerEdge):
            # find abaqus indices
            abqindex1 = temppoint1+1
            abqindex2 = temppoint2+1
            p.PartitionFaceByShortestPath(point1=d[abqindex1], point2=d[abqindex2],
                                          faces=pickedFaces)
            edgeindex = np.append(edgeindex, np.uint64(count))
            count = count + 1
        else:
            edgeindex = np.append(edgeindex, np.uint64(0))
    fied.close()

    if dimension == 3:
        # define boundingbox to pick the entire volume
        BoundBox1[0] = -0.1*pwidth
        BoundBox1[1] = -0.1*pheight
        BoundBox1[2] = -0.1*pdepth
        BoundBox2[0] = 1.1*pwidth
        BoundBox2[1] = 1.1*pheight
        BoundBox2[2] = 1.1*pdepth

        p = mdb.models[model_name].parts[part_name]
        c = p.cells
        pickedCells = c.getByBoundingBox(
            BoundBox1[0], BoundBox1[1], BoundBox1[2], BoundBox2[0], BoundBox2[1], BoundBox2[2])
        alledges, d = p.edges, p.datums

        # create grains = cells
        count = 0
        for indexe in range(0, len(edgeindex)):  # cycle over all edges in tess file
            if (edgeindex[indexe] > 0):  # corresponds to an edge on the upper surface
                temppoint1 = int(edgepoint1[indexe])
                temppoint2 = int(edgepoint2[indexe])
                midx = (arrx[temppoint1-1] + arrx[temppoint2-1])/2.0
                midy = (arry[temppoint1-1] + arry[temppoint2-1])/2.0
                p = mdb.models[model_name].parts[part_name]
                c = p.cells
                pickedCells = c.getByBoundingBox(
                    BoundBox1[0], BoundBox1[1], BoundBox1[2], BoundBox2[0], BoundBox2[1], BoundBox2[2])
                alledges, d = p.edges, p.datums
                # find current edge on the upper surface
                tempedge = alledges.findAt((midx, midy, pdepth))
                sweepEdge = alledges.findAt((pwidth, pheight, 0.4*pdepth))
                p.PartitionCellByExtrudeEdge(line=sweepEdge, cells=pickedCells,
                                             edges=tempedge, sense=REVERSE)


def create_set(model_name='Model-1', part_name='PART-1', grain_prefix='GRAIN_', dimension=2):
    # =============================================================================
    # create grains' sets
    # =============================================================================
    if dimension == 2:
        p = mdb.models[model_name].parts[part_name]
        f = p.faces
        tempgrainnumber = 0
        for face in p.faces:
            tempgrainnumber = tempgrainnumber + 1
            puntoface = f[tempgrainnumber-1].pointOn
            faces = f.findAt(
                ((puntoface[0][0], puntoface[0][1], puntoface[0][2]),))
            p.Set(name=grain_prefix + str(tempgrainnumber), faces=faces)
    elif dimension == 3:
        p = mdb.models[model_name].parts[part_name]
        c = p.cells
        tempgrainnumber = 0
        for cella in p.cells:
            tempgrainnumber = tempgrainnumber + 1
            puntocella = c[tempgrainnumber-1].pointOn
            cells = c.findAt(
                ((puntocella[0][0], puntocella[0][1], puntocella[0][2]),))
            p.Set(name=grain_prefix + str(tempgrainnumber), cells=cells)


def neper2cae(model_name='Model-1',
              part_name='PART-1',
              grain_prefix='GRAIN_',
              parametersfilename='',
              datumpointsfilename='',
              edgesfilename='',
              dimension=2):

    # =============================================================================
    # parameters
    # =============================================================================
    fparam = open(parametersfilename, "r")
    pwidth = float(fparam.readline())
    pheight = float(fparam.readline())
    pdepth = float(fparam.readline())
    if dimension == 2:
        pdepth = 0
    Ngrains = int(fparam.readline())
    caepath = fparam.readline()
    fparam.close()

    # =============================================================================
    # Mdb
    # =============================================================================
    executeOnCaeStartup()

    Mdb()

    create_sketch_base(model_name=model_name, width=pwidth,
                       height=pheight, center=[pwidth/2.0, pheight/2.0])

    create_part(model_name=model_name,
                part_name=part_name,
                dimension=dimension,
                pdepth=pdepth,
                pwidth=pwidth,
                pheight=pheight,
                datumpointsfilename=datumpointsfilename,
                edgesfilename=edgesfilename)

    create_set(model_name=model_name,
               part_name=part_name,
               grain_prefix=grain_prefix,
               dimension=dimension)

    mdb_name = r'mesh.cae'
    mdb.saveAs(pathName=mdb_name)
