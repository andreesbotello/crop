from django.contrib.gis.geos import GEOSGeometry
from crop.models import Parcelas
from scripts.crop.myLib import p1Settings

def run():
    g=GEOSGeometry('POLYGON ((711616.39484254620037973 4245621.08034353423863649, 711603.85678024333901703 4245594.95938040316104889, 711484.39690885762684047 4245656.95313290040940046, 711489.96938099223189056 4245668.79463618714362383, 711521.66281625779811293 4245670.18775422032922506, 711616.39484254620037973 4245621.08034353423863649))',
                    srid =25830)

    if g.valid:
        b=Parcelas(dueno='Juan Garcia', area= g.area, perimetro= g.length, cultivo= 'Tomate', geom = g)
        b.save()
        print(b.id)
    else:
        print('geometria invalida')

#windows. You don have GEOS
# deactivate in windows. You don have GEOS
#create the geometry with geos

#print the representation of the object
#print(g)
#create a building object, from the model Buildings
#b=Buildings(description='Edificio 1', area=100, geom=g)

#saves it into the database
#prints the asigned id of the object in the database
#print(b.id)
#another way to create the object with a dictionary
#d_of_values= {'description':'Edificio 1', 'area':2000}