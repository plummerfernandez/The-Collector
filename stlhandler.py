from stl import stl


filename = "test.stl"
mesh = stl.StlMesh(filename,calculate_normals=False) #do not calculate normals automatically


def getcartesianrange(vertarray): #give it the vertex array and calculate the min and max coords
	verts = []
	for vector in vertarray:
		for vert in vector:
			verts.append(vert)

	mymaxs = map(max, zip(*verts)) #iterably getting the max out of each xyz
	mymax = max(mymaxs) #getting the max of the maxes
	mymins = map(min, zip(*verts)) 
	mymin = min(mymins)
	#v1 = abs(mymax)
	#v2 = abs(mymin)
	#minmax = ([v2,v1])
	return mymin,mymax


###------------ Converting Vertices -------------###
minmax = getcartesianrange(mesh.vectors)
print "minmax = " + str(minmax)